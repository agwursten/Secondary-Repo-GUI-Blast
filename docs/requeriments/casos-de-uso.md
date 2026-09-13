# Casos de Uso — LocalBlast

Los casos de uso se redactan en **formato textual estructurado (Cockburn)** — actor, objetivo, precondición, flujo principal, alternativos, excepciones, postcondición — según pide el TP1, y **no** como diagrama gráfico (Mermaid no incluye un tipo de diagrama de casos de uso nativo).

Todos los casos de uso de este documento derivan del proceso profundizado **P1 · Ejecutar búsqueda BLAST** del DFD Nivel 1. Los procesos P2 y P3 quedan documentados a nivel de alcance en el DFD y en el modelo de dominio, pero **no** tienen casos de uso propios en este TP (ver justificación en la sección 5 del [SRS](srs.md#5-selección-de-procesos-a-profundizar)).

Cada caso de uso declara qué requerimientos funcionales realiza. La cadena completa de trazabilidad es:

**RF → CU → slice → HU**

## Enfoque de los casos de uso — qué es un CU y qué no

Un caso de uso representa **una capacidad discreta que el sistema le brinda al actor** — un objetivo alcanzable —, no un trazo secuencial de pasos que el actor tiene que recorrer de punta a punta. Dos consecuencias prácticas de esa definición para este TP:

- **Del proceso P1 salen tres CU, no uno solo largo.** El investigador tiene tres objetivos distintos que el sistema le habilita, y que puede combinar como necesite:
  - `CU001` (ejecutar una búsqueda) — obtener alineamientos crudos visibles en la interfaz.
  - `CU002` (refinar con filtros post-búsqueda) — ver los alineamientos con criterios post-búsqueda aplicados, sin volver a correr BLAST.
  - `CU003` (descargar) — obtener un archivo con los alineamientos actualmente visibles, en un formato.
- **La descarga no siempre se ejerce.** A veces el investigador solo quiere mirar los resultados filtrados en pantalla (queda en `CU002`) y no descargarlos. A veces querrá descargar sin haber filtrado (directamente `CU003` sobre los crudos). Y, cuando D2 se profundice como fuente de lectura en una versión futura, el investigador podrá iniciar `CU003` sobre una búsqueda vieja del historial sin volver a ejecutar `CU001`. Ese abanico de combinaciones es lo que justifica tener CU separados por capacidad y no uno solo secuencial.
- **Cuando el camino feliz de un CU queda largo, se descompone en slices.** No los CU en sí, sino su flujo principal. Los slices son módulos que aportan valor por sí mismos hacia el objetivo del CU. En este TP, `CU001` se descompone en dos slices básicos (`B1` y `B2`); `CU002` y `CU003` quedan cada uno con un único slice básico (`B`) porque sus flujos son cortos.

## Convención de identificadores y trazabilidad

**Cadena de trazabilidad:** `RF → CU → slice → HU`.

- Un **CU** puede realizar uno o varios RF, y a la inversa un RF puede estar realizado por varios slices del mismo CU (por ejemplo la validación previa aparece tanto en el camino feliz como en los slices de excepción).
- El identificador del **slice básico** es la letra `B` (`CU00X_B`); si además se subdivide, pasa a `B1`, `B2`, … Los **slices alternativos** se numeran `A1`, `A2`, … y los **de excepción** `E1`, `E2`, …
- La relación **slice ↔ HU es 1:1**. La HU conserva el identificador de trazabilidad del slice: `HU01_CU001_B1` detalla el slice `CU001_B1`; `HU10_CU003_B` detalla el (único) slice básico de `CU003`.
- Los once slices identificados en los tres CU tienen **cada uno** su HU detallada en [`historias-usuario.md`](historias-usuario.md), con criterios Given-When-Then. El grupo decidió detallarlos a todos ya (en lugar de dejar algunos "nombrados sin detallar", que sería la opción mínima de la guía) porque el modelo de ciclo de vida es ágil y la HU es la unidad mínima de sprint — la explicación completa está al comienzo del `historias-usuario.md`.

---

## CU001 · Ejecutar una búsqueda BLAST

- **Actor principal:** Investigador/a
- **Actor secundario:** Motor **BLAST+** (invocado por el sistema en ambos modos: local, y remoto con la flag `-remote` — es BLAST+ el que se comunica con NCBI del otro lado, nunca directamente nuestra GUI)
- **Objetivo:** Obtener un conjunto de alineamientos de una secuencia query contra una base de datos elegida, con parámetros del algoritmo bajo control del usuario, verlos en la interfaz, y que la búsqueda quede persistida en el historial para uso posterior.
- **Realiza:** RF-01, RF-02, RF-03, RF-04, RF-05, RF-06, RF-07, RF-08, RF-11
- **Precondición:** Existe al menos una base de datos disponible (local, con su entrada en D1, o remota entre las que ofrece NCBI). El investigador accedió a la interfaz web.
- **Disparador:** El investigador decide iniciar una nueva búsqueda BLAST.
- **Garantía de éxito:** El investigador ve la tabla de alineamientos correspondiente a su búsqueda en la interfaz, y la búsqueda (con sus resultados crudos) queda persistida en D2. Esos resultados quedan disponibles en la sesión para que el investigador los procese después con `CU002` (refinar) o `CU003` (descargar), si así lo decide.
- **Garantía mínima:** El sistema nunca invoca a BLAST+ con datos que no pasaron validación, ni deja búsquedas parcialmente ejecutadas consumiendo recursos indefinidamente.

### Flujo principal

1. El investigador ingresa la **secuencia query** subiendo un archivo FASTA desde su equipo o pegando la secuencia como texto en el formulario.
2. El investigador elige el **modo de ejecución**: local o remoto (NCBI). La interfaz muestra una única opción alternativa, para que la decisión sea clara.
3. El investigador selecciona la **base de datos** de una lista: si eligió modo local, aparecen las bases de datos del catálogo del laboratorio (leídas de D1); si eligió modo remoto, las bases estándar de NCBI.
4. El investigador elige el **programa BLAST** a ejecutar (`blastn`, `blastp`, `blastx`, `tblastn`, `tblastx`).
5. El investigador ajusta los **parámetros pre-búsqueda** (E-value máximo, matriz de sustitución, tamaño de palabra, penalización de gaps). La interfaz ofrece valores por defecto sensatos según el programa.
6. El investigador presiona **Ejecutar búsqueda**.
7. El sistema **valida** que la secuencia sea reconocible como ADN, ARN o proteína, que los parámetros estén dentro de rangos lógicos, y que la combinación de programa BLAST elegido, tipo de la secuencia query y tipo de la base de datos seleccionada sea **compatible** (por ejemplo, no dejar correr `blastp` sobre una secuencia de nucleótidos).
8. El sistema **invoca a BLAST+** en segundo plano con la combinación de opciones armada a partir del formulario (programa, ruta de la base de datos, query, parámetros pre-búsqueda, y la flag `-remote` cuando el modo elegido es remoto), y muestra un indicador de progreso sin bloquear la interfaz. La comunicación con NCBI, cuando corresponde, la realiza BLAST+ internamente por la flag `-remote`; el sistema solo espera su respuesta.
9. Cuando termina, el sistema muestra la **lista de alineamientos** (hits) en una tabla, con columnas mínimas: identificador del hit, score, E-value observado, % identidad, % cobertura, y **persiste la búsqueda con sus resultados crudos en D2** (parámetros pre-búsqueda, base de datos usada, timestamp y lista completa de alineamientos antes de cualquier filtro).

**Postcondición:** El investigador ve la tabla de alineamientos de su búsqueda en la interfaz, y la búsqueda queda persistida en D2. Los resultados quedan disponibles en la sesión para que el investigador los use en `CU002` (refinar) o `CU003` (descargar) si así lo decide.

### Descomposición en slices

El camino feliz de 9 pasos está en el borde de "largo" y tiene dos módulos con valor propio: dejar una búsqueda configurada y validada (valor: el investigador sabe que su búsqueda es lanzable), y ejecutar, presentar y persistir los resultados (valor: el investigador ve los hits y queda registro de la búsqueda). Se divide en dos slices básicos, más los alternativos y de excepción que se explican debajo.

```
CU001 · Ejecutar una búsqueda BLAST
├─ Camino feliz (slices básicos)
│  ├─ CU001_B1  — pasos 1-7:  cargar, configurar y validar la búsqueda
│  └─ CU001_B2  — pasos 8-9:  ejecutar la búsqueda, presentar resultados y persistir en D2
├─ Caminos alternativos (slices A)
│  ├─ CU001_A1  — cancelación manual de la búsqueda en curso
│  └─ CU001_A2  — base de datos local no disponible
└─ Terminaciones abruptas (slices E)
   ├─ CU001_E1  — secuencia query con formato inválido
   ├─ CU001_E2  — parámetros pre-búsqueda fuera de rango
   ├─ CU001_E3  — combinación programa / query / base de datos incompatible
   └─ CU001_E4  — fallo del modo remoto de BLAST+
```

### Slices básicos — descripción

- **`CU001_B1` · Cargar, configurar y validar la búsqueda (pasos 1-7).** El investigador ingresa la secuencia query, elige el modo (local o remoto), la base de datos, el programa BLAST y los parámetros pre-búsqueda; al presionar **Ejecutar búsqueda**, el sistema valida el alfabeto de la secuencia, los rangos de los parámetros y la compatibilidad entre programa/query/base de datos. **Valor entregado:** una búsqueda queda configurada y validada, lista para ser ejecutada. **Realiza:** RF-01, RF-02, RF-03, RF-04, RF-05, RF-06.
- **`CU001_B2` · Ejecutar la búsqueda, presentar resultados y persistir (pasos 8-9).** El sistema invoca a BLAST+ con la configuración ya validada, muestra un indicador de progreso sin bloquear la interfaz y, al terminar, presenta la tabla de alineamientos con las columnas mínimas y persiste la búsqueda + resultados crudos en D2. **Valor entregado:** el investigador ve los alineamientos que BLAST+ devolvió, y la búsqueda queda registrada para uso posterior aunque el investigador nunca ejerza `CU002` ni `CU003`. **Realiza:** RF-07, RF-08, RF-11.

### Slices alternativos — descripción

Son caminos válidos alternativos al flujo principal; el sistema sigue funcionando y el CU puede alcanzar (o no) el objetivo por otra ruta.

- **`CU001_A1` · Cancelación manual de la búsqueda.** Mientras la búsqueda está en ejecución (durante `CU001_B2`), el investigador presiona **Cancelar**. El sistema aborta el subproceso local o cancela la solicitud remota a través de BLAST+, y deja la interfaz lista para iniciar una nueva búsqueda. La postcondición del CU no se alcanza; es una decisión explícita del actor de abandonar el objetivo actual. Al no haber ejecución exitosa, tampoco hay persistencia en D2. **Realiza:** RF-07.
- **`CU001_A2` · Base de datos local no disponible.** En el paso 3, el investigador seleccionó modo local y una base de datos que en ese momento no está lista en D1 (por ejemplo, se está actualizando desde P3, o su índice quedó marcado con error). El sistema informa el estado de esa base de datos y su motivo, y devuelve al investigador al paso 3 con la lista de bases de datos locales actualizada. El investigador decide por su cuenta qué hacer a continuación (elegir otra base local, cambiar de modo, o cancelar); el sistema **no** propone equivalencias entre bases locales y remotas, porque no las hay: una base propia del laboratorio no es intercambiable con las bases estándar de NCBI. **Realiza:** RF-03.


### Slices de excepción — descripción

Son terminaciones abruptas del flujo: el sistema detecta una condición que impide continuar, corta la ejecución del CU y notifica al investigador. La postcondición del CU no se alcanza y, al no haber ejecución exitosa, tampoco hay persistencia en D2.

- **`CU001_E1` · Secuencia query con formato inválido.** En el paso 7, la validación detecta que la secuencia ingresada no tiene formato reconocible (caracteres fuera del alfabeto de ADN/ARN/proteína, FASTA mal formado, encabezado sin cuerpo, longitud fuera de rango). El sistema no invoca a BLAST+, corta el flujo y muestra un mensaje que indica exactamente el problema y dónde aparece. **Realiza:** RF-06.
- **`CU001_E2` · Parámetros pre-búsqueda fuera de rango.** En el paso 7, la validación detecta al menos un parámetro con valor imposible (E-value negativo, tamaño de palabra fuera del rango soportado, penalización de gap fuera de escala). El sistema corta el flujo y señala qué campo corregir y cuál es el rango esperado. **Realiza:** RF-04, RF-06.
- **`CU001_E3` · Combinación programa / query / base de datos incompatible.** En el paso 7, la verificación de compatibilidad detecta que el programa BLAST elegido no coincide con el tipo de la secuencia query o con el tipo de la base de datos (por ejemplo `blastp` con query de nucleótidos, o `blastn` contra una base de datos de proteínas). El sistema corta el flujo, indica el motivo y sugiere qué combinaciones sí son válidas para lo que el usuario ya cargó. **Realiza:** RF-05.
- **`CU001_E4` · Fallo del modo remoto de BLAST+.** En el paso 8, con modo remoto seleccionado, BLAST+ reporta un error de comunicación con NCBI (sin respuesta, timeout, o error explícito devuelto por la API). El sistema captura el error, corta el flujo del CU e informa al investigador con el detalle recibido. Un reintento posterior es un CU nuevo, no la continuación de este. **Realiza:** RF-07.

---

## CU002 · Refinar los resultados con filtros post-búsqueda

- **Actor principal:** Investigador/a
- **Objetivo:** Ver la lista de alineamientos filtrada por criterios post-búsqueda (identidad, cobertura, E-value observado, taxonomía), sin re-ejecutar BLAST.
- **Realiza:** RF-09
- **Precondición:** Existe una búsqueda con resultados visibles en la interfaz (postcondición de `CU001`). En una versión futura del sistema, cuando D2 sea legible desde la interfaz, esos resultados también podrán provenir del historial sin haber ejecutado `CU001` en la sesión actual.
- **Disparador:** El investigador quiere restringir la vista a un subconjunto de los alineamientos según criterios post-búsqueda.
- **Garantía de éxito:** La tabla muestra los alineamientos que superan los criterios elegidos. No se ejecuta BLAST+ ni se persiste nada nuevo en D2 (la búsqueda ya quedó registrada en `CU001` con sus resultados crudos).
- **Garantía mínima:** La tabla filtrada nunca "inventa" hits que no estaban en el conjunto crudo; los filtros son estrictamente restrictivos sobre el conjunto ya calculado.

### Flujo principal

1. El investigador ajusta los **filtros post-búsqueda** (umbrales de identidad, cobertura, E-value observado; filtro por taxonomía cuando la información esté disponible).
2. El sistema re-filtra la tabla en el momento, mostrando únicamente los hits que superan todos los umbrales fijados, **sin volver a invocar a BLAST+**.

**Postcondición:** La tabla de resultados visible en la interfaz refleja los filtros post-búsqueda actuales. Los resultados crudos originales siguen intactos en la sesión (y en D2), disponibles para probar otros filtros o para descargar sin filtrar.

### Por qué este CU no se subdivide en slices

`CU002` es corto (2 pasos) y no tiene módulos internos con valor separado: ajustar filtros sin ver la tabla re-filtrada no aporta nada, y la re-filtración sin el ajuste previo no tiene sentido. El slice básico es entonces uno solo, identificado como `CU002_B`. Tampoco tiene alternativas ni excepciones dignas de nota: el caso "el filtro deja la tabla vacía" no interrumpe el CU (la tabla vacía es un resultado válido del filtro); es un problema recién si el investigador intenta descargar esa tabla vacía, y por eso ese caso vive en `CU003_A1`.

### Slices del CU

```
CU002 · Refinar los resultados con filtros post-búsqueda
└─ Camino feliz
   └─ CU002_B   — pasos 1-2:  ajustar filtros post-búsqueda y ver la tabla re-filtrada
```

---

## CU003 · Descargar los resultados en un formato

- **Actor principal:** Investigador/a
- **Objetivo:** Obtener, en su equipo, un archivo con los alineamientos actualmente visibles en la interfaz, en el formato adecuado para su análisis posterior.
- **Realiza:** RF-10
- **Precondición:** Existe una búsqueda con resultados visibles en la interfaz (postcondición de `CU001`). Los resultados pueden estar filtrados (postcondición de `CU002`) o no; en ambos casos `CU003` descarga lo que está a la vista. En una versión futura del sistema, cuando D2 sea legible desde la interfaz, `CU003` también podrá iniciarse a partir de una búsqueda cargada del historial, sin haber ejecutado `CU001` en la sesión actual.
- **Disparador:** El investigador quiere llevarse un archivo con los resultados.
- **Garantía de éxito:** El investigador tiene, en su equipo, un archivo en el formato pedido con los alineamientos que estaban visibles al momento de presionar **Descargar**.
- **Garantía mínima:** El archivo entregado nunca contiene hits que no estuvieran visibles en la tabla al momento de descargar, ni omite hits que sí lo estaban.

### Flujo principal

1. El investigador elige el **formato de descarga** (CSV, JSON, FASTA, tabular BLAST `-outfmt 6`, o XML) y presiona **Descargar**.
2. El sistema arma el archivo con los alineamientos actualmente visibles en la tabla, en el formato pedido, e incluye una sección de metadatos con parámetros pre-búsqueda, base de datos usada, timestamp y filtros post-búsqueda aplicados (si los hay).
3. El sistema entrega el archivo al investigador.

**Postcondición:** El archivo con los resultados (filtrados o no, según el estado de la tabla al momento de la descarga) está en el equipo del investigador. No se modifica D2 (la persistencia ya la hizo `CU001_B2` al ejecutar).

### Por qué este CU no se subdivide en slices

`CU003` es corto (3 pasos) y sus pasos no son separables en módulos con valor propio: elegir formato sin descargar no deja nada útil, y descargar sin elegir formato daría un default arbitrario. El slice básico es entonces uno solo, identificado como `CU003_B`.

### Slices del CU

```
CU003 · Descargar los resultados en un formato
├─ Camino feliz
│  └─ CU003_B   — pasos 1-3:  elegir formato y descargar los resultados actualmente visibles
└─ Caminos alternativos
   └─ CU003_A1  — ningún resultado supera los filtros post-búsqueda
```

### Slices alternativos — descripción

- **`CU003_A1` · Ningún resultado supera los filtros post-búsqueda.** El investigador aplicó filtros que dejan la tabla vacía y de todos modos pide descargar. El sistema no impide la descarga: entrega un archivo con encabezados y la sección de metadatos de la búsqueda (parámetros, base de datos, timestamp, filtros aplicados) pero sin filas de hits, para que el investigador tenga constancia del intento. No hay persistencia adicional (la búsqueda ya está en D2 con sus resultados crudos, desde `CU001_B2`). **Realiza:** RF-10.

---

## Trazabilidad RF → CU → slice

La tabla `RF → CU → slice → HU` (con las HU incluidas) está en [`historias-usuario.md`](historias-usuario.md). Acá se resume la parte `RF → CU → slice`:

| RF | CU | Slice(s) que lo realizan |
|---|---|---|
| RF-01 | CU001 | CU001_B1 |
| RF-02 | CU001 | CU001_B1 |
| RF-03 | CU001 | CU001_B1, CU001_A2 |
| RF-04 | CU001 | CU001_B1, CU001_E2 |
| RF-05 | CU001 | CU001_B1, CU001_E3 |
| RF-06 | CU001 | CU001_B1, CU001_E1, CU001_E2 |
| RF-07 | CU001 | CU001_B2, CU001_A1, CU001_E4 |
| RF-08 | CU001 | CU001_B2 |
| RF-09 | CU002 | CU002_B |
| RF-10 | CU003 | CU003_B, CU003_A1 |
| RF-11 | CU001 | CU001_B2 |

Un mismo RF puede aparecer en varios slices del mismo CU — por ejemplo RF-06 (validación pre-ejecución) se realiza en el camino feliz `B1` (cuando la validación pasa) y también en `E1` y `E2` (cuando falla y corta el flujo). Esa dispersión es esperable: los slices de excepción son otra forma en que se cumple el RF de validación.

Ningún RF cruza entre los tres CU: los RF de ejecución y persistencia (RF-01 a RF-08, RF-11) son todos de `CU001`, RF-09 es exclusivo de `CU002` y RF-10 es exclusivo de `CU003`. Esa separación limpia es una consecuencia directa de haber separado los CU por capacidad y no por trazo secuencial: cada CU realiza el subconjunto de RF que le corresponde a su objetivo.
