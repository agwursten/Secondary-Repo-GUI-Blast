"""AdaptadorBlastCli: invoca a BLAST+ por línea de comandos y lee su salida XML.

Es el único lugar del sistema que conoce el formato de BLAST+ (DA-03).

- Táctica "introducir concurrencia" (EC-01, DA-04): cada llamada a `ejecutar` lanza
  un subproceso propio de BLAST+ y espera su salida. No hay estado compartido entre
  búsquedas: los hits vuelven por la misma llamada que los pidió.
- Táctica "adaptar la interfaz" (EC-02): `leer_salida` toma los campos que conoce por
  su nombre; si la salida trae campos desconocidos, los ignora y los advierte con
  `registrar_advertencia`, sin tocar los conocidos (R5).

Quién ejecuta el comando se recibe por el constructor (`ejecutor`). En producción es
`ejecutar_subproceso` (BLAST+ real); para demostraciones y pruebas puede ser
`BlastSimulado`, que reemplaza al sistema externo BLAST+ y no al adaptador.
"""

import logging
import subprocess
import xml.etree.ElementTree as ET
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from backend.adaptador_blast.adaptador_blast import AdaptadorBlast, ErrorBlast, Hit

logger = logging.getLogger("localblast.adaptador_blast")


@dataclass(frozen=True)
class ResultadoComando:
    codigo: int
    salida: str
    errores: str


EjecutorComando = Callable[[list[str], str, Path | None, float | None], ResultadoComando]


def ejecutar_subproceso(
    comando: list[str], entrada: str, directorio: Path | None, limite_segundos: float | None
) -> ResultadoComando:
    """Ejecuta BLAST+ real como subproceso independiente (DA-04)."""
    proceso = subprocess.run(
        comando,
        input=entrada,
        capture_output=True,
        text=True,
        cwd=directorio,
        timeout=limite_segundos,
        check=False,
    )
    return ResultadoComando(proceso.returncode, proceso.stdout, proceso.stderr)


# Parámetros pre-búsqueda que se traducen a opciones de BLAST+.
OPCIONES_BLAST = {
    "evalue": "-evalue",
    "word_size": "-word_size",
    "matrix": "-matrix",
    "gapopen": "-gapopen",
    "gapextend": "-gapextend",
    "max_target_seqs": "-max_target_seqs",
}

# Etiquetas del formato XML de BLAST+ (-outfmt 5, NCBI_BlastOutput.dtd) que el sistema conoce.
CAMPOS_CONOCIDOS = frozenset({
    "BlastOutput", "BlastOutput_program", "BlastOutput_version", "BlastOutput_reference",
    "BlastOutput_db", "BlastOutput_query-ID", "BlastOutput_query-def", "BlastOutput_query-len",
    "BlastOutput_query-seq", "BlastOutput_param", "BlastOutput_iterations", "BlastOutput_mbstat",
    "Parameters", "Parameters_matrix", "Parameters_expect", "Parameters_include",
    "Parameters_sc-match", "Parameters_sc-mismatch", "Parameters_gap-open", "Parameters_gap-extend",
    "Parameters_filter", "Parameters_pattern", "Parameters_entrez-query",
    "Iteration", "Iteration_iter-num", "Iteration_query-ID", "Iteration_query-def",
    "Iteration_query-len", "Iteration_hits", "Iteration_stat", "Iteration_message",
    "Statistics", "Statistics_db-num", "Statistics_db-len", "Statistics_hsp-len",
    "Statistics_eff-space", "Statistics_kappa", "Statistics_lambda", "Statistics_entropy",
    "Hit", "Hit_num", "Hit_id", "Hit_def", "Hit_accession", "Hit_len", "Hit_hsps",
    "Hsp", "Hsp_num", "Hsp_bit-score", "Hsp_score", "Hsp_evalue", "Hsp_query-from",
    "Hsp_query-to", "Hsp_hit-from", "Hsp_hit-to", "Hsp_pattern-from", "Hsp_pattern-to",
    "Hsp_query-frame", "Hsp_hit-frame", "Hsp_identity", "Hsp_positive", "Hsp_gaps",
    "Hsp_align-len", "Hsp_density", "Hsp_qseq", "Hsp_hseq", "Hsp_midline",
})

# Identificador que BLAST+ asigna a las secuencias de bases creadas sin -parse_seqids.
PREFIJO_ID_ORDINAL = "gnl|BL_ORD_ID|"


