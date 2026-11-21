"""RepositorioHistorialSqlite: arma el registro del historial y pide escribirlo.

Sabe *qué* se guarda (la búsqueda y sus alineamientos crudos, CA-03). *Cómo* se habla
con el motor de base de datos (conexión y transacción) lo sabe ConexionBD.
"""

import json
from typing import TYPE_CHECKING
from uuid import uuid4

from backend.acceso_datos.conexion_bd import ConexionBD
from backend.acceso_datos.repositorio_historial import RepositorioHistorial

if TYPE_CHECKING:
    from backend.ejecucion.busqueda import Busqueda

INSERTAR_BUSQUEDA = """
    INSERT INTO busqueda (id, fecha, variante, modo, base_datos, secuencia, parametros)
    VALUES (?, ?, ?, ?, ?, ?, ?)
"""
INSERTAR_ALINEAMIENTO = """
    INSERT INTO alineamiento (busqueda_id, orden, id_hit, descripcion, score, evalue,
                              identidades, longitud_alineamiento, query_desde, query_hasta)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


class RepositorioHistorialSqlite(RepositorioHistorial):
    def __init__(self, conexion: ConexionBD) -> None:
        self._conexion = conexion

    def guardar(self, busqueda: "Busqueda") -> None:
        id_busqueda = str(uuid4())
        registro = [(
            INSERTAR_BUSQUEDA,
            (
                id_busqueda,
                busqueda.fecha.isoformat(),
                busqueda.variante,
                busqueda.modo,
                busqueda.base_datos,
                busqueda.secuencia,
                json.dumps(busqueda.parametros),
            ),
        )]
        registro += [
            (
                INSERTAR_ALINEAMIENTO,
                (
                    id_busqueda,
                    orden,
                    alineamiento.id_hit,
                    alineamiento.descripcion,
                    alineamiento.score,
                    alineamiento.evalue,
                    alineamiento.identidades,
                    alineamiento.longitud_alineamiento,
                    alineamiento.query_desde,
                    alineamiento.query_hasta,
                ),
            )
            for orden, alineamiento in enumerate(busqueda.alineamientos, start=1)
        ]
        self._conexion.ejecutar_transaccion(registro)
