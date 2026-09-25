# Historias de Usuario — LocalBlast

Cada historia de usuario detalla **un slice puntual** de un caso de uso (relación 1:1). El identificador de la HU conserva explícitamente el del slice de origen, para que la trazabilidad sea directa: la HU llamada `HU01_CU001_B` detalla el slice básico `B` del caso de uso `CU001`; la HU `HU13_CU007_B` detalla el (único) slice básico `B` del caso de uso `CU007`.

Formato de cada HU:

- **Deriva de**: qué CU y qué slice detalla.
- **Realiza**: qué RF materializa este slice (heredados del CU y del slice de origen).
- **Rol – meta – motivo**: "Como … quiero … para …".
- **Criterios de aceptación**: en formato **Given-When-Then**, trazables a la precondición y postcondición del slice.

Para el TP1 se detallan las HU de **todos los slices identificados en los casos de uso** — los siete básicos (`CU001_B`, `CU002_B`, `CU003_B`, `CU004_B`, `CU005_B`, `CU006_B`, `CU007_B`), las tres alternativas (`CU002_A1`, `CU004_A1`, `CU007_A1`) y las cuatro excepciones (`CU001_E1`, `CU003_E1`, `CU003_E2`, `CU004_E1`). En total, 14 historias de usuario.

**Numeración:** las HU se enumeran de forma consecutiva por CU y, dentro de cada CU, en el orden: slice básico (`B`) → slices alternativos (`A1`, `A2`, …) → slices de excepción (`E1`, `E2`, …). Así los identificadores acompañan el orden en el que aparecen los slices en [`casos-de-uso.md`](casos-de-uso.md).

---

## HU derivadas de CU001 · Cargar la secuencia query

### HU01_CU001_B · Cargar la secuencia query y chequear su formato

- **Deriva de:** `CU001`, slice `B` (pasos 1-2 del camino feliz)
- **Realiza:** RF-01, RF-02

> **Como** investigador/a,
> **quiero** subir un archivo FASTA o pegar la secuencia como texto y que el sistema la deje disponible con su alfabeto inferido,
> **para** poder reutilizar la misma secuencia en distintas configuraciones de búsqueda sin tener que cargarla de nuevo.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Carga de secuencia FASTA de proteína desde archivo:
  - **Given** un archivo `.fasta` bien formado con un único registro de secuencia de aminoácidos válidos,
  - **When** el investigador lo sube desde el formulario,
  - **Then** el sistema deja la secuencia disponible en la sesión, muestra el alfabeto inferido "proteína" y habilita los controles del `CU002` para configurar la búsqueda.

- **CA-02.** Carga de secuencia pegada como texto plano:
  - **Given** una secuencia de ADN pegada en el textarea del formulario, sin encabezado FASTA,
  - **When** el investigador confirma la carga,
  - **Then** el sistema la acepta como secuencia plana, infiere alfabeto "ADN" y la deja disponible para `CU002`.

- **CA-03.** Reutilización de la secuencia cargada:
  - **Given** una secuencia ya cargada en la sesión con la que el investigador ya lanzó una búsqueda,
  - **When** el investigador vuelve al formulario para armar otra configuración distinta,
  - **Then** la secuencia sigue disponible sin necesidad de volver a cargarla, y solo se reinicia el resto del formulario.

---

### HU02_CU001_E1 · Rechazo de secuencia query con formato inválido

- **Deriva de:** `CU001`, slice `E1` (terminación abrupta detectada en el paso 2)
- **Realiza:** RF-02

> **Como** investigador/a,
> **quiero** recibir un mensaje claro cuando la secuencia que subo o pego no es reconocible,
> **para** poder corregirla de inmediato sin tener que adivinar qué le pasa.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Caracter fuera del alfabeto:
  - **Given** un texto pegado como query que contiene al menos un carácter fuera del alfabeto de ADN, ARN o proteína (por ejemplo un dígito o un símbolo de puntuación),
  - **When** el investigador confirma la carga,
  - **Then** el sistema no marca la secuencia como cargada, no habilita los controles del `CU002` y muestra un mensaje que indica cuál es el carácter inválido y en qué posición aparece.

