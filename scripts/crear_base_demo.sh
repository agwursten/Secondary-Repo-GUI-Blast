#!/usr/bin/env bash
# Construye la base de datos BLAST local de demostración con makeblastdb (BLAST+).
# Solo hace falta para usar LocalBlast con BLAST+ real; el BLAST+ simulado no la necesita.
#
# Uso (desde la raíz del repositorio):
#     bash scripts/crear_base_demo.sh
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DESTINO="$RAIZ/datos/blastdb"

if ! command -v makeblastdb >/dev/null 2>&1; then
    echo "No se encontró makeblastdb. Instalá BLAST+ (por ejemplo: sudo apt install ncbi-blast+)." >&2
    exit 1
fi

mkdir -p "$DESTINO"
makeblastdb \
    -in "$RAIZ/datos/ejemplo/base_proteinas_demo.fasta" \
    -dbtype prot \
    -parse_seqids \
    -title "Proteinas de demostracion de LocalBlast" \
    -out "$DESTINO/proteinas_demo"

echo "Base creada en $DESTINO/proteinas_demo"
