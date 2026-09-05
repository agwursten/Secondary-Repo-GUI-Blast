# LocalBlast 2026

## Integrantes

- Agustín Facundo Gaitán
- Augusto Wursten
- Valentín Farías

---

## Síntesis del proyecto

**LocalBlast** es una interfaz gráfica web sobre **BLAST+** — la suite oficial de línea de comandos de NCBI — que permite a investigadores y estudiantes ejecutar alineamientos de secuencias sin depender de la terminal ni de la carga de la interfaz oficial de NCBI. El motor de alineamiento es BLAST+ en todos los casos: LocalBlast no reimplementa BLAST, lo envuelve. Con un mismo formulario, el usuario elige si el alineamiento se corre localmente (BLAST+ contra bases de datos alojadas por el laboratorio) o de forma remota (BLAST+ con la flag `-remote`, que a su vez se comunica con NCBI); configura los parámetros del algoritmo y aplica filtros a los resultados antes de descargarlos. Un rol de administrador puede además cargar y mantener las bases de datos locales del laboratorio.

Para el detalle completo — visión, alcance, requerimientos funcionales, casos de uso, historias de usuario y modelo de dominio — ver el SRS:

👉 [`docs/requirements/srs.md`](docs/requirements/srs.md)

Documentos adicionales del SRS:

- [Diagrama de contexto (DFD N0 y N1)](docs/architecture/contexto-inicial.md)
- [Modelo de dominio conceptual](docs/requirements/modelo-dominio.md)
- [Casos de uso (Cockburn)](docs/requirements/casos-de-uso.md)
- [Historias de usuario con escenarios de aceptación](docs/requirements/historias-usuario.md)
- [Bitácora de uso de IA](docs/uso-ia.md)

---

## Modelo de ciclo de vida

El grupo adopta un **modelo iterativo e incremental con prácticas ágiles livianas** (tablero de tareas y revisiones cortas por TP), por dos razones concretas del proyecto:

1. **Los requerimientos están claros en el núcleo pero indefinidos en los bordes.** El corazón —lanzar una búsqueda BLAST desde una interfaz web y descargar el resultado— lo entendemos bien porque la herramienta subyacente (BLAST+) ya resuelve el algoritmo; pero los detalles de la administración de bases de datos por parte del laboratorio, y qué filtros post-búsqueda son realmente útiles para el usuario, los vamos a descubrir recién cuando mostremos versiones intermedias a un usuario real. Un modelo secuencial (cascada) obligaría a congelar esos detalles antes de tiempo.
2. **Hay valor entregable temprano.** Una primera iteración con solo búsqueda remota (invocando a BLAST+ con `-remote` contra NCBI) y descarga en un único formato ya demuestra el valor central y sirve para validar la interfaz antes de sumar la parte más costosa (BLAST+ local + administración de bases de datos). Alinea con el enfoque del cuatrimestre, donde cada TP es una iteración con su propio punto de control.

Se descartó **cascada** por la razón (1), y **espiral** porque el riesgo tecnológico del proyecto es acotado (BLAST+ está estable y bien documentado) — no justifica el sobrecosto de análisis de riesgo por iteración.
