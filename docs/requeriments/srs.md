# SRS — LocalBlast

**Especificación de Requerimientos de Software (SRS)**
Este documento es la línea base del proyecto **LocalBlast** al cierre del TP1. Se estructura en secciones y se apoya en documentos hermanos para el detalle de diagramas, casos de uso e historias de usuario.

---

## Índice

1. [Visión y alcance](#1-visión-y-alcance)
2. [Stakeholders y actores del sistema](#2-stakeholders-y-actores-del-sistema)
3. [Diagrama de contexto (DFD)](#3-diagrama-de-contexto-dfd)
4. [Modelo de dominio](#4-modelo-de-dominio)
5. [Selección de procesos a profundizar](#5-selección-de-procesos-a-profundizar)
6. [Requerimientos funcionales](#6-requerimientos-funcionales)
7. [Casos de uso e historias de usuario](#7-casos-de-uso-e-historias-de-usuario)
8. [Suposiciones y dependencias](#8-suposiciones-y-dependencias)
9. [Glosario](#9-glosario)

---

## 1. Visión y alcance

### 1.1 Problema

La ejecución de alineamientos con BLAST presenta hoy dos alternativas incompletas para el usuario típico de un laboratorio o cursada:

- **Línea de comandos (BLAST+):** exige recordar la sintaxis de los binarios (`blastn`, `blastp`, `makeblastdb`, etc.), armar comandos con muchos parámetros, gestionar la ubicación de las bases de datos y parsear la salida a mano. Es la opción más flexible pero tiene barrera de entrada alta.
- **Interfaz web oficial de NCBI:** es accesible pero pesada, no permite ejecutar contra bases de datos propias del laboratorio, y no ofrece filtros interactivos post-búsqueda (identidad, cobertura, taxonomía) sobre la lista de resultados.

Ninguna de las dos permite hoy, con una sola herramienta: correr BLAST **local o remoto** desde la misma interfaz, con **bases de datos propias** del laboratorio administradas por un rol dedicado, aplicar **filtros pre-búsqueda** (parámetros del algoritmo) y **post-búsqueda** (refinamiento sobre resultados) de forma intuitiva, y **descargar los resultados** en el formato que más convenga.

### 1.2 Propuesta de valor

LocalBlast es una **interfaz gráfica para BLAST+** que resuelve las carencias identificadas:

- El **investigador** decide con un botón si el alineamiento se corre localmente (contra bases de datos del laboratorio ya cargadas en el catálogo) o remotamente. En ambos casos el sistema invoca a BLAST+; en modo remoto le pasa la flag `-remote` y es BLAST+ quien se comunica con NCBI del otro lado.
- Los **filtros pre-búsqueda** se cargan en un formulario con valores por defecto sensatos; los **filtros post-búsqueda** se aplican en la tabla de resultados sin volver a correr BLAST.
- Los **resultados** se descargan en CSV, JSON, FASTA, tabular BLAST o XML.

> **Nota sobre el rol Administrador.** El diseño integral del sistema contempla también un **rol Administrador** encargado de subir archivos FASTA (del propio laboratorio o de bases públicas como SwissProt) para dejarlos disponibles como bases de datos locales. Esta capacidad aparece en los diagramas de contexto y en el modelo de dominio para dejar la visión completa del producto, pero **queda fuera del alcance del TP1 de este cuatrimestre por restricciones de tiempo** (ver §1.4). Para las funcionalidades de modo local se asume que el catálogo ya está poblado por fuera del sistema.

### 1.3 Dentro del alcance

- Interfaz web para el rol **Investigador**.
- Ejecución de búsquedas BLAST local (`blastn`, `blastp`, `blastx`, `tblastn`, `tblastx`) y remota (`-remote`).
- Formulario de parámetros pre-búsqueda con valores por defecto.
- Aplicación interactiva de filtros post-búsqueda sobre la tabla de resultados.
- Descarga de resultados en múltiples formatos.
- Persistencia automática de las búsquedas ejecutadas en un historial, para uso futuro.

### 1.4 Fuera del alcance

- **Administración de bases de datos locales por parte del rol Administrador (proceso P3).** El diseño integral del sistema contempla un rol Administrador que da de alta, actualiza y da de baja bases de datos BLAST locales a partir de archivos FASTA subidos desde su equipo, invocando internamente a `makeblastdb`. Esta capacidad **se documenta a nivel conceptual** en el DFD (Nivel 0 y Nivel 1, ver [`docs/architecture/contexto-inicial.md`](../architecture/contexto-inicial.md)) y en el modelo de dominio, para dejar registrada la visión completa del producto, pero **queda fuera del alcance de este cuatrimestre por restricciones de tiempo**: no tiene requerimientos funcionales asociados, no se detalla como casos de uso ni historias de usuario, y no se implementará en el TP. Para las funcionalidades del modo local se asume que el catálogo D1 ya contiene al menos una base de datos, cargada por fuera del sistema.
- **Autenticación y gestión de usuarios/roles.** Dado que en el cuatrimestre solo se profundiza el rol Investigador, no se implementa autenticación ni gestión de sesiones. Queda para versiones futuras junto con la incorporación del rol Administrador.
- Modificación del algoritmo BLAST subyacente. LocalBlast **usa** el motor BLAST+; no lo reimplementa.
- Herramientas de alineamiento múltiple (ClustalW, Muscle) o modelado 3D de estructuras.
- Búsquedas en lote con múltiples queries simultáneas en una sola ejecución (queda como posible ampliación en el Trabajo Integrador).
- Anotación funcional o enriquecimiento biológico de los hits más allá de lo que devuelve BLAST.

---
## 2. Stakeholders y actores del sistema

### 2.1 Stakeholders

Se conservan los stakeholders identificados en el canvas de descubrimiento (ver [README](../../README.md#1-canvas-de-descubrimiento-síntesis) del repositorio):

- **Estudiantes de Grado y Posgrado.** Necesitan realizar alineamientos locales rápidos para trabajos prácticos o investigación sin perder tiempo en la configuración de entornos por terminal.
- **Investigadores y Docentes de Bioinformática / Biología Molecular.** Buscan una herramienta ágil e intuitiva para explorar resultados con filtros visuales personalizados que no están disponibles de forma nativa en la web tradicional.

Estos son los grupos humanos cuyo interés motiva el proyecto. No son (necesariamente) categorías exhaustivas de los actores del sistema, ni describen quién tiene qué permiso en la aplicación, para eso ver la subsección siguiente.

### 2.2 Actores del sistema

Los stakeholders anteriores interactúan con el sistema tomando alguno de estos dos roles operativos, que son los que aparecen en el DFD Nivel 0 y en el modelo de dominio:

- **Investigador/a.** El actor principal del proceso profundizado P1. Es quien ejecuta búsquedas, refina resultados y los descarga. Cualquiera de los dos grupos de stakeholders arriba mencionados puede asumir este rol.
- **Administrador/a de bases de datos.** El actor del proceso P3 (no profundizado en este TP). Es quien mantiene el catálogo de bases de datos locales del laboratorio. Suele ser un bioinformático o técnico de IT del grupo de investigación, aunque nada impide que un investigador con permisos administre su propio catálogo.

Además, el sistema dialoga con un **actor no humano**: **BLAST+**, la suite oficial de línea de comandos de NCBI, que aparece como sistema externo en el DFD. LocalBlast lo invoca, no lo reimplementa.

---

## 3. Diagrama de contexto (DFD)

Los diagramas de contexto (Nivel 0) y su descomposición (Nivel 1), junto con la descripción de procesos, almacenes y flujos, están en:

👉 [`docs/architecture/contexto-inicial.md`](../architecture/contexto-inicial.md)

---

## 4. Modelo de dominio

El modelo de dominio conceptual, entidades esenciales del problema y sus relaciones sin atributos ni detalles de implementación, está en:

👉 [`docs/requirements/modelo-dominio.md`](modelo-dominio.md)

---

## 5. Selección de procesos a profundizar

De los tres procesos identificados en el DFD Nivel 1 (P1, P2, P3), el grupo elige llevar a profundidad **P1 (Ejecutar búsqueda BLAST) y P2 (Filtrar y entregar resultados)**. Ambos son necesarios para cerrar una interacción típica del investigador con el sistema: P1 se ocupa de correr la búsqueda y dejarla persistida, y P2 le permite al investigador trabajar sobre esos resultados (filtrarlos y descargarlos) a su conveniencia. El proceso **P3 (Administrar bases de datos)** queda documentado a nivel de alcance en el DFD y en el modelo de dominio, pero **no** se detalla como casos de uso propios ni tiene RF profundizados en este SRS.

### 5.1 Qué se profundiza y por qué

- **P1 · Ejecutar búsqueda BLAST — profundizado.** Es el proceso *core* del sistema: sin él no hay valor entregable. Concentra la complejidad interesante del dominio (dos modos de invocación a BLAST+ — con o sin `-remote` —, validación de parámetros pre-búsqueda, verificación de compatibilidad programa/query/base de datos, ejecución asíncrona con cancelación y persistencia automática en el historial). Da lugar a **un caso de uso**, `CU001 · Ejecutar una búsqueda BLAST`, descompuesto en dos slices básicos `B1` (cargar, configurar y validar) y `B2` (ejecutar, presentar resultados y persistir), más sus alternativas y excepciones.

- **P2 · Filtrar y entregar resultados — profundizado.** Es lo que le permite al investigador cerrar la interacción con valor real: sin filtrar ni descargar, la búsqueda queda "en el aire" en la interfaz. P2 se ejecuta sobre los datos ya devueltos por BLAST+ y su lógica es previsible (comparaciones numéricas para el filtro, serialización para la descarga), pero es indispensable para el flujo típico del usuario y por eso lo profundizamos. Da lugar a **dos casos de uso** con capacidades distintas para el mismo actor investigador: `CU002 · Refinar los resultados con filtros post-búsqueda` y `CU003 · Descargar los resultados en un formato`. Están detallados en [`docs/requeriments/casos-de-uso.md`](casos-de-uso.md).

### 5.2 Qué queda fuera del profundizado y por qué

- **P3 · Administrar bases de datos — no profundizado.** Es el proceso de un actor distinto (Administrador), con objetivo distinto y precondición distinta a los procesos anteriores. Un caso de uso derivado de P3, por ejemplo "Administrar base de datos BLAST local", pertenece conceptualmente a ese proceso, no a P1 ni a P2, y por lo tanto queda fuera de la cadena `RF → CU → slice → HU` de este TP. Se documenta a nivel de alcance en el DFD Nivel 1 (con sus flujos hacia BLAST+ y hacia D1) y sus entidades siguen presentes en el modelo de dominio, pero sin RF ni CU propios profundizados en este cuatrimestre.

**Criterio general.** Esta decisión respeta la recomendación explícita de la cátedra: *"elegir uno bien resuelto vale más que varios a medio desarrollar"*. Concentrar el trabajo en los dos procesos que cubren una interacción completa del investigador (P1 y P2) nos permite descomponer esa interacción en las tres capacidades que el sistema le da —lanzar una búsqueda, refinar resultados, descargarlos—, y todavía dentro de `CU001` distinguir dos slices con valor incremental (dejar la búsqueda validada, versus ejecutar y ver resultados). Es más rico que dispersar el esfuerzo entre P3, que responde a un objetivo y a un actor diferentes.

---

## 6. Requerimientos funcionales
Los RF-01 a RF-11 corresponden a los procesos profundizados P1 y P2. La tabla de trazabilidad detallada por slice está en [`casos-de-uso.md`](casos-de-uso.md).

### 6.1 Proceso P1 — Ejecución de búsqueda BLAST

Realizados por `CU001` (ejecutar una búsqueda).

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
| **RF-11** | El sistema debe persistir automáticamente en el historial (D2) cada búsqueda que termine su ejecución exitosamente, incluyendo parámetros pre-búsqueda, base de datos usada, timestamp y el conjunto **crudo** de resultados que devolvió BLAST+ |

### 6.2 Proceso P2 — Filtrado y entrega de resultados

Realizados por `CU002` (refinar con filtros post-búsqueda) y `CU003` (descargar en un formato).

| ID | Requerimiento |
|---|---|
| **RF-09** | El sistema debe permitir aplicar filtros post-búsqueda sobre la tabla de resultados (al menos: umbrales de porcentaje de identidad, porcentaje de cobertura, E-value observado y filtro por taxonomía cuando la información esté disponible) sin volver a ejecutar la búsqueda. |
| **RF-10** | El sistema debe permitir al usuario descargar los resultados actualmente visibles en la tabla (filtrados o sin filtrar) en al menos los formatos: CSV, JSON, FASTA, tabular BLAST (`-outfmt 6`) y XML. |

---

## 7. Casos de uso e historias de usuario

Los casos de uso en formato Cockburn (flujo principal detallado y slices secundarios nombrados), todos derivados del proceso profundizado P1, están en:

👉 [`docs/requirements/casos-de-uso.md`](casos-de-uso.md)

Las historias de usuario asociadas a cada slice (relación 1:1 slice ↔ HU), con criterios de aceptación en formato **Given-When-Then**, están en:

👉 [`docs/requirements/historias-usuario.md`](historias-usuario.md)

## 8. Suposiciones y dependencias

- El binario **BLAST+** (versión 2.14 o posterior) está disponible en el servidor donde corre el sistema. Es una dependencia externa: LocalBlast **usa** BLAST+, no lo empaqueta.
- La API remota de NCBI (`https://blast.ncbi.nlm.nih.gov/Blast.cgi`) está disponible desde la red del servidor cuando el usuario elige modo remoto — **BLAST+ es quien la contacta**, no directamente nuestra GUI. Las políticas de uso responsable de NCBI (frecuencia de polling, límite de queries por unidad de tiempo) las respeta BLAST+, no nuestro código.
- El sistema tiene espacio suficiente para alojar las bases locales del laboratorio y los archivos temporales de las búsquedas.
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
| **Historial (D2)** | Almacén interno donde se persisten las búsquedas ejecutadas y sus resultados crudos. En esta versión solo se escribe; la lectura queda como uso futuro. |