- **CA-02.** FASTA con encabezado sin cuerpo:
  - **Given** un archivo FASTA con una línea de encabezado (`>ID`) pero sin ninguna línea de secuencia debajo,
  - **When** el investigador lo sube,
  - **Then** el sistema no marca la secuencia como cargada, no habilita los controles del `CU002` y muestra el mensaje "El FASTA contiene un encabezado pero ninguna secuencia asociada".

---

## HU derivadas de CU002 · Configurar los parámetros de la búsqueda

### HU03_CU002_B · Configurar modo, base de datos, programa y parámetros pre-búsqueda

- **Deriva de:** `CU002`, slice `B` (pasos 1-4 del camino feliz)
- **Realiza:** RF-03, RF-04, RF-05, RF-06

> **Como** investigador/a,
> **quiero** elegir el modo (local o remoto), la base de datos, el programa BLAST y los parámetros pre-búsqueda sobre la secuencia que ya cargué,
> **para** dejar el formulario listo para pedirle al sistema que lo valide.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Configuración completa en modo remoto:
  - **Given** una secuencia de proteína ya cargada en la sesión (postcondición de `CU001`),
  - **When** el investigador elige modo remoto, base de datos `nr`, programa `blastp` y deja los parámetros en su valor por defecto,
  - **Then** el formulario queda completo y el sistema habilita el botón "Validar búsqueda" que dispara `CU003`.

- **CA-02.** Valores por defecto sensatos según el programa:
  - **Given** un formulario donde el investigador acaba de seleccionar el programa `blastp`,
  - **When** la interfaz carga los parámetros pre-búsqueda,
  - **Then** los campos de E-value máximo, matriz de sustitución, tamaño de palabra y penalización de gaps aparecen prellenados con los valores por defecto correspondientes al programa `blastp` (no los mismos que para `blastn`).

- **CA-03.** Base de datos coherente con el modo elegido:
  - **Given** el investigador cambia el modo de "remoto" a "local",
  - **When** el sistema recarga la lista de bases de datos disponibles,
  - **Then** la lista muestra únicamente las bases de datos del catálogo local (leídas de D1), sin las bases estándar de NCBI que aparecían en modo remoto.

---

### HU04_CU002_A1 · Manejo de base de datos local no disponible

- **Deriva de:** `CU002`, slice `A1` (camino alternativo en el paso 2)
- **Realiza:** RF-04

> **Como** investigador/a,
> **quiero** que el sistema me informe claramente cuando la base de datos local que elegí no está en condiciones de ser usada, y me devuelva la lista actualizada para que yo decida,
> **para** no quedarme trabado ni terminar corriendo contra una base equivocada porque el sistema me la sustituyó por su cuenta.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Base de datos en proceso de actualización:
  - **Given** modo local seleccionado y una base de datos del catálogo D1 que está en estado "actualizándose" porque P3 la está reconstruyendo en ese momento,
  - **When** el investigador la selecciona en el paso 2,
  - **Then** el sistema muestra el mensaje "La base de datos '\<nombre\>' está siendo actualizada y no puede usarse en este momento" y devuelve al investigador al paso 2 con la lista de bases locales actualizada, **sin** proponer un cambio automático a modo remoto.

- **CA-02.** Base de datos con índice en error:
  - **Given** modo local seleccionado y una base de datos cuyo índice quedó marcado como "con errores" tras un fallo previo de `makeblastdb`,
  - **When** el investigador la selecciona en el paso 2,
  - **Then** el sistema muestra un mensaje que explica que el índice está corrupto y sugiere contactar al administrador de bases de datos, y devuelve al investigador al paso 2.

---

## HU derivadas de CU003 · Validar la búsqueda

### HU05_CU003_B · Obtener el visto bueno del sistema sobre la búsqueda configurada

