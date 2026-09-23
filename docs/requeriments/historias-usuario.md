# Historias de Usuario — LocalBlast

Cada historia de usuario detalla **un slice puntual** de un caso de uso (relación 1:1). El identificador de la HU conserva explícitamente el del slice de origen, para que la trazabilidad sea directa: la HU llamada `HU01_CU001_B1` detalla el slice `B1` del caso de uso `CU001`; la HU `HU10_CU003_B` detalla el (único) slice básico `B` del caso de uso `CU003`.

Formato de cada HU:

- **Deriva de**: qué CU y qué slice detalla.
- **Realiza**: qué RF materializa este slice (heredados del CU y del slice de origen).
- **Rol – meta – motivo**: "Como … quiero … para …".
- **Criterios de aceptación**: en formato **Given-When-Then**, trazables a la precondición y postcondición del slice.

Para el TP1 se detallan las HU de **todos los slices identificados en los casos de uso** — los cuatro básicos (`CU001_B1`, `CU001_B2`, `CU002_B`, `CU003_B`), las tres alternativas (`CU001_A1`, `CU001_A2`, `CU003_A1`) y las cuatro excepciones (`CU001_E1`, `CU001_E2`, `CU001_E3`, `CU001_E4`). En total, 11 historias de usuario.

**Numeración:** las HU se enumeran de forma consecutiva por CU y, dentro de cada CU, en el orden: slices básicos (`B` / `B1`, `B2`) → slices alternativos (`A1`, `A2`, …) → slices de excepción (`E1`, `E2`, …). Así los identificadores acompañan el orden en el que aparecen los slices en [`casos-de-uso.md`](casos-de-uso.md).

---

## HU derivadas de CU001 · Ejecutar una búsqueda BLAST

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

### HU02_CU001_B2 · Ejecutar la búsqueda BLAST, presentar los resultados y persistir en el historial

- **Deriva de:** `CU001`, slice `B2` (pasos 8-9 del camino feliz)
- **Realiza:** RF-07, RF-08, RF-11

> **Como** investigador/a,
> **quiero** que el sistema ejecute la búsqueda en segundo plano, me muestre los resultados en una tabla dentro de la misma vista cuando termine, y guarde la búsqueda en el historial automáticamente,
> **para** poder seguir trabajando en la aplicación mientras la búsqueda corre —sin quedarme atado a una pantalla de espera— y no perder la búsqueda aunque no llegue a descargarla ni refinarla en esta sesión.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Ejecución asíncrona con indicador de progreso:
  - **Given** una búsqueda ya configurada y validada (postcondición del slice `B1`),
  - **When** el sistema invoca a BLAST+ en segundo plano,
  - **Then** la interfaz muestra un indicador de progreso visible y permanece navegable — el investigador puede desplazarse dentro de la aplicación sin que la ejecución se interrumpa.

- **CA-02.** Presentación de la tabla al finalizar:
  - **Given** una búsqueda que finalizó correctamente y BLAST+ devolvió al menos un hit,
  - **When** el sistema recibe los resultados,
  - **Then** los presenta en una tabla con al menos las columnas: identificador del hit, score, E-value observado, porcentaje de identidad y porcentaje de cobertura.

- **CA-03.** Persistencia automática en el historial:
  - **Given** una búsqueda que finalizó correctamente,
  - **When** el sistema termina de mostrar los resultados en la tabla,
  - **Then** queda registrada en el historial (D2) una entrada con los parámetros pre-búsqueda, la base de datos usada, el timestamp y el conjunto **completo** de resultados crudos que devolvió BLAST+ (antes de cualquier filtro post-búsqueda) — sin que el investigador tenga que ejercer `CU002` ni `CU003` para que la persistencia ocurra.

---

### HU03_CU001_A1 · Cancelación manual de una búsqueda en curso

- **Deriva de:** `CU001`, slice `A1` (camino alternativo durante el slice `B2`)
- **Realiza:** RF-07

> **Como** investigador/a,
> **quiero** poder cancelar una búsqueda que está en ejecución,
> **para** dejar de esperar y no consumir recursos remotos ni locales cuando me di cuenta que configuré algo mal o el resultado ya dejó de importarme.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Cancelación de una búsqueda local:
  - **Given** una búsqueda en modo local que BLAST+ está ejecutando en el servidor (indicador de progreso visible),
  - **When** el investigador presiona "Cancelar",
  - **Then** el sistema aborta el subproceso local de BLAST+, deja la interfaz lista para configurar otra búsqueda desde cero, no muestra tabla de resultados y no persiste nada en D2.

