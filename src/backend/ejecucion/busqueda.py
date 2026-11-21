"""Entidad Busqueda: raíz del agregado Busqueda–Alineamiento.

Reglas que viven acá:
    R2 · Al historial va el conjunto completo de alineamientos crudos: se crea un
         Alineamiento por cada hit que devolvió BLAST+, sin descartar ninguno.
    Los resultados se registran una sola vez (no se agregan a un conjunto anterior).
"""

from datetime import datetime

from backend.adaptador_blast.adaptador_blast import Hit
from backend.ejecucion.alineamiento import Alineamiento


class Busqueda:
    """Una consulta BLAST con su configuración validada y los alineamientos que produjo."""

    def __init__(self, configuracion: dict, fecha: datetime) -> None:
        self.secuencia: str = configuracion["secuencia"]
        self.variante: str = configuracion["variante"]
        self.modo: str = configuracion["modo"]
        self.base_datos: str = configuracion["base_datos"]
        self.parametros: dict = dict(configuracion.get("parametros") or {})
        self.fecha: datetime = fecha
        self._alineamientos: list[Alineamiento] = []
        self._resultados_registrados = False

    @property
    def remota(self) -> bool:
        return self.modo == "remoto"

    @property
    def longitud_query(self) -> int:
        """Cantidad de residuos de la query, sin el encabezado FASTA ni espacios."""
        lineas = (linea for linea in self.secuencia.splitlines() if not linea.startswith(">"))
        return sum(len("".join(linea.split())) for linea in lineas)

    @property
    def alineamientos(self) -> tuple[Alineamiento, ...]:
        return tuple(self._alineamientos)

    def registrar_resultados(self, hits: list[Hit]) -> None:
        if self._resultados_registrados:
            raise ValueError("La búsqueda ya tiene sus resultados registrados.")
        longitud = self.longitud_query
        self._alineamientos = [Alineamiento(hit, longitud) for hit in hits]
        self._resultados_registrados = True

    def tabla_resultados(self) -> list[dict]:
        return [
            {
                "id_hit": alineamiento.id_hit,
                "descripcion": alineamiento.descripcion,
                "score": alineamiento.score,
                "evalue": alineamiento.evalue,
                "porcentaje_identidad": alineamiento.porcentaje_identidad(),
                "porcentaje_cobertura": alineamiento.porcentaje_cobertura(),
            }
            for alineamiento in self._alineamientos
        ]