- **Deriva de:** `CU003`, slice `B` (pasos 1-2 del camino feliz)
- **Realiza:** RF-05, RF-06, RF-07

> **Como** investigador/a,
> **quiero** disparar la validación semántica de mi configuración y recibir el visto bueno explícito del sistema antes de comprometer tiempo de BLAST+,
> **para** no perder tiempo lanzando búsquedas mal configuradas.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Validación exitosa habilita el disparador de `CU004`:
  - **Given** una secuencia cargada (postcondición de `CU001`) y un formulario configurado con modo, BD, programa y parámetros compatibles (postcondición de `CU002`),
  - **When** el investigador presiona "Validar búsqueda",
  - **Then** el sistema chequea alfabeto vs. programa, rangos de parámetros y compatibilidad programa/query/BD, marca la configuración como "válida y lista para ejecutar" y habilita el botón "Ejecutar búsqueda" que dispara `CU004`.

- **CA-02.** Cambio posterior al formulario invalida la marca:
  - **Given** una configuración ya validada y marcada como ejecutable,
  - **When** el investigador cambia cualquier campo del formulario (por ejemplo el programa),
  - **Then** el sistema quita la marca de "válida", deshabilita el botón "Ejecutar búsqueda" y exige que el investigador vuelva a disparar `CU003` para re-validar la nueva combinación.

---

### HU06_CU003_E1 · Rechazo de parámetros pre-búsqueda fuera de rango

- **Deriva de:** `CU003`, slice `E1` (terminación abrupta detectada en el paso 2)
- **Realiza:** RF-06, RF-07

> **Como** investigador/a,
> **quiero** que el sistema me señale exactamente qué parámetro está fuera de rango y cuál es el rango válido para el programa BLAST que elegí,
> **para** poder corregirlo sin consultar la documentación de BLAST+ por afuera.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** E-value negativo:
  - **Given** un formulario completo con el campo "E-value máximo" en `-1`,
  - **When** el investigador presiona "Validar búsqueda",
  - **Then** el sistema corta el flujo del CU, no marca la búsqueda como válida y muestra un mensaje que señala el campo "E-value" e indica que debe ser un número positivo (típicamente entre 0 y 10).

- **CA-02.** Tamaño de palabra fuera del rango del programa:
  - **Given** un formulario con programa `blastn` seleccionado y "Tamaño de palabra" = 3 (por debajo del mínimo válido para `blastn`),
  - **When** el investigador presiona "Validar búsqueda",
  - **Then** el sistema corta el flujo del CU, no marca la búsqueda como válida y muestra un mensaje que señala el campo "Tamaño de palabra" e indica el rango válido para el programa `blastn`.

---

### HU07_CU003_E2 · Rechazo de combinación programa / query / base de datos incompatible

- **Deriva de:** `CU003`, slice `E2` (terminación abrupta detectada en el paso 2)
- **Realiza:** RF-05, RF-07

> **Como** investigador/a,
> **quiero** que el sistema me impida validar una combinación de programa BLAST y tipos de secuencia/base incompatibles, y me sugiera qué combinaciones sí funcionan con lo que ya cargué,
> **para** no perder tiempo esperando un resultado que no va a existir.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** `blastp` sobre una query de nucleótidos:
  - **Given** una secuencia query de nucleótidos (ADN o ARN), programa `blastp` seleccionado, y cualquier base de datos,
  - **When** el investigador presiona "Validar búsqueda",
  - **Then** el sistema corta el flujo del CU, no marca la búsqueda como válida y muestra el mensaje "El programa `blastp` espera queries de proteína. Para su query de nucleótidos, opciones válidas son: `blastn` (contra base de nucleótidos), `blastx` o `tblastx`".

- **CA-02.** `blastn` contra una base de datos de proteínas:
  - **Given** una secuencia query de nucleótidos, programa `blastn` seleccionado, y una base de datos de proteínas seleccionada,
  - **When** el investigador presiona "Validar búsqueda",
  - **Then** el sistema corta el flujo del CU, no marca la búsqueda como válida y muestra el mensaje "El programa `blastn` requiere base de datos de nucleótidos. Elija otra base de datos, o cambie el programa a `blastx`".