- **CA-02.** Cancelación de una búsqueda remota:
  - **Given** una búsqueda en modo remoto que BLAST+ tramita contra NCBI (indicador de progreso visible),
  - **When** el investigador presiona "Cancelar",
  - **Then** el sistema cancela la solicitud a través de BLAST+, deja la interfaz lista para configurar otra búsqueda desde cero, no muestra tabla de resultados y no persiste nada en D2.

---

### HU04_CU001_A2 · Manejo de base de datos local no disponible

- **Deriva de:** `CU001`, slice `A2` (camino alternativo en el paso 3)
- **Realiza:** RF-03

> **Como** investigador/a,
> **quiero** que el sistema me informe claramente cuando la base de datos local que elegí no está en condiciones de ser usada, y me devuelva la lista actualizada para que yo decida,
> **para** no quedarme trabado ni terminar corriendo contra una base equivocada porque el sistema me la sustituyó por su cuenta.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Base de datos en proceso de actualización:
  - **Given** modo local seleccionado y una base de datos del catálogo D1 que está en estado "actualizándose" porque P3 la está reconstruyendo en ese momento,
  - **When** el investigador la selecciona en el paso 3,
  - **Then** el sistema muestra el mensaje "La base de datos '\<nombre\>' está siendo actualizada y no puede usarse en este momento" y devuelve al investigador al paso 3 con la lista de bases locales actualizada, **sin** proponer un cambio automático a modo remoto.

- **CA-02.** Base de datos con índice en error:
  - **Given** modo local seleccionado y una base de datos cuyo índice quedó marcado como "con errores" tras un fallo previo de `makeblastdb`,
  - **When** el investigador la selecciona en el paso 3,
  - **Then** el sistema muestra un mensaje que explica que el índice está corrupto y sugiere contactar al administrador de bases de datos, y devuelve al investigador al paso 3.

---

### HU05_CU001_E1 · Rechazo de secuencia query con formato inválido

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

### HU06_CU001_E2 · Rechazo de parámetros pre-búsqueda fuera de rango

- **Deriva de:** `CU001`, slice `E2` (terminación abrupta detectada en el paso 7)
- **Realiza:** RF-04, RF-06

> **Como** investigador/a,
> **quiero** que el sistema me señale exactamente qué parámetro está fuera de rango y cuál es el rango válido para el programa BLAST que elegí,
> **para** poder corregirlo sin consultar la documentación de BLAST+ por afuera.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** E-value negativo:
  - **Given** un formulario completo con el campo "E-value máximo" en `-1`,
  - **When** el investigador presiona "Ejecutar búsqueda",
  - **Then** el sistema no invoca a BLAST+, corta el flujo del CU y muestra un mensaje que señala el campo "E-value" e indica que debe ser un número positivo (típicamente entre 0 y 10).

- **CA-02.** Tamaño de palabra fuera del rango del programa:
  - **Given** un formulario con programa `blastn` seleccionado y "Tamaño de palabra" = 3 (por debajo del mínimo válido para `blastn`),
  - **When** el investigador presiona "Ejecutar búsqueda",
  - **Then** el sistema no invoca a BLAST+, corta el flujo del CU y muestra un mensaje que señala el campo "Tamaño de palabra" e indica el rango válido para el programa `blastn`.

---

### HU07_CU001_E3 · Rechazo de combinación programa / query / base de datos incompatible

- **Deriva de:** `CU001`, slice `E3` (terminación abrupta detectada en el paso 7)
- **Realiza:** RF-05

> **Como** investigador/a,
> **quiero** que el sistema me impida lanzar una combinación de programa BLAST y tipos de secuencia/base incompatibles, y me sugiera qué combinaciones sí funcionan con lo que ya cargué,
> **para** no perder tiempo esperando un resultado que no va a existir.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** `blastp` sobre una query de nucleótidos:
  - **Given** una secuencia query de nucleótidos (ADN o ARN), programa `blastp` seleccionado, y cualquier base de datos,
  - **When** el investigador presiona "Ejecutar búsqueda",
  - **Then** el sistema no invoca a BLAST+, corta el flujo del CU y muestra el mensaje "El programa `blastp` espera queries de proteína. Para su query de nucleótidos, opciones válidas son: `blastn` (contra base de nucleótidos), `blastx` o `tblastx`".

- **CA-02.** `blastn` contra una base de datos de proteínas:
  - **Given** una secuencia query de nucleótidos, programa `blastn` seleccionado, y una base de datos de proteínas seleccionada,
  - **When** el investigador presiona "Ejecutar búsqueda",
  - **Then** el sistema no invoca a BLAST+, corta el flujo del CU y muestra el mensaje "El programa `blastn` requiere base de datos de nucleótidos. Elija otra base de datos, o cambie el programa a `blastx`".

