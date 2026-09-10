# SRS — LocalBlast

**Especificación de Requerimientos de Software (SRS) — Ingeniería de Software 2026, FIUNER.**
Este documento es la línea base del proyecto **LocalBlast** al cierre del TP1. Se estructura en secciones y se apoya en documentos hermanos para el detalle de diagramas, casos de uso e historias de usuario.

---

## Índice

1. [Visión y alcance](#1-visión-y-alcance)
2. [Stakeholders y usuarios](#2-stakeholders-y-usuarios)
3. [Diagrama de contexto (DFD)](#3-diagrama-de-contexto-dfd)
4. [Modelo de dominio](#4-modelo-de-dominio)
5. [Selección de procesos a profundizar](#5-selección-de-procesos-a-profundizar)
6. [Requerimientos funcionales](#6-requerimientos-funcionales)
7. [Casos de uso e historias de usuario](#7-casos-de-uso-e-historias-de-usuario)
8. [Suposiciones y dependencias](#8-suposiciones-y-dependencias)
9. [Glosario](#9-glosario)

> **Nota:** los atributos de calidad (ISO 25010) con sus escenarios se incorporan en la siguiente entrega, según la reprogramación indicada por la cátedra.

---

## 1. Visión y alcance

### 1.1 Problema

La ejecución de alineamientos con BLAST presenta hoy dos alternativas incompletas para el usuario típico de un laboratorio o cursada:

- **Línea de comandos (BLAST+):** exige recordar la sintaxis de los binarios (`blastn`, `blastp`, `makeblastdb`, etc.), armar comandos con muchos parámetros, gestionar la ubicación de las bases de datos y parsear la salida a mano. Es la opción más flexible pero tiene barrera de entrada alta.
- **Interfaz web oficial de NCBI:** es accesible pero pesada, no permite ejecutar contra bases de datos propias del laboratorio, y no ofrece filtros interactivos post-búsqueda (identidad, cobertura, taxonomía) sobre la lista de resultados.

Ninguna de las dos permite hoy, con una sola herramienta: correr BLAST **local o remoto** desde la misma interfaz, con **bases de datos propias** del laboratorio administradas por un rol dedicado, aplicar **filtros pre-búsqueda** (parámetros del algoritmo) y **post-búsqueda** (refinamiento sobre resultados) de forma intuitiva, y **descargar los resultados** en el formato que más convenga.

### 1.2 Propuesta de valor

LocalBlast es una **interfaz web para BLAST+** que resuelve las tres carencias:

- El **investigador** decide con un botón si el alineamiento se corre localmente (contra bases de datos del laboratorio) o remotamente. En ambos casos el sistema invoca a BLAST+; en modo remoto le pasa la flag `-remote` y es BLAST+ quien se comunica con NCBI del otro lado.
- El **administrador** puede subir archivos FASTA para dejarlos disponibles como bases de datos locales — sean del propio laboratorio o de bases de datos públicas como SwissProt, que el administrador descarga por su cuenta antes de subirlas al sistema.
- Los **filtros pre-búsqueda** se cargan en un formulario con valores por defecto sensatos; los **filtros post-búsqueda** se aplican en la tabla de resultados sin volver a correr BLAST.
- Los **resultados** se descargan en CSV, JSON, FASTA, tabular BLAST o XML.

### 1.3 Dentro del alcance (TP1 → TP5)

- Interfaz web para investigador y administrador.
- Ejecución de búsquedas BLAST local (`blastn`, `blastp`, `blastx`, `tblastn`, `tblastx`) y remota (`-remote`).
- Formulario de parámetros pre-búsqueda con valores por defecto.
- Aplicación interactiva de filtros post-búsqueda sobre la tabla de resultados.
- Descarga de resultados en múltiples formatos.
- Alta, actualización y baja de bases de datos locales por parte del administrador, a partir de un archivo FASTA subido desde su equipo.
- Autenticación básica con dos roles (Investigador y Administrador).

### 1.4 Fuera del alcance

- Modificación del algoritmo BLAST subyacente. LocalBlast **usa** el motor BLAST+; no lo reimplementa.
- Herramientas de alineamiento múltiple (ClustalW, Muscle) o modelado 3D de estructuras.
- Búsquedas en lote con múltiples queries simultáneas en una sola ejecución (queda como posible ampliación en el Trabajo Integrador).
- Anotación funcional o enriquecimiento biológico de los hits más allá de lo que devuelve BLAST.

---

## 2. Stakeholders y usuarios

| Actor / Stakeholder | Rol | Usa el sistema | Interés en el proyecto |
|---|---|---|---|
| **Investigador/a** | Estudiante de grado/posgrado, tesista, becario/a, docente-investigador/a | Sí (usuario final principal) | Reducir el tiempo de las búsquedas BLAST recurrentes y evitar la fricción de la terminal o de la web de NCBI. |
| **Administrador/a de bases de datos** | Bioinformático/a del laboratorio, técnico/a de IT del grupo de investigación | Sí | Poder mantener bases de datos propias (secuencias del laboratorio) y espejos de bases públicas sin depender del acceso externo. |
| **Docente de la cursada** | Docente de bioinformática o materias afines | Sí (a través del rol Investigador) | Usar la herramienta en clases y trabajos prácticos, reemplazando parcialmente a la web de NCBI. |
| **NCBI** | Proveedor del servicio remoto de BLAST | No interactúa con LocalBlast; sus servidores son contactados por BLAST+ cuando se lo invoca con `-remote` | Establece los límites de uso de la API remota (rate limits) que BLAST+ respeta, y que indirectamente afectan al comportamiento visible del sistema. |
| **Cátedra de Ingeniería de Software (FIUNER)** | Evaluador del proyecto | No | Verificar la aplicación correcta de los conceptos del cuatrimestre. |

Los dos primeros son los actores del modelo de casos de uso (los que aparecen en el diagrama de contexto). El resto son stakeholders sin interacción directa con el sistema.

---

## 3. Diagrama de contexto (DFD)

Los diagramas de contexto (Nivel 0) y su descomposición (Nivel 1), junto con la descripción de procesos, almacenes y flujos, están en:

👉 [`docs/architecture/contexto-inicial.md`](../architecture/contexto-inicial.md)

---

## 4. Modelo de dominio

El modelo de dominio conceptual — entidades esenciales del problema y sus relaciones, sin atributos ni detalles de implementación — está en:

👉 [`docs/requirements/modelo-dominio.md`](modelo-dominio.md)

---

## 5. Selección de procesos a profundizar

De los tres procesos identificados en el DFD Nivel 1 (P1, P2, P3), el grupo elige llevar a profundidad **únicamente P1 (Ejecutar búsqueda BLAST)**. P2 (Filtrar y entregar resultados) y P3 (Administrar bases de datos) quedan documentados a nivel de alcance en el DFD y en el modelo de dominio, pero **no** se detallan como casos de uso propios ni tienen RF profundizados en este SRS.

### 5.1 Qué se profundiza y por qué

- **P1 · Ejecutar búsqueda BLAST — profundizado.** Es el proceso *core* del sistema: sin él no hay valor entregable. Concentra toda la complejidad interesante del dominio (dos modos de invocación a BLAST+ — con o sin `-remote` —, validación de parámetros pre-búsqueda, verificación de compatibilidad programa/query/base de datos, ejecución asíncrona con cancelación, y refinamiento posterior de resultados). De este proceso se derivan **dos casos de uso** con capacidades distintas del actor investigador: `CU001` (ejecutar una búsqueda BLAST) y `CU002` (refinar y descargar los resultados de una búsqueda). Ambos se detallan en [`docs/requirements/casos-de-uso.md`](casos-de-uso.md), con `CU001` descompuesto en slices y `CU002` sin subdivisión adicional.

### 5.2 Qué queda fuera del profundizado y por qué

- **P2 · Filtrar y entregar resultados — no profundizado como proceso en sí.** Se ejecuta enteramente sobre datos ya en memoria (filtros a la tabla y serialización a un formato) y su lógica es previsible: comparaciones numéricas y export a formatos estándar. Su capacidad hacia el actor sí queda cubierta —como parte de `CU002` (refinar y descargar los resultados de una búsqueda)—, porque desde el punto de vista del investigador aplicar filtros y bajar un archivo es una única capacidad. Como proceso técnico independiente, en cambio, no aporta descubrimiento significativo al TP1 ni riesgo de arquitectura para el TP3; su tratamiento como CU aparte con sus propios slices duplicaría trabajo sin ganar información.

- **P3 · Administrar bases de datos — no profundizado.** Es el proceso de un actor distinto (Administrador), con objetivo distinto y precondición distinta al de P1. Un caso de uso derivado de P3 —por ejemplo "Administrar base de datos BLAST local"— pertenece conceptualmente a ese proceso, no a P1, y por lo tanto queda fuera de la cadena `RF → CU → slice → HU` de este TP. Se documenta a nivel de alcance en el DFD Nivel 1 (con sus flujos hacia BLAST+ y hacia D1) y sus entidades siguen presentes en el modelo de dominio, pero sin RF ni CU propios profundizados en este cuatrimestre.

**Criterio general.** Esta decisión respeta la recomendación explícita de la cátedra: *"elegir uno bien resuelto vale más que varios a medio desarrollar"*. Concentrar el trabajo en P1 nos permite descomponerlo en los dos casos de uso que le da al investigador —lanzar una búsqueda y trabajar sobre sus resultados—, y todavía dentro de `CU001` distinguir dos slices con valor incremental (dejar la búsqueda validada, versus ejecutar y ver resultados). Es más rico que dispersar el esfuerzo entre procesos que responden a objetivos y actores diferentes.

**Nota sobre el enfoque de los CU.** Un caso de uso representa **una capacidad discreta que el sistema le da al actor**, no un trazo secuencial de pasos. Por eso del proceso P1 salen dos CU en vez de uno solo largo: la capacidad de correr una búsqueda (`CU001`) y la capacidad de refinar/descargar resultados (`CU002`) son dos objetivos distintos del mismo actor, aunque uno dependa del otro en cuanto a los datos. Ver la explicación completa en la sección "Enfoque de los casos de uso" de [`casos-de-uso.md`](casos-de-uso.md).

---

## 6. Requerimientos funcionales

Los RF-01 a RF-10 corresponden a **P1 (Ejecutar búsqueda BLAST)** y están repartidos entre los dos casos de uso derivados de ese proceso: `CU001` realiza RF-01 a RF-08 y `CU002` realiza RF-09 y RF-10. La tabla de trazabilidad detallada por slice está en [`casos-de-uso.md`](casos-de-uso.md).

Los requerimientos del proceso P3 (administración de bases de datos) no se incluyen en este SRS porque P3 no se profundiza en el cuatrimestre — ver justificación en la sección 5.2.

### Proceso P1 — Ejecución de búsqueda BLAST

| ID | Requerimiento |
|---|---|
| **RF-01** | El sistema debe permitir al usuario ingresar la secuencia query como texto pegado en el formulario o como archivo FASTA subido. |
| **RF-02** | El sistema debe permitir al usuario elegir entre dos modos de ejecución mutuamente excluyentes: **local** (invoca a BLAST+ contra una base de datos del catálogo del laboratorio) o **remoto** (invoca a BLAST+ con la flag `-remote`, y es BLAST+ el que se comunica con NCBI). |
| **RF-03** | El sistema debe permitir al usuario seleccionar una base de datos disponible para el modo elegido: en modo local, las que figuran en el catálogo administrado por P3; en modo remoto, las bases estándar de NCBI. |
| **RF-04** | El sistema debe permitir al usuario configurar los parámetros pre-búsqueda que afectan al algoritmo: **E-value máximo**, **matriz de sustitución** (para BLAST de proteínas), **tamaño de palabra** y **penalización de gaps** (apertura y extensión). El sistema debe ofrecer valores por defecto sensatos según el programa BLAST correspondiente. |
| **RF-05** | El sistema debe permitir al usuario elegir el programa BLAST a ejecutar (`blastn`, `blastp`, `blastx`, `tblastn`, `tblastx`) y debe verificar que esa elección sea compatible con el tipo de la secuencia query y con el tipo de la base de datos seleccionada. Si la combinación no es compatible, no permite lanzar la búsqueda e indica el motivo. |
| **RF-06** | El sistema debe validar, antes de ejecutar la búsqueda, que la secuencia query respete el alfabeto declarado o inferido (ADN, ARN o proteína) y que los parámetros pre-búsqueda estén dentro de rangos válidos. |
| **RF-07** | El sistema debe ejecutar la búsqueda de forma asíncrona, mostrando un indicador de progreso, sin bloquear la interfaz de usuario, y debe permitir cancelar una búsqueda en curso. |
| **RF-08** | El sistema debe mostrar los resultados en una tabla con, como mínimo: identificador del hit, score, E-value observado, porcentaje de identidad y porcentaje de cobertura. |
| **RF-09** | El sistema debe permitir aplicar filtros post-búsqueda sobre la tabla de resultados — al menos: umbrales de porcentaje de identidad, porcentaje de cobertura, E-value observado y filtro por taxonomía cuando la información esté disponible — sin volver a ejecutar la búsqueda. |
| **RF-10** | El sistema debe permitir al usuario descargar los resultados filtrados en al menos los formatos: CSV, JSON, FASTA, tabular BLAST (`-outfmt 6`) y XML. |

---

## 7. Casos de uso e historias de usuario

Los casos de uso en formato Cockburn (flujo principal detallado y slices secundarios nombrados), todos derivados del proceso profundizado P1, están en:

👉 [`docs/requirements/casos-de-uso.md`](casos-de-uso.md)

Las historias de usuario asociadas a cada slice (relación 1:1 slice ↔ HU), con criterios de aceptación en formato **Given-When-Then**, están en:

👉 [`docs/requirements/historias-usuario.md`](historias-usuario.md)

**Resumen de la cadena de trazabilidad `RF → CU → slice → HU`:**

- **CU001 · Ejecutar una búsqueda BLAST** realiza RF-01 a RF-08.
  - Slices del camino feliz (básicos): `CU001_B1` (cargar, configurar y validar), `CU001_B2` (ejecutar y presentar resultados).
  - Slices alternativos: `CU001_A1` (cancelación manual), `CU001_A2` (base de datos local no disponible — el sistema informa y el investigador decide).
  - Slices de excepción: `CU001_E1` (secuencia con formato inválido), `CU001_E2` (parámetros fuera de rango), `CU001_E3` (combinación programa/query/BD incompatible), `CU001_E4` (fallo del modo remoto de BLAST+).
- **CU002 · Refinar y descargar los resultados de una búsqueda** realiza RF-09 y RF-10.
  - Slice básico único (camino feliz corto, sin subdivisión): `CU002_B` (aplicar filtros y descargar).
  - Slice alternativo: `CU002_A1` (ningún resultado supera los filtros).
- **HU detalladas en este TP:** `HU01_CU001_B1`, `HU02_CU001_B2`, `HU03_CU002_B`, `HU04_CU001_E1`. El resto de los slices están **nombrados** en los CU y se detallarán como HU cuando algún TP posterior los necesite.

---

## 8. Suposiciones y dependencias

- El binario **BLAST+** (versión 2.14 o posterior) está disponible en el servidor donde corre el sistema. Es una dependencia externa: LocalBlast **usa** BLAST+, no lo empaqueta.
- La API remota de NCBI (`https://blast.ncbi.nlm.nih.gov/Blast.cgi`) está disponible desde la red del servidor cuando el usuario elige modo remoto — **BLAST+ es quien la contacta**, no directamente nuestra GUI. Las políticas de uso responsable de NCBI (frecuencia de polling, límite de queries por unidad de tiempo) las respeta BLAST+, no nuestro código.
- El servidor tiene espacio en disco suficiente para alojar las bases locales del laboratorio y los archivos temporales de las búsquedas.
- Los usuarios acceden por HTTPS desde navegadores modernos.
- **Precondición de catálogo.** Como P3 (administración del catálogo) no se profundiza en el TP1, para las historias de usuario que dependen del modo local (por ejemplo `HU01_CU001_B1` con base de datos local) se asume que ya existe al menos una base de datos cargada en el catálogo D1. El mecanismo por el cual llega ahí queda fuera del alcance profundizado.

---

## 9. Glosario

| Término | Significado |
|---|---|
| **BLAST** | *Basic Local Alignment Search Tool*: familia de algoritmos para buscar regiones de similitud local entre secuencias biológicas. |
| **BLAST+** | Suite oficial de línea de comandos de NCBI que implementa BLAST (`blastn`, `blastp`, `makeblastdb`, etc.). Es la herramienta que LocalBlast envuelve. |
| **Query** | Secuencia biológica que el investigador quiere alinear contra una base de datos. |
| **Base de datos BLAST** | Conjunto de secuencias biológicas indexadas para búsqueda BLAST. Físicamente: los archivos `.nhr/.nin/.nsq` (nucleótidos) o `.phr/.pin/.psq` (proteínas) generados por `makeblastdb`. |
| **Hit / Alineamiento** | Cada una de las coincidencias que BLAST devuelve entre la query y una secuencia de la base de datos. |
| **E-value** | Cantidad esperada de hits del mismo score o mejor que se obtendrían por azar. Cuanto más bajo, más significativa la coincidencia. |
| **Matriz de sustitución** | Tabla que puntúa cada posible sustitución entre residuos, usada por BLAST de proteínas (BLOSUM62, PAM30, etc.). |
| **FASTA** | Formato de texto para representar secuencias biológicas, con un encabezado `>ID descripción` seguido de la secuencia. |
| **SwissProt** | Base de datos curada de proteínas, parte de UniProtKB. Un ejemplo típico de base de datos pública que un laboratorio querría espejar localmente. |
| **`makeblastdb`** | Utilitario de BLAST+ que construye los índices de una base de datos a partir de un archivo FASTA. |
| **Filtro pre-búsqueda** | Valor de un parámetro del algoritmo BLAST que se fija antes de ejecutar y que afecta al resultado (E-value máximo, matriz, tamaño de palabra, etc.). |
| **Filtro post-búsqueda** | Criterio que se aplica sobre resultados ya calculados para restringir qué se muestra o descarga, sin volver a correr BLAST (umbral de % identidad, cobertura, taxón). |
| **Slice** | Corte de un caso de uso que aporta valor por sí mismo hacia el objetivo del CU. Puede ser básico (parte del camino feliz), alternativo (camino alterno) o de excepción (terminación abrupta). Se corresponde 1:1 con una historia de usuario. |
