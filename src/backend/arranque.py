"""Punto de arranque del Backend: el único lugar que elige y arma las implementaciones.

Se configura con variables de entorno (todas opcionales):

    LOCALBLAST_BLAST               simulado (por defecto) | real
    LOCALBLAST_BLAST_DIR           carpeta de los ejecutables de BLAST+ (si no están en el PATH)
    LOCALBLAST_LIMITE_SEGUNDOS     tiempo máximo de una ejecución de BLAST+ (por defecto 1800)
    LOCALBLAST_SIMULADO_DEMORA     segundos que tarda el BLAST+ simulado (por defecto 3)
    LOCALBLAST_SIMULADO_CAMPO_NUEVO  1 para que el simulado agregue un campo desconocido (EC-02)
    LOCALBLAST_PERSISTENCIA        sqlite (por defecto) | memoria
    LOCALBLAST_BD                  archivo SQLite del historial (por defecto datos/historial.sqlite3)

Uso, desde la raíz del repositorio:
    uvicorn backend.arranque:app --app-dir src --port 8000
"""

import logging
import os
from pathlib import Path

from backend.acceso_datos.conexion_bd import ConexionBD
from backend.acceso_datos.repositorio_historial import RepositorioHistorial
from backend.acceso_datos.repositorio_historial_memoria import RepositorioHistorialEnMemoria
from backend.acceso_datos.repositorio_historial_sqlite import RepositorioHistorialSqlite
from backend.adaptador_blast.adaptador_blast import AdaptadorBlast
from backend.adaptador_blast.adaptador_blast_cli import AdaptadorBlastCli, ejecutar_subproceso
from backend.adaptador_blast.blast_simulado import BlastSimulado
from backend.controladores.rutas import crear_app
from backend.ejecucion.controlador_ejecucion import ControladorEjecucion

RAIZ = Path(__file__).resolve().parents[2]

logging.basicConfig(level=logging.INFO, format="%(levelname)s [%(name)s] %(message)s")
logger = logging.getLogger("localblast")


def crear_adaptador() -> AdaptadorBlast:
    tipo = os.environ.get("LOCALBLAST_BLAST", "simulado")
    if tipo == "real":
        ejecutor = ejecutar_subproceso
    elif tipo == "simulado":
        ejecutor = BlastSimulado(
            demora_segundos=float(os.environ.get("LOCALBLAST_SIMULADO_DEMORA", "3")),
            campo_nuevo=os.environ.get("LOCALBLAST_SIMULADO_CAMPO_NUEVO") == "1",
        )
    else:
        raise SystemExit(f"LOCALBLAST_BLAST debe ser 'real' o 'simulado', no '{tipo}'.")
    directorio_blast = os.environ.get("LOCALBLAST_BLAST_DIR")
    logger.info("BLAST+: %s", tipo)
    return AdaptadorBlastCli(
        ejecutor,
        directorio_blast=Path(directorio_blast) if directorio_blast else None,
        directorio_trabajo=RAIZ,  # las rutas relativas de las bases se resuelven desde la raíz
        limite_segundos=float(os.environ.get("LOCALBLAST_LIMITE_SEGUNDOS", "1800")),
    )


def crear_repositorio() -> RepositorioHistorial:
    tipo = os.environ.get("LOCALBLAST_PERSISTENCIA", "sqlite")
    if tipo == "memoria":
        logger.info("Historial: en memoria")
        return RepositorioHistorialEnMemoria()
    if tipo == "sqlite":
        ruta = Path(os.environ.get("LOCALBLAST_BD", RAIZ / "datos" / "historial.sqlite3"))
        logger.info("Historial: SQLite en %s", ruta)
        return RepositorioHistorialSqlite(ConexionBD(ruta))
    raise SystemExit(f"LOCALBLAST_PERSISTENCIA debe ser 'sqlite' o 'memoria', no '{tipo}'.")


controlador = ControladorEjecucion(crear_adaptador(), crear_repositorio())
app = crear_app(controlador, carpeta_web=RAIZ / "src" / "web" / "dist")