---

### HU08_CU001_E4 · Manejo de fallo del modo remoto de BLAST+

- **Deriva de:** `CU001`, slice `E4` (terminación abrupta durante el slice `B2`)
- **Realiza:** RF-07

> **Como** investigador/a,
> **quiero** que cuando la búsqueda remota falla el sistema me muestre el error tal como lo devolvió BLAST+ (o NCBI a través de BLAST+),
> **para** poder distinguir un problema de red temporal de un problema más grave y decidir si vale la pena reintentar más tarde.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Timeout de comunicación con NCBI:
  - **Given** una búsqueda en modo remoto en ejecución y la API remota de NCBI que no responde dentro del tiempo esperado,
  - **When** BLAST+ reporta timeout de comunicación,
  - **Then** el sistema corta el flujo del CU, no persiste nada en D2 y muestra el mensaje de error de BLAST+, aclarando explícitamente que se trata de un timeout de la conexión remota y no de un problema con los parámetros de la búsqueda.

- **CA-02.** Error explícito devuelto por NCBI:
  - **Given** una búsqueda en modo remoto que BLAST+ envió a NCBI,
  - **When** NCBI responde con un error explícito (rate limit, query rejected, u otro) que BLAST+ propaga al sistema,
  - **Then** el sistema corta el flujo del CU, no persiste nada en D2 y muestra el error literal que devolvió BLAST+, incluyendo el mensaje original de NCBI, sin traducirlo ni reinterpretarlo.

---

## HU derivadas de CU002 · Refinar los resultados con filtros post-búsqueda

### HU09_CU002_B · Refinar la vista con filtros post-búsqueda

- **Deriva de:** `CU002`, slice `B` (único slice básico; el camino feliz no se subdivide)
- **Realiza:** RF-09

> **Como** investigador/a,
> **quiero** aplicar filtros post-búsqueda sobre la tabla de resultados y verla refrescada en el momento, sin correr BLAST otra vez,
> **para** poder explorar interactivamente los alineamientos con distintos criterios y quedarme mirando el subconjunto relevante, aunque no llegue a descargar nada.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Filtrado interactivo sin re-ejecución de BLAST:
  - **Given** una tabla de resultados con al menos 20 alineamientos y filtros post-búsqueda establecidos en identidad ≥ 80% y cobertura ≥ 50%,
  - **When** el investigador confirma los filtros,
  - **Then** la tabla se re-filtra en el momento mostrando solo los hits que cumplen ambos umbrales, sin volver a invocar a BLAST+.

- **CA-02.** Ajuste sucesivo de filtros no re-ejecuta BLAST:
  - **Given** una tabla ya filtrada por identidad ≥ 80%,
  - **When** el investigador afloja el umbral a identidad ≥ 60% y agrega cobertura ≥ 70%,
  - **Then** la tabla se re-filtra sobre el conjunto crudo original (no sobre el resultado del filtro anterior) y aparecen los hits que cumplen los nuevos umbrales, sin ninguna invocación adicional a BLAST+.

- **CA-03.** Filtros no modifican el historial:
  - **Given** una búsqueda ya persistida en D2 al terminar su ejecución (postcondición de `CU001_B2`),
  - **When** el investigador aplica cualquier combinación de filtros post-búsqueda,
  - **Then** la entrada en D2 no se modifica: sigue conteniendo el conjunto **crudo** completo de resultados, para que en el futuro se pueda volver a esa búsqueda y probar filtros distintos.

---

## HU derivadas de CU003 · Descargar los resultados en un formato

### HU10_CU003_B · Descargar los alineamientos actualmente visibles en un formato

- **Deriva de:** `CU003`, slice `B` (único slice básico; el camino feliz no se subdivide)
- **Realiza:** RF-10

> **Como** investigador/a,
> **quiero** descargar los alineamientos que estoy viendo en la tabla —filtrados o no— en el formato que necesite,
> **para** llevarme el archivo tal cual quedó configurada la vista y seguir procesándolo por fuera del sistema.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Descarga en el formato elegido, sobre resultados sin filtrar:
  - **Given** una tabla de resultados sin filtros post-búsqueda aplicados (postcondición directa de `CU001_B2`),
  - **When** el investigador selecciona formato "CSV" y presiona "Descargar",
  - **Then** el sistema entrega un archivo `.csv` con la totalidad de los alineamientos crudos, con una fila de encabezados que incluye al menos las columnas mínimas (identificador, score, E-value observado, % identidad, % cobertura), y una sección de metadatos con los parámetros pre-búsqueda, la base de datos y el timestamp.

