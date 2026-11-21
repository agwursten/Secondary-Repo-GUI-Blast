-- Esquema del historial de búsquedas (almacén D2).
-- Se aplica automáticamente al iniciar el Backend; todas las sentencias son idempotentes.

PRAGMA journal_mode = WAL;  -- permite leer mientras otra búsqueda escribe (EC-01)

CREATE TABLE IF NOT EXISTS busqueda (
    id          TEXT PRIMARY KEY,
    fecha       TEXT NOT NULL,      -- ISO 8601 con zona horaria
    variante    TEXT NOT NULL,      -- blastn, blastp, blastx, tblastn, tblastx
    modo        TEXT NOT NULL,      -- local o remoto
    base_datos  TEXT NOT NULL,      -- ruta del índice local o nombre de la base de NCBI
    secuencia   TEXT NOT NULL,      -- query en FASTA
    parametros  TEXT NOT NULL       -- parámetros pre-búsqueda en JSON
);

CREATE TABLE IF NOT EXISTS alineamiento (
    busqueda_id            TEXT    NOT NULL REFERENCES busqueda (id),
    orden                  INTEGER NOT NULL,
    id_hit                 TEXT    NOT NULL,
    descripcion            TEXT    NOT NULL,
    score                  REAL    NOT NULL,   -- bit score
    evalue                 REAL    NOT NULL,
    identidades            INTEGER NOT NULL,
    longitud_alineamiento  INTEGER NOT NULL,
    query_desde            INTEGER NOT NULL,
    query_hasta            INTEGER NOT NULL,
    PRIMARY KEY (busqueda_id, orden)
);