---

## HU derivadas de CU004 · Ejecutar la búsqueda

### HU08_CU004_B · Ejecutar la búsqueda validada de forma asíncrona

- **Deriva de:** `CU004`, slice `B` (pasos 1-3 del camino feliz)
- **Realiza:** RF-08

> **Como** investigador/a,
> **quiero** que el sistema invoque a BLAST+ en segundo plano sobre mi búsqueda validada, con indicador de progreso y opción de cancelar,
> **para** poder seguir trabajando en la aplicación mientras la búsqueda corre y decidir en cualquier momento si la abandono.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Ejecución asíncrona con indicador de progreso:
  - **Given** una búsqueda ya configurada y validada (postcondición de `CU003`),
  - **When** el investigador presiona "Ejecutar búsqueda" y el sistema invoca a BLAST+ en segundo plano,
  - **Then** la interfaz muestra un indicador de progreso visible y permanece navegable — el investigador puede desplazarse dentro de la aplicación sin que la ejecución se interrumpa.

- **CA-02.** Fin exitoso libera los resultados crudos para `CU005`:
  - **Given** una búsqueda en ejecución que BLAST+ termina exitosamente,
  - **When** el sistema recibe el conjunto crudo de alineamientos,
  - **Then** deja esos resultados disponibles en memoria de la sesión y dispara `CU005` para presentarlos y persistirlos.

---

### HU09_CU004_A1 · Cancelación manual de una búsqueda en curso

- **Deriva de:** `CU004`, slice `A1` (camino alternativo durante el paso 2)
- **Realiza:** RF-08

> **Como** investigador/a,
> **quiero** poder cancelar una búsqueda que está en ejecución,
> **para** dejar de esperar y no consumir recursos remotos ni locales cuando me di cuenta que configuré algo mal o el resultado ya dejó de importarme.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Cancelación de una búsqueda local:
  - **Given** una búsqueda en modo local que BLAST+ está ejecutando en el servidor (indicador de progreso visible),
  - **When** el investigador presiona "Cancelar",
  - **Then** el sistema aborta el subproceso local de BLAST+, deja la interfaz lista para configurar otra búsqueda desde cero, no dispara `CU005` y no persiste nada en D2.

- **CA-02.** Cancelación de una búsqueda remota:
  - **Given** una búsqueda en modo remoto que BLAST+ tramita contra NCBI (indicador de progreso visible),
  - **When** el investigador presiona "Cancelar",
  - **Then** el sistema cancela la solicitud a través de BLAST+, deja la interfaz lista para configurar otra búsqueda desde cero, no dispara `CU005` y no persiste nada en D2.

---

### HU10_CU004_E1 · Manejo de fallo del modo remoto de BLAST+

- **Deriva de:** `CU004`, slice `E1` (terminación abrupta durante el paso 2)
- **Realiza:** RF-08

> **Como** investigador/a,
> **quiero** que cuando la búsqueda remota falla el sistema me muestre el error tal como lo devolvió BLAST+ (o NCBI a través de BLAST+),
> **para** poder distinguir un problema de red temporal de un problema más grave y decidir si vale la pena reintentar más tarde.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Timeout de comunicación con NCBI:
  - **Given** una búsqueda en modo remoto en ejecución y la API remota de NCBI que no responde dentro del tiempo esperado,
  - **When** BLAST+ reporta timeout de comunicación,
  - **Then** el sistema corta el flujo del CU, no dispara `CU005`, no persiste nada en D2 y muestra el mensaje de error de BLAST+, aclarando explícitamente que se trata de un timeout de la conexión remota y no de un problema con los parámetros de la búsqueda.

