"""Entidad Alineamiento: un hit que devolvió BLAST+ para una búsqueda.

Regla del negocio que vive acá (R1 del diseño detallado):
    % identidad = identidades / longitud del alineamiento * 100
    % cobertura = tramo de la query cubierto / longitud de la query * 100
"""

from backend.adaptador_blast.adaptador_blast import Hit


class Alineamiento:
    """Parte del agregado Busqueda: solo la crea su Busqueda."""

    def __init__(self, hit: Hit, longitud_query: int) -> None:
        if hit["longitud_alineamiento"] <= 0:
            raise ValueError("Un alineamiento no puede tener longitud 0.")
        if longitud_query <= 0:
            raise ValueError("La longitud de la query tiene que ser mayor que 0.")
        self.id_hit: str = hit["id_hit"]
        self.descripcion: str = hit["descripcion"]
        self.score: float = hit["score"]
        self.evalue: float = hit["evalue"]
        self.identidades: int = hit["identidades"]
        self.longitud_alineamiento: int = hit["longitud_alineamiento"]
        self.query_desde: int = hit["query_desde"]
        self.query_hasta: int = hit["query_hasta"]
        self.longitud_query: int = longitud_query

    def porcentaje_identidad(self) -> float:
        return self.identidades / self.longitud_alineamiento * 100

    def porcentaje_cobertura(self) -> float:
        # BLAST+ puede informar el tramo invertido (por ejemplo, en marcos negativos de blastx).
        tramo = abs(self.query_hasta - self.query_desde) + 1
        return min(tramo / self.longitud_query * 100, 100.0)
