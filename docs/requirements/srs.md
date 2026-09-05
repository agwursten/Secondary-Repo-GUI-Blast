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

De los tres procesos identificados en el DFD Nivel 1 (P1, P2, P3), el grupo elige llevar a profundidad **P1 (Ejecutar búsqueda BLAST)** y **P3 (Administrar bases de datos)**. P2 (Filtrar y entregar resultados) queda documentado a nivel de alcance en el DFD pero no se profundiza como caso de uso propio.

### 5.1 Qué se profundiza y por qué

- **P1 · Ejecutar búsqueda BLAST — profundizado.** Es el proceso *core* del sistema: sin él no hay valor entregable. Concentra la complejidad interesante (dos modos de invocación a BLAST+ — con o sin `-remote` —, validación de parámetros pre-búsqueda, verificación de compatibilidad programa/query/base de datos, y ejecución asíncrona). Se detalla como CU-01.

- **P3 · Administrar bases de datos — profundizado.** Es el proceso que habilita el modo local, que es lo que diferencia a LocalBlast de "otra GUI para búsquedas remotas". Sin P3 el laboratorio no puede tener bases de datos propias, y el sistema pierde la mitad de su propuesta de valor. Se detalla como CU-02.

### 5.2 Qué queda fuera del profundizado y por qué

- **P2 · Filtrar y entregar resultados — no profundizado.** Se ejecuta enteramente sobre datos ya en memoria (filtros a la tabla y serialización a un formato) y su lógica es previsible: comparaciones numéricas y export a formatos estándar. No aporta descubrimiento significativo al TP1 ni riesgo de arquitectura para el TP3. Va a ser cubierto en detalle recién en el TP4 (diseño detallado) y TP5 (pruebas), donde su naturaleza combinatoria — muchos filtros, muchos formatos — recién se vuelve relevante.

Elegir dos procesos y no los tres cumple con la recomendación explícita de la cátedra: **"elegir uno bien resuelto vale más que varios a medio desarrollar"**. Se eligieron dos porque están fuertemente relacionados en la propuesta de valor del proyecto (búsqueda local + gestión de bases locales son la misma feature vista desde dos roles distintos), y separar uno sin el otro no capturaría bien el dominio.

---

## 6. Requerimientos funcionales

Los RF-01 a RF-10 corresponden a **P1 (Ejecutar búsqueda BLAST)** y son realizados por el CU-01.
Los RF-11 a RF-14 corresponden a **P3 (Administrar bases de datos)** y son realizados por el CU-02.

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

### Proceso P3 — Administración de bases de datos

| ID | Requerimiento |
|---|---|
| **RF-11** | El sistema debe permitir al administrador dar de alta una nueva base de datos local, indicando: nombre visible, tipo (nucleótidos o proteínas) y archivo FASTA de origen, subido desde su equipo. |
| **RF-12** | El sistema debe construir los índices BLAST (`makeblastdb`) de la nueva base de datos en segundo plano, mostrando un indicador de progreso y sin bloquear la interfaz. |
| **RF-13** | El sistema debe validar que el archivo FASTA sea legible y que su contenido sea consistente con el tipo declarado, y debe rechazar la creación de la base de datos con un mensaje explicativo si la validación falla. |
| **RF-14** | El sistema debe permitir al administrador actualizar o dar de baja una base de datos existente del catálogo, sin afectar las búsquedas en curso ni el historial de búsquedas ya realizadas. |

---

## 7. Casos de uso e historias de usuario

Los casos de uso en formato Cockburn (flujo principal detallado y slices secundarios nombrados) están en:

👉 [`docs/requirements/casos-de-uso.md`](casos-de-uso.md)

Las historias de usuario ya detalladas para el TP1 (slice básico + un slice secundario por CU, con escenarios de aceptación en prosa) están en:

👉 [`docs/requirements/historias-usuario.md`](historias-usuario.md)

**Resumen de la cadena de trazabilidad:**

- **CU-01** realiza RF-01 a RF-10. Slice básico → **HU-01**. Slice A1 → **HU-01.A1**. Slices A2–A7 nombrados.
- **CU-02** realiza RF-11 a RF-14. Slice básico → **HU-02a**. Slice A1 → **HU-02.A1**. Slices A2–A4 nombrados.

---

## 8. Suposiciones y dependencias

- El binario **BLAST+** (versión 2.14 o posterior) está disponible en el servidor donde corre el sistema. Es una dependencia externa: LocalBlast **usa** BLAST+, no lo empaqueta.
- La API remota de NCBI (`https://blast.ncbi.nlm.nih.gov/Blast.cgi`) está disponible desde la red del servidor cuando el usuario elige modo remoto — **BLAST+ es quien la contacta**, no directamente nuestra GUI. Las políticas de uso responsable de NCBI (frecuencia de polling, límite de queries por unidad de tiempo) las respeta BLAST+, no nuestro código.
- El servidor tiene espacio en disco suficiente para alojar las bases locales del laboratorio y los archivos temporales de las búsquedas.
- Los usuarios acceden por HTTPS desde navegadores modernos.

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