- **CA-02.** Error explícito devuelto por NCBI:
  - **Given** una búsqueda en modo remoto que BLAST+ envió a NCBI,
  - **When** NCBI responde con un error explícito (rate limit, query rejected, u otro) que BLAST+ propaga al sistema,
  - **Then** el sistema corta el flujo del CU, no dispara `CU005`, no persiste nada en D2 y muestra el error literal que devolvió BLAST+, incluyendo el mensaje original de NCBI, sin traducirlo ni reinterpretarlo.

---

## HU derivadas de CU005 · Ver los resultados y persistir la búsqueda en el historial

### HU11_CU005_B · Presentar la tabla de alineamientos y guardar la búsqueda en el historial

- **Deriva de:** `CU005`, slice `B` (pasos 1-2 del camino feliz)
- **Realiza:** RF-09, RF-10

> **Como** investigador/a,
> **quiero** ver los alineamientos en una tabla dentro de la misma vista apenas termina la ejecución, y que el sistema guarde automáticamente la búsqueda en el historial,
> **para** no perder la búsqueda aunque no llegue a descargarla ni refinarla en esta sesión.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Presentación de la tabla al finalizar:
  - **Given** un conjunto crudo de alineamientos disponible en la sesión, entregado por una ejecución exitosa de `CU004`,
  - **When** el sistema toma el control tras esa ejecución,
  - **Then** presenta los resultados en una tabla con al menos las columnas: identificador del hit, score, E-value observado, porcentaje de identidad y porcentaje de cobertura.

- **CA-02.** Persistencia automática en el historial:
  - **Given** los mismos resultados crudos recién presentados en la tabla,
  - **When** el sistema termina de mostrarlos,
  - **Then** queda registrada en el historial (D2) una entrada con los parámetros pre-búsqueda, la base de datos usada, el timestamp y el conjunto **completo** de resultados crudos que devolvió BLAST+ (antes de cualquier filtro post-búsqueda) — sin que el investigador tenga que ejercer `CU006` ni `CU007` para que la persistencia ocurra.

---

## HU derivadas de CU006 · Refinar los resultados con filtros post-búsqueda

### HU12_CU006_B · Refinar la vista con filtros post-búsqueda

- **Deriva de:** `CU006`, slice `B` (único slice básico; el camino feliz no se subdivide)
- **Realiza:** RF-11

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
  - **Given** una búsqueda ya persistida en D2 al terminar su ejecución (postcondición de `CU005_B`),
  - **When** el investigador aplica cualquier combinación de filtros post-búsqueda,
  - **Then** la entrada en D2 no se modifica: sigue conteniendo el conjunto **crudo** completo de resultados, para que en el futuro se pueda volver a esa búsqueda y probar filtros distintos.

---

## HU derivadas de CU007 · Descargar los resultados en un formato

### HU13_CU007_B · Descargar los alineamientos actualmente visibles en un formato

- **Deriva de:** `CU007`, slice `B` (único slice básico; el camino feliz no se subdivide)
- **Realiza:** RF-12

> **Como** investigador/a,
> **quiero** descargar los alineamientos que estoy viendo en la tabla —filtrados o no— en el formato que necesite,
> **para** llevarme el archivo tal cual quedó configurada la vista y seguir procesándolo por fuera del sistema.

**Criterios de aceptación (Given-When-Then)**

- **CA-01.** Descarga en el formato elegido, sobre resultados sin filtrar:
  - **Given** una tabla de resultados sin filtros post-búsqueda aplicados (postcondición directa de `CU005_B`),
  - **When** el investigador selecciona formato "CSV" y presiona "Descargar",
  - **Then** el sistema entrega un archivo `.csv` con la totalidad de los alineamientos crudos, con una fila de encabezados que incluye al menos las columnas mínimas (identificador, score, E-value observado, % identidad, % cobertura), y una sección de metadatos con los parámetros pre-búsqueda, la base de datos y el timestamp.

- **CA-02.** Descarga en el formato elegido, sobre resultados filtrados:
  - **Given** una tabla de resultados con filtros post-búsqueda aplicados (postcondición de `CU006_B`),
  - **When** el investigador selecciona formato "CSV" y presiona "Descargar",
  - **Then** el sistema entrega un archivo `.csv` que contiene únicamente los hits que superan los filtros vigentes al momento de la descarga, con la fila de encabezados y la sección de metadatos donde figuran también los filtros post-búsqueda aplicados.

