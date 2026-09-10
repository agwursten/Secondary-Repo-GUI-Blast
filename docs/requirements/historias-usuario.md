# Historias de Usuario — LocalBlast

Cada historia de usuario detalla **un slice puntual** de un caso de uso (relación 1:1). El identificador de la HU conserva explícitamente el del slice de origen, para que la trazabilidad sea directa: la HU llamada `HU01_CU001_B1` detalla el slice `B1` del caso de uso `CU001`.

Formato de cada HU:

- **Deriva de**: qué CU y qué slice detalla.
- **Realiza**: qué RF materializa este slice (heredados del CU y del slice de origen).
- **Rol – meta – motivo**: "Como … quiero … para …".
- **Criterios de aceptación**: en formato **Given-When-Then**, trazables a la precondición y postcondición del slice.

Para el TP1 se detallan las HU de los **tres slices básicos** del camino feliz (`B1`, `B2`, `B3`) del único caso de uso profundizado (`CU001`), más una HU de un slice de excepción representativo (`E1`, secuencia con formato inválido). El resto de los slices están **nombrados en el caso de uso** ([`casos-de-uso.md`](casos-de-uso.md)) y se detallarán como HU cuando algún TP posterior los necesite — no es obligación abrirlos todos ya, como aclara la propia guía del TP1.

---

## HU derivadas del slice básico de CU001

### HU01_CU001_B1 · Cargar, configurar y validar una búsqueda BLAST

- **Deriva de:** `CU001`, slice `B1` (pasos 1-7 del camino feliz)
- **Realiza:** RF-01, RF-02, RF-03, RF-04, RF-05, RF-06

> **Como** investigador/a,
> **quiero** cargar mi secuencia query, elegir el modo (local o remoto), la base de datos, el programa BLAST y los parámetros pre-búsqueda, y que el sistema valide todo antes de habilitar la ejecución,
> **para** no perder tiempo lanzando búsquedas mal configuradas.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Configuración completa y válida en modo remoto:
  - **Given** una secuencia FASTA de proteína válida pegada en el formulario, modo remoto seleccionado, base de datos remota "nr", programa `blastp` y parámetros pre-búsqueda en sus valores por defecto,
  - **When** el investigador presiona "Ejecutar búsqueda",
  - **Then** el sistema valida la secuencia y los parámetros, no muestra errores, y habilita la ejecución de la búsqueda (transición al slice `B2`).

- **CA-02.** Valores por defecto sensatos según el programa:
  - **Given** un formulario donde el investigador acaba de seleccionar el programa `blastp`,
  - **When** la interfaz carga los parámetros pre-búsqueda,
  - **Then** los campos de E-value máximo, matriz de sustitución, tamaño de palabra y penalización de gaps aparecen prellenados con los valores por defecto correspondientes al programa `blastp` (no los mismos que para `blastn`).

- **CA-03.** Base de datos coherente con el modo elegido:
  - **Given** el investigador cambia el modo de "remoto" a "local",
  - **When** el sistema recarga la lista de bases de datos disponibles,
  - **Then** la lista muestra únicamente las bases de datos del catálogo local (leídas de D1), sin las bases estándar de NCBI que aparecían en modo remoto.

---

### HU02_CU001_B2 · Ejecutar la búsqueda BLAST y presentar los resultados crudos

- **Deriva de:** `CU001`, slice `B2` (pasos 8-9 del camino feliz)
- **Realiza:** RF-07, RF-08

> **Como** investigador/a,
> **quiero** que el sistema ejecute la búsqueda en segundo plano y me muestre los resultados en una tabla cuando termine,
> **para** poder seguir trabajando mientras se ejecuta y luego revisar los hits sin cargar otra pantalla.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Ejecución asíncrona con indicador de progreso:
  - **Given** una búsqueda ya configurada y validada (postcondición del slice `B1`),
  - **When** el sistema invoca a BLAST+ en segundo plano,
  - **Then** la interfaz muestra un indicador de progreso visible y permanece navegable — el investigador puede desplazarse dentro de la aplicación sin que la ejecución se interrumpa.

- **CA-02.** Presentación de la tabla al finalizar:
  - **Given** una búsqueda que finalizó correctamente y BLAST+ devolvió al menos un hit,
  - **When** el sistema recibe los resultados,
  - **Then** los presenta en una tabla con al menos las columnas: identificador del hit, score, E-value observado, porcentaje de identidad y porcentaje de cobertura.

---

### HU03_CU001_B3 · Filtrar, descargar y persistir los resultados de la búsqueda

- **Deriva de:** `CU001`, slice `B3` (pasos 10-12 del camino feliz)
- **Realiza:** RF-09, RF-10

