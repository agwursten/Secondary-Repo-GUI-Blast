"""Interfaz RepositorioHistorial: qué se puede hacer con el historial (D2).

ControladorEjecucion solo conoce esta interfaz, así que cambiar la persistencia
(SQLite o memoria) no lo modifica.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.ejecucion.busqueda import Busqueda


class RepositorioHistorial(ABC):
    @abstractmethod
    def guardar(self, busqueda: "Busqueda") -> None:
        """Guarda la búsqueda con sus parámetros, base, fecha y todos sus alineamientos crudos."""