- **CA-03.** La descarga no modifica el historial:
  - **Given** una búsqueda ya persistida en D2 (postcondición de `CU005_B`),
  - **When** el investigador descarga los resultados (con o sin filtros aplicados),
  - **Then** la entrada en D2 no se modifica ni se duplica: sigue conteniendo el conjunto crudo de resultados original, con el timestamp de la ejecución (no el de la descarga).

---

### HU14_CU007_A1 · Descarga cuando ningún resultado supera los filtros

- **Deriva de:** `CU007`, slice `A1` (camino alternativo dentro del slice `B`)
- **Realiza:** RF-12

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
  - **Then** la entrada en D2 permanece igual que antes: contiene el conjunto **completo** de resultados crudos que devolvió BLAST+ (persistido en `CU005_B`), no la lista vacía que quedó tras el filtro, de forma que el investigador pueda volver más tarde y probar filtros distintos sin re-ejecutar BLAST.

---

## Tabla de trazabilidad completa `RF → CU → slice → HU`

| RF | CU | Slice | HU |
|---|---|---|---|
| RF-01, RF-02 | CU001 | CU001_B | **HU01_CU001_B** |
| RF-02 | CU001 | CU001_E1 (secuencia inválida) | **HU02_CU001_E1** |
| RF-03, RF-04, RF-05, RF-06 | CU002 | CU002_B | **HU03_CU002_B** |
| RF-04 | CU002 | CU002_A1 (BD local no disponible) | **HU04_CU002_A1** |
| RF-05, RF-06, RF-07 | CU003 | CU003_B | **HU05_CU003_B** |
| RF-06, RF-07 | CU003 | CU003_E1 (parámetros fuera de rango) | **HU06_CU003_E1** |
| RF-05, RF-07 | CU003 | CU003_E2 (combinación incompatible) | **HU07_CU003_E2** |
| RF-08 | CU004 | CU004_B | **HU08_CU004_B** |
| RF-08 | CU004 | CU004_A1 (cancelación manual) | **HU09_CU004_A1** |
| RF-08 | CU004 | CU004_E1 (fallo modo remoto) | **HU10_CU004_E1** |
| RF-09, RF-10 | CU005 | CU005_B | **HU11_CU005_B** |
| RF-11 | CU006 | CU006_B | **HU12_CU006_B** |
| RF-12 | CU007 | CU007_B | **HU13_CU007_B** |
| RF-12 | CU007 | CU007_A1 (resultado vacío) | **HU14_CU007_A1** |

## Notas sobre el enfoque de este TP

- **Un CU puede implementar varios RF**, y viceversa un mismo RF puede estar realizado por varios slices del mismo CU. Por ejemplo RF-07 (validación semántica) aparece en el camino feliz `CU003_B` cuando la validación pasa, y también en `CU003_E1` y `CU003_E2` cuando falla y corta el flujo. Esa dispersión es esperable: los slices de excepción son otra forma en que se cumple el RF.
- **La validación tiene dos RFs distintos, no uno solo con dos facetas.** RF-02 cubre la validación sintáctica del formato del FASTA (al cargar la secuencia, cae en `CU001`) y RF-07 cubre la validación semántica de coherencia entre secuencia, programa, base de datos y parámetros (al pedir el visto bueno, cae en `CU003`). Son RFs emparentados conceptualmente pero se disparan en momentos distintos del flujo y con criterios de aceptación distintos, por eso los tenemos separados (ver Entrada 12 de la bitácora de IA).
- **La unidad mínima de sprint es la HU**, no el CU ni el slice. Por eso las HU tienen un identificador propio (`HU01`, `HU02`, …) además del sufijo de trazabilidad — para que la planificación de sprints pueda referirse a ellas sin ambigüedad.