> **Como** investigador/a,
> **quiero** aplicar filtros post-búsqueda sobre la tabla de resultados sin volver a correr BLAST y luego descargar los hits filtrados en el formato que necesite,
> **para** llevarme solo los alineamientos relevantes y en la forma en que voy a seguir procesándolos.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Filtrado interactivo sin re-ejecución:
  - **Given** una tabla de resultados con al menos 20 hits y filtros post-búsqueda establecidos en identidad ≥ 80% y cobertura ≥ 50%,
  - **When** el investigador confirma los filtros,
  - **Then** la tabla se re-filtra en el momento mostrando solo los hits que cumplen ambos umbrales, sin volver a invocar a BLAST+.

- **CA-02.** Descarga en el formato elegido:
  - **Given** una tabla de resultados con filtros post-búsqueda ya aplicados,
  - **When** el investigador selecciona formato "CSV" y presiona "Descargar",
  - **Then** el sistema entrega un archivo `.csv` que contiene únicamente los hits filtrados, con una fila de encabezados que incluye al menos las columnas mínimas (identificador, score, E-value observado, % identidad, % cobertura).

- **CA-03.** Persistencia en el historial:
  - **Given** una descarga que finalizó correctamente,
  - **When** el archivo termina de entregarse al investigador,
  - **Then** el sistema guarda en el historial (D2) una entrada con los parámetros de la búsqueda, la base de datos usada, el timestamp y el conjunto de resultados obtenidos (antes de aplicar los filtros post-búsqueda).

---

## HU derivada de un slice de excepción de CU001

### HU04_CU001_E1 · Rechazo de secuencia query con formato inválido

- **Deriva de:** `CU001`, slice `E1` (terminación abrupta detectada en el paso 7)
- **Realiza:** RF-06

> **Como** investigador/a,
> **quiero** recibir un mensaje claro cuando la secuencia que subo o pego no es reconocible,
> **para** poder corregirla de inmediato sin tener que adivinar qué le pasa.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Caracter fuera del alfabeto:
  - **Given** un texto pegado como query que contiene al menos un carácter fuera del alfabeto de ADN, ARN o proteína (por ejemplo un dígito o un símbolo de puntuación),
  - **When** el investigador presiona "Ejecutar búsqueda",
  - **Then** el sistema no invoca a BLAST+, corta el flujo del CU y muestra un mensaje que indica cuál es el carácter inválido y en qué posición aparece.

- **CA-02.** FASTA con encabezado sin cuerpo:
  - **Given** un archivo FASTA con una línea de encabezado (`>ID`) pero sin ninguna línea de secuencia debajo,
  - **When** el investigador presiona "Ejecutar búsqueda",
  - **Then** el sistema no invoca a BLAST+, corta el flujo del CU y muestra el mensaje "El FASTA contiene un encabezado pero ninguna secuencia asociada".

---

## Tabla de trazabilidad completa `RF → CU → slice → HU`

| RF | CU | Slice | HU |
|---|---|---|---|
| RF-01, RF-02, RF-03, RF-04, RF-05, RF-06 | CU001 | B1 | **HU01_CU001_B1** |
| RF-07, RF-08 | CU001 | B2 | **HU02_CU001_B2** |
| RF-09, RF-10 | CU001 | B3 | **HU03_CU001_B3** |
| RF-06 | CU001 | E1 | **HU04_CU001_E1** |
| RF-07 | CU001 | A1 (cancelación manual) | *nombrada, sin detallar aún* |
| RF-09, RF-10 | CU001 | A2 (resultado vacío) | *nombrada, sin detallar aún* |
| RF-03 | CU001 | A3 (BD local no disponible) | *nombrada, sin detallar aún* |
| RF-04, RF-06 | CU001 | E2 (parámetros fuera de rango) | *nombrada, sin detallar aún* |
| RF-05 | CU001 | E3 (combinación incompatible) | *nombrada, sin detallar aún* |
| RF-07 | CU001 | E4 (fallo modo remoto) | *nombrada, sin detallar aún* |

Los slices nombrados sin HU detallada no son un olvido: la propia guía del TP1 aclara que "no todo slice justifica ese nivel de inversión" y que se detallan solo cuando un TP posterior los necesita.

---

## Notas sobre el enfoque de este TP

- **Un CU puede implementar varios RF**, y viceversa un mismo RF puede estar realizado por varios slices del mismo CU — por ejemplo RF-06 (validación pre-ejecución) aparece en el slice `B1` cuando la validación pasa y también en los slices `E1` y `E2` cuando falla y corta el flujo. La trazabilidad de la tabla de arriba refleja esa realidad.
- **La unidad mínima de sprint es la HU**, no el CU ni el slice. Por eso las HU están nombradas con un identificador propio (`HU01`, `HU02`, …) además del sufijo de trazabilidad — para que la planificación de sprints pueda referirse a ellas sin ambigüedad.
- **Los criterios de aceptación en formato Given-When-Then** son la semilla de los casos de prueba de TP5 (Módulo 6). Cada `Then` describe un resultado observable — un mensaje puntual, una columna que debe aparecer, un archivo que se entrega — nunca una descripción de implementación interna.
