"""ConexionBD: frontera hacia el motor de base de datos (SQLite).

Es lo único que conoce el motor: abre la conexión, ejecuta las sentencias y confirma
la transacción. Regla R7: el registro del historial se escribe completo o no se
escribe (si una sentencia falla, se deshace todo).

Cada llamada abre su propia conexión, así que puede usarse desde varios hilos a la vez
(EC-01). El esquema se crea al construir el objeto si todavía no existe.
"""

import sqlite3
from pathlib import Path

ESQUEMA = Path(__file__).with_name("esquema.sql")

Sentencia = tuple[str, tuple]


class ConexionBD:
    def __init__(self, ruta: Path, limite_espera_segundos: float = 30.0) -> None:
        self._ruta = ruta
        self._limite_espera_segundos = limite_espera_segundos
        ruta.parent.mkdir(parents=True, exist_ok=True)
        conexion = self._abrir()
        try:
            conexion.executescript(ESQUEMA.read_text(encoding="utf-8"))
        finally:
            conexion.close()

    def ejecutar_transaccion(self, registro: list[Sentencia]) -> None:
        conexion = self._abrir()
        try:
            with conexion:  # confirma al salir, o deshace todo si hubo una excepción
                for sentencia, valores in registro:
                    conexion.execute(sentencia, valores)
        finally:
            conexion.close()

    def _abrir(self) -> sqlite3.Connection:
        conexion = sqlite3.connect(self._ruta, timeout=self._limite_espera_segundos)
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion
