"""Componente Controladores (capa de presentación del Backend).

Solo traduce HTTP: valida la forma de la solicitud JSON, llama a
ControladorEjecucion.ejecutar_busqueda y convierte el resultado (o el ErrorBlast) en
la respuesta JSON. No tiene lógica del dominio.

La ruta se declara con `def` (no `async def`): FastAPI atiende cada solicitud en un
hilo propio de su pool, así varias búsquedas corren a la vez sin bloquearse (EC-01).
"""

from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

from backend.ejecucion.controlador_ejecucion import ControladorEjecucion, ErrorBlast


class SolicitudEjecucion(BaseModel):
    """Configuración validada que envía la Aplicación Web (los campos extra se ignoran)."""

    model_config = ConfigDict(extra="ignore")

    secuencia: str = Field(min_length=1)
    variante: Literal["blastn", "blastp", "blastx", "tblastn", "tblastx"]
    modo: Literal["local", "remoto"]
    base_datos: str = Field(min_length=1)
    parametros: dict[str, int | float | str] = Field(default_factory=dict)


def crear_app(controlador: ControladorEjecucion, carpeta_web: Path | None = None) -> FastAPI:
    app = FastAPI(title="LocalBlast", version="1.0")

    @app.post("/api/busquedas/ejecucion")
    def ejecutar_busqueda(solicitud: SolicitudEjecucion):
        try:
            filas = controlador.ejecutar_busqueda(solicitud.model_dump())
        except ErrorBlast as error:
            return JSONResponse(
                status_code=502, content={"tipo": "ErrorBlast", "mensaje": str(error)}
            )
        return {"filas": filas}

    if carpeta_web is not None and (carpeta_web / "index.html").is_file():
        # Interfaz ya compilada (npm run build): se sirve desde el mismo puerto.
        app.mount("/", StaticFiles(directory=carpeta_web, html=True), name="web")

    return app
