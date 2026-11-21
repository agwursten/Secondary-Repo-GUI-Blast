"""Genera los datos de demostración de LocalBlast.

Crea una proteína query sintética y una base de proteínas sintéticas con variantes
de esa query a distintos porcentajes de identidad y de cobertura, más algunas
proteínas sin relación (que BLAST+ no debería informar como hits).

Los encabezados van sin acentos porque makeblastdb solo acepta ASCII.
Todas las secuencias son inventadas: sirven para mostrar el sistema funcionando con
BLAST+ real sin depender de bases públicas. Los archivos generados ya están en el
repositorio; este script solo hace falta para regenerarlos.

Uso (desde la raíz del repositorio):
    python3 scripts/generar_datos_demo.py
"""

import random
from pathlib import Path

AMINOACIDOS = "ACDEFGHIKLMNPQRSTVWY"
LONGITUD_QUERY = 420
SEMILLA = 2026
CARPETA = Path(__file__).resolve().parent.parent / "datos" / "ejemplo"

# (identificador, porcentaje de identidad buscado, fracción de la query que cubre)
VARIANTES = [
    ("demo_var01", 0.99, 1.00),
    ("demo_var02", 0.95, 1.00),
    ("demo_var03", 0.90, 1.00),
    ("demo_var04", 0.85, 0.95),
    ("demo_var05", 0.78, 1.00),
    ("demo_var06", 0.70, 0.90),
    ("demo_var07", 0.62, 1.00),
    ("demo_var08", 0.55, 0.80),
    ("demo_var09", 0.48, 1.00),
    ("demo_var10", 0.92, 0.45),
    ("demo_var11", 0.40, 0.70),
    ("demo_var12", 0.35, 1.00),
]
SIN_RELACION = 6


def secuencia_al_azar(rng: random.Random, longitud: int) -> str:
    return "".join(rng.choice(AMINOACIDOS) for _ in range(longitud))


def mutar(rng: random.Random, secuencia: str, identidad: float) -> str:
    residuos = list(secuencia)
    for i, residuo in enumerate(residuos):
        if rng.random() > identidad:
            residuos[i] = rng.choice(AMINOACIDOS.replace(residuo, ""))
    return "".join(residuos)


def en_lineas(secuencia: str, ancho: int = 60) -> str:
    return "\n".join(secuencia[i:i + ancho] for i in range(0, len(secuencia), ancho))


def main() -> None:
    rng = random.Random(SEMILLA)
    query = "M" + secuencia_al_azar(rng, LONGITUD_QUERY - 1)

    CARPETA.mkdir(parents=True, exist_ok=True)
    (CARPETA / "proteina_demo.fasta").write_text(
        ">proteina_demo Proteina sintetica de demostracion de LocalBlast\n"
        + en_lineas(query) + "\n",
        encoding="utf-8",
    )

    registros = []
    for identificador, identidad, cobertura in VARIANTES:
        largo = round(len(query) * cobertura)
        inicio = rng.randint(0, len(query) - largo)
        tramo = mutar(rng, query[inicio:inicio + largo], identidad)
        extremo = secuencia_al_azar(rng, rng.randint(5, 30))
        descripcion = (f"Variante sintetica de la proteina de demostracion "
                       f"(~{round(identidad * 100)}% identidad, ~{round(cobertura * 100)}% cobertura)")
        registros.append((identificador, descripcion, extremo + tramo))
    for numero in range(1, SIN_RELACION + 1):
        registros.append((f"demo_otra{numero:02d}", "Proteina sintetica sin relacion con la query",
                          "M" + secuencia_al_azar(rng, rng.randint(250, 500))))

    (CARPETA / "base_proteinas_demo.fasta").write_text(
        "".join(f">{ident} {desc}\n{en_lineas(seq)}\n" for ident, desc, seq in registros),
        encoding="utf-8",
    )
    print(f"Datos generados en {CARPETA}")


if __name__ == "__main__":
    main()