class AdaptadorBlastCli(AdaptadorBlast):
    def __init__(
        self,
        ejecutor: EjecutorComando = ejecutar_subproceso,
        directorio_blast: Path | None = None,
        directorio_trabajo: Path | None = None,
        limite_segundos: float | None = None,
    ) -> None:
        self._ejecutor = ejecutor
        self._directorio_blast = directorio_blast
        self._directorio_trabajo = directorio_trabajo
        self._limite_segundos = limite_segundos

    def ejecutar(
        self,
        variante: str,
        secuencia: str,
        base_datos: str,
        remota: bool,
        parametros: dict,
    ) -> list[Hit]:
        comando = self._armar_comando(variante, base_datos, remota, parametros)
        try:
            resultado = self._ejecutor(
                comando, secuencia, self._directorio_trabajo, self._limite_segundos
            )
        except FileNotFoundError:
            raise ErrorBlast(
                f"No se encontró el programa '{comando[0]}'. Verificá que BLAST+ esté "
                "instalado y en el PATH, o indicá su carpeta en LOCALBLAST_BLAST_DIR."
            ) from None
        except subprocess.TimeoutExpired:
            raise ErrorBlast(
                f"BLAST+ no terminó dentro del límite de {self._limite_segundos:g} segundos."
            ) from None
        if resultado.codigo != 0:
            mensaje = resultado.errores.strip()
            raise ErrorBlast(mensaje or f"BLAST+ terminó con código {resultado.codigo}.")
        return self.leer_salida(resultado.salida)

    def leer_salida(self, salida_xml: str) -> list[Hit]:
        try:
            raiz = ET.fromstring(salida_xml)
        except ET.ParseError as error:
            raise ErrorBlast(f"La salida de BLAST+ no es un XML válido: {error}") from None
        desconocidos = sorted({elemento.tag for elemento in raiz.iter()} - CAMPOS_CONOCIDOS)
        if desconocidos:
            self.registrar_advertencia(desconocidos)
        return [self._leer_hit(hit) for hit in raiz.iter("Hit")]

    def registrar_advertencia(self, campos: list[str]) -> None:
        logger.warning(
            "La salida de BLAST+ trae campos que el sistema no conoce y se ignoran: %s",
            ", ".join(campos),
        )

    # --- detalles del formato de BLAST+ -------------------------------------------

    def _armar_comando(
        self, variante: str, base_datos: str, remota: bool, parametros: dict
    ) -> list[str]:
        programa = str(self._directorio_blast / variante) if self._directorio_blast else variante
        # Sin -query: BLAST+ lee la secuencia de la entrada estándar.
        comando = [programa, "-db", base_datos, "-outfmt", "5"]
        if remota:
            comando.append("-remote")
        for nombre, opcion in OPCIONES_BLAST.items():
            if nombre in parametros:
                comando += [opcion, str(parametros[nombre])]
        return comando

    def _leer_hit(self, hit: ET.Element) -> Hit:
        hsp = hit.find("Hit_hsps/Hsp")  # El primer HSP es el de mejor score.
        if hsp is None:
            raise ErrorBlast("La salida de BLAST+ tiene un hit sin alineamientos (Hsp).")
        identificador = _campo(hit, "Hit_id")
        descripcion = _campo(hit, "Hit_def")
        if identificador.startswith(PREFIJO_ID_ORDINAL):
            # Base sin -parse_seqids: el identificador real es la primera palabra de la definición.
            identificador, _, descripcion = descripcion.partition(" ")
        return Hit(
            id_hit=identificador,
            descripcion=descripcion,
            score=float(_campo(hsp, "Hsp_bit-score")),
            evalue=float(_campo(hsp, "Hsp_evalue")),
            identidades=int(_campo(hsp, "Hsp_identity")),
            longitud_alineamiento=int(_campo(hsp, "Hsp_align-len")),
            query_desde=int(_campo(hsp, "Hsp_query-from")),
            query_hasta=int(_campo(hsp, "Hsp_query-to")),
        )


def _campo(elemento: ET.Element, nombre: str) -> str:
    texto = elemento.findtext(nombre)
    if texto is None:
        raise ErrorBlast(f"La salida de BLAST+ no tiene el campo obligatorio {nombre}.")
    return texto