- **CA-02.** Descarga en el formato elegido, sobre resultados filtrados:
  - **Given** una tabla de resultados con filtros post-búsqueda aplicados (postcondición de `CU002_B`),
  - **When** el investigador selecciona formato "CSV" y presiona "Descargar",
  - **Then** el sistema entrega un archivo `.csv` que contiene únicamente los hits que superan los filtros vigentes al momento de la descarga, con la fila de encabezados y la sección de metadatos donde figuran también los filtros post-búsqueda aplicados.

- **CA-03.** La descarga no modifica el historial:
  - **Given** una búsqueda ya persistida en D2 (postcondición de `CU001_B2`),
  - **When** el investigador descarga los resultados (con o sin filtros aplicados),
  - **Then** la entrada en D2 no se modifica ni se duplica: sigue conteniendo el conjunto crudo de resultados original, con el timestamp de la ejecución (no el de la descarga).

---

### HU11_CU003_A1 · Descarga cuando ningún resultado supera los filtros

- **Deriva de:** `CU003`, slice `A1` (camino alternativo dentro del slice `B`)
- **Realiza:** RF-10

> **Como** investigador/a,
> **quiero** poder descargar el archivo aunque los filtros post-búsqueda dejen la tabla vacía,
> **para** tener constancia del intento y de los criterios que apliqué, aun cuando ningún hit los haya superado.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Descarga con tabla vacía:
  - **Given** una tabla de resultados con filtros post-búsqueda que dejan cero hits visibles (por ejemplo identidad ≥ 99% sobre una búsqueda de similitud lejana),
  - **When** el investigador selecciona formato "CSV" y presiona "Descargar",
  - **Then** el sistema entrega un archivo `.csv` con la fila de encabezados y una sección de metadatos de la búsqueda (parámetros pre-búsqueda, base de datos, timestamp, filtros post-búsqueda aplicados), pero **sin** filas de hits.

- **CA-02.** El historial mantiene los resultados crudos aunque la descarga sea vacía:
  - **Given** una búsqueda cuya descarga se hizo con filtros que dejaron cero hits visibles,
  - **When** el sistema termina de entregar el archivo,
  - **Then** la entrada en D2 permanece igual que antes: contiene el conjunto **completo** de resultados crudos que devolvió BLAST+ (persistido en `CU001_B2`), no la lista vacía que quedó tras el filtro, de forma que el investigador pueda volver más tarde y probar filtros distintos sin re-ejecutar BLAST.
    
---

## Tabla de trazabilidad completa `RF → CU → slice → HU`

| RF | CU | Slice | HU |
|---|---|---|---|
| RF-01, RF-02, RF-03, RF-04, RF-05, RF-06 | CU001 | CU001_B1 | **HU01_CU001_B1** |
| RF-07, RF-08, RF-11 | CU001 | CU001_B2 | **HU02_CU001_B2** |
| RF-07 | CU001 | CU001_A1 (cancelación manual) | **HU03_CU001_A1** |
| RF-03 | CU001 | CU001_A2 (BD local no disponible) | **HU04_CU001_A2** |
| RF-06 | CU001 | CU001_E1 (secuencia inválida) | **HU05_CU001_E1** |
| RF-04, RF-06 | CU001 | CU001_E2 (parámetros fuera de rango) | **HU06_CU001_E2** |
| RF-05 | CU001 | CU001_E3 (combinación incompatible) | **HU07_CU001_E3** |
| RF-07 | CU001 | CU001_E4 (fallo modo remoto) | **HU08_CU001_E4** |
| RF-09 | CU002 | CU002_B | **HU09_CU002_B** |
| RF-10 | CU003 | CU003_B | **HU10_CU003_B** |
| RF-10 | CU003 | CU003_A1 (resultado vacío) | **HU11_CU003_A1** |

## Notas sobre el enfoque de este TP

- **Un CU puede implementar varios RF**, y viceversa un mismo RF puede estar realizado por varios slices del mismo CU — por ejemplo RF-06 (validación pre-ejecución) aparece en el slice `B1` de `CU001` cuando la validación pasa y también en los slices `E1` y `E2` cuando falla y corta el flujo. La trazabilidad refleja esa realidad.
- **La unidad mínima de sprint es la HU**, no el CU ni el slice. Por eso las HU tienen un identificador propio (`HU01`, `HU02`, …) además del sufijo de trazabilidad — para que la planificación de sprints pueda referirse a ellas sin ambigüedad.
