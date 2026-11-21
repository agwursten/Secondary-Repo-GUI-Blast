"""BlastSimulado: reemplaza al sistema externo BLAST+ cuando no está instalado.

No reemplaza al adaptador: AdaptadorBlastCli arma el comando y lee la salida igual que
con BLAST+ real. Lo único simulado es el programa que se ejecuta. Devuelve la salida
grabada de una ejecución real de `blastp` (BLAST+ 2.12) de la proteína de
demostración contra la base `proteinas_demo`, después de una demora configurable
para que se vea el indicador de progreso.

Comportamiento:
- Base local que no se llama `proteinas_demo`: responde como BLAST+ cuando no
  encuentra la base (código 2 y el mismo mensaje de error).
- Modo remoto (-remote): devuelve la salida grabada con cualquier base.
- `campo_nuevo=True`: agrega a cada HSP un campo que el sistema no conoce, como si
  fuera una versión nueva de BLAST+ (sirve para mostrar el escenario EC-02).
"""

import time
from pathlib import Path

from backend.adaptador_blast.adaptador_blast_cli import ResultadoComando

SALIDA_GRABADA = Path(__file__).with_name("salida_grabada_demo.xml")
BASES_LOCALES = frozenset({"proteinas_demo"})


class BlastSimulado:
    def __init__(
        self,
        demora_segundos: float = 3.0,
        campo_nuevo: bool = False,
        salida_grabada: Path = SALIDA_GRABADA,
    ) -> None:
        self._demora_segundos = demora_segundos
        self._campo_nuevo = campo_nuevo
        self._salida = salida_grabada.read_text(encoding="utf-8")

    def __call__(
        self,
        comando: list[str],
        entrada: str,
        directorio: Path | None,
        limite_segundos: float | None,
    ) -> ResultadoComando:
        time.sleep(self._demora_segundos)
        base = comando[comando.index("-db") + 1]
        if "-remote" not in comando and Path(base).name not in BASES_LOCALES:
            return ResultadoComando(
                codigo=2,
                salida="",
                errores=(
                    "BLAST Database error: No alias or index file found for protein "
                    f"database [{base}] in search path [{directorio or ''}::]"
                ),
            )
        salida = self._salida
        if self._campo_nuevo:
            salida = salida.replace(
                "</Hsp_gaps>", "</Hsp_gaps>\n      <Hsp_nuevo-campo>0</Hsp_nuevo-campo>"
            )
        return ResultadoComando(codigo=0, salida=salida, errores="")
