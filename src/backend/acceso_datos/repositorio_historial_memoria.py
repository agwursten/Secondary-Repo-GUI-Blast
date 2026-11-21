"""RepositorioHistorialEnMemoria: historial que vive mientras corre el proceso.

Implementa la misma interfaz que el repositorio SQLite. Sirve para las pruebas y para
correr el sistema sin base de datos (LOCALBLAST_PERSISTENCIA=memoria): el controlador
no cambia.
"""

from threading import Lock
from typing import TYPE_CHECKING

from backend.acceso_datos.repositorio_historial import RepositorioHistorial

if TYPE_CHECKING:
    from backend.ejecucion.busqueda import Busqueda


class RepositorioHistorialEnMemoria(RepositorioHistorial):
    def __init__(self) -> None:
        self._guardadas: list["Busqueda"] = []
        self._candado = Lock()

    def guardar(self, busqueda: "Busqueda") -> None:
        with self._candado:
            self._guardadas.append(busqueda)

    @property
    def guardadas(self) -> tuple["Busqueda", ...]:
        with self._candado:
            return tuple(self._guardadas)
