# Casos de Uso — LocalBlast

Los casos de uso se redactan en **formato textual estructurado (Cockburn)**, actor, objetivo, precondición, flujo principal, alternativos, excepciones, postcondición, según pide el TP1, y **no** como diagrama gráfico (Mermaid no incluye un tipo de diagrama de casos de uso nativo).

Los casos de uso de este documento derivan de los dos procesos profundizados del DFD Nivel 1:

- `CU001`, `CU002`, `CU003`, `CU004` y `CU005` derivan del proceso **P1 · Ejecutar búsqueda BLAST**.
- `CU006` y `CU007` derivan del proceso **P2 · Filtrar y entregar resultados**.

Ambos procesos son necesarios para cerrar una interacción típica del investigador con el sistema: P1 le corre la búsqueda y la persiste, y P2 le deja trabajar con esos resultados (filtrar y descargar) a su conveniencia. El tercer proceso, **P3 (Administrar bases de datos)**, queda documentado a nivel de alcance en el DFD y en el modelo de dominio pero **no** tiene casos de uso propios en este TP (ver justificación en la sección 5 del [SRS](srs.md#5-selección-de-procesos-a-profundizar)).

Cada caso de uso declara qué requerimientos funcionales realiza. La cadena completa de trazabilidad es:

**RF → CU → slice → HU**

## Enfoque de los casos de uso

Un caso de uso representa **una capacidad discreta que el sistema le brinda al actor** , un objetivo alcanzable, no un trazo secuencial de pasos que el actor tiene que recorrer de punta a punta. Dos consecuencias prácticas de esa definición para este TP:

- **De los procesos profundizados salen siete CU, no uno solo largo ni dos medianos.** El investigador tiene siete objetivos distintos que el sistema le habilita, y que puede combinar como necesite:
  - `CU001` (cargar la secuencia query, deriva de **P1**) — dejar una secuencia disponible en la sesión, con su formato sintáctico chequeado, para usarla en una o varias búsquedas.
  - `CU002` (configurar los parámetros de la búsqueda, deriva de **P1**) — armar el resto del formulario de la búsqueda (modo, base de datos, programa BLAST, parámetros pre-búsqueda) sobre la secuencia ya cargada.
  - `CU003` (validar la búsqueda, deriva de **P1**) — pedirle al sistema que verifique semánticamente la configuración (alfabeto compatible con el programa, rangos, combinación programa/query/base de datos), y dejarla marcada como ejecutable.
  - `CU004` (ejecutar la búsqueda, deriva de **P1**) — correr BLAST+ sobre una configuración ya validada, con progreso y cancelación.
  - `CU005` (ver los resultados y persistir en el historial, deriva de **P1**) — presentar la tabla de alineamientos que devolvió BLAST+ y dejar la búsqueda registrada en D2 para uso posterior.
  - `CU006` (refinar con filtros post-búsqueda, deriva de **P2**) — ver los alineamientos con criterios post-búsqueda aplicados, sin volver a correr BLAST.
  - `CU007` (descargar, deriva de **P2**) — obtener un archivo con los alineamientos actualmente visibles, en un formato.
- **Los CU no obligan a una secuencia rígida.** El investigador puede cargar una secuencia (`CU001`) y luego probar tres configuraciones distintas encadenando `CU002 → CU003 → CU004 → CU005` tres veces, sin volver a cargar la secuencia. Puede parametrizar el formulario (`CU002`) sin llegar a pedir la validación (queda en la interfaz sin ejecutar). Puede validar (`CU003`) y quedarse mirando el "listo para ejecutar" sin lanzar la búsqueda todavía. Puede lanzar la ejecución (`CU004`) y cancelarla antes de ver resultados. Modelar todo esto como un único CU obligaría a que las capacidades ocurrieran juntas cuando en realidad son independientes.
- **La descarga no siempre se ejerce, y no siempre viene después del filtrado.** A veces el investigador solo quiere mirar los resultados filtrados en pantalla (queda en `CU006`) y no descargarlos. A veces querrá descargar sin haber filtrado (directamente `CU007` sobre los crudos). Y, cuando D2 se profundice como fuente de lectura en una versión futura, el investigador podrá iniciar `CU007` sobre una búsqueda vieja del historial sin volver a ejecutar `CU004`. Ese abanico de combinaciones es lo que justifica tener CU separados por capacidad y no uno solo secuencial.
- **Cada CU tiene un flujo principal corto.** Al haber partido los antiguos "cargar/configurar/validar" y "ejecutar/ver-resultados" en capacidades independientes, ninguno de los siete CU actuales necesita descomponerse en sub-slices básicos: cada uno tiene un único slice básico `B` de entre 1 y 3 pasos. Los caminos alternativos y las excepciones sí se numeran (`A1`, `A2`, …, `E1`, `E2`, …) y quedan repartidos entre los CU en el momento del flujo en el que aparecen: la validación sintáctica de la secuencia queda en `CU001_E1`; la BD local no disponible cae en `CU002_A1` porque es en la selección de BD que aparece; los errores semánticos de rango y de compatibilidad caen en `CU003_E1` y `CU003_E2` porque se detectan cuando el sistema valida; la cancelación manual y el fallo del modo remoto caen en `CU004_A1` y `CU004_E1` porque son eventos de la ejecución; y la descarga sobre tabla vacía queda en `CU007_A1`.

## Convención de identificadores y trazabilidad

**Cadena de trazabilidad:** `RF → CU → slice → HU`.

- Un **CU** puede realizar uno o varios RF, y a la inversa un RF puede estar realizado por varios slices del mismo CU (por ejemplo la validación semántica aparece tanto en el camino feliz de `CU003` como en sus slices de excepción).
- Un **RF** puede además estar realizado por varios CU distintos cuando el requerimiento tiene facetas separables, aunque en general en ese caso preferimos escribir dos RFs distintos y no uno con dos caras: por ejemplo, el chequeo sintáctico del formato del FASTA (RF-06, que se dispara al cargar la secuencia y cae en `CU001`) y el chequeo semántico de coherencia entre secuencia, programa, base de datos y parámetros (RF-12, que se dispara en la validación explícita y cae en `CU003`) originalmente eran un mismo RF-06 con dos facetas; los separamos en dos RFs distintos porque se disparan en momentos distintos, con criterios de aceptación distintos, y se realizan en CUs distintos.
- El identificador del **slice básico** es la letra `B` (`CU00X_B`). Los **slices alternativos** se numeran `A1`, `A2`, … y los **de excepción** `E1`, `E2`, …
- La relación **slice ↔ HU es 1:1**. La HU conserva el identificador de trazabilidad del slice: `HU01_CU001_B` detalla el slice `CU001_B`; `HU12_CU006_B` detalla el (único) slice básico de `CU006`.
- Los catorce slices identificados en los siete CU tienen **cada uno** su HU detallada en [`historias-usuario.md`](historias-usuario.md), con criterios Given-When-Then.
---

## CU001 · Cargar la secuencia query

- **Deriva del proceso:** P1 · Ejecutar búsqueda BLAST
- **Actor principal:** Investigador/a
- **Objetivo:** Dejar una secuencia query disponible en la sesión, con su formato sintáctico chequeado, para ser usada por una o varias búsquedas subsiguientes.
- **Realiza:** RF-01, RF-06
- **Precondición:** El investigador accedió a la interfaz web.
- **Disparador:** El investigador quiere trabajar con una secuencia biológica.
- **Garantía de éxito:** La secuencia queda cargada en la sesión, con su alfabeto inferido preliminarmente (ADN / ARN / proteína) y disponible para el resto del flujo.
- **Garantía mínima:** El sistema no acepta como cargada una secuencia con formato FASTA obviamente inválido (encabezado sin cuerpo, caracteres no imprimibles, archivo vacío).

### Flujo principal

1. El investigador ingresa la **secuencia query** subiendo un archivo FASTA desde su equipo o pegando la secuencia como texto en el formulario.
2. El sistema verifica que el contenido tenga formato reconocible (encabezado FASTA con cuerpo, o secuencia plana con caracteres imprimibles válidos) e infiere preliminarmente si es ADN, ARN o proteína en base al alfabeto observado.

**Postcondición:** La secuencia está cargada en la sesión y disponible para ser configurada en `CU002` (o para lanzar una nueva búsqueda sobre otra configuración, sin volver a cargarla).

### Slices del CU

```
CU001 · Cargar la secuencia query
├─ Camino feliz
│  └─ CU001_B    — pasos 1-2:  cargar la secuencia y verificar formato sintáctico
└─ Terminaciones abruptas (slices E)
   └─ CU001_E1   — secuencia query con formato inválido
```

### Slice básico — descripción

- **`CU001_B` · Cargar y chequear sintácticamente la secuencia query (pasos 1-2).** El investigador ingresa la secuencia (archivo o texto pegado) y el sistema verifica formato FASTA y alfabeto reconocible. **Valor entregado:** una secuencia queda disponible en la sesión para ser usada por `CU002` y los CU siguientes. **Realiza:** RF-01, RF-06.

### Slice de excepción — descripción

- **`CU001_E1` · Secuencia query con formato inválido.** En el paso 2, el chequeo sintáctico detecta que el contenido no tiene formato reconocible (caracteres fuera del alfabeto de ADN/ARN/proteína en cantidad significativa, FASTA mal formado, encabezado sin cuerpo, longitud fuera de rango, archivo vacío). El sistema no marca la secuencia como cargada, corta el flujo y muestra un mensaje que indica exactamente el problema y dónde aparece. **Realiza:** RF-06.

---

## CU002 · Configurar los parámetros de la búsqueda

- **Deriva del proceso:** P1 · Ejecutar búsqueda BLAST
- **Actor principal:** Investigador/a
- **Objetivo:** Armar el resto de la configuración de una búsqueda BLAST (modo de ejecución, base de datos, programa BLAST y parámetros pre-búsqueda) sobre una secuencia ya cargada, dejando el formulario listo para que `CU003` lo valide.
- **Realiza:** RF-02, RF-03, RF-04, RF-05. La verificación de que la elección quedó dentro de rangos válidos (RF-04) y de que la combinación es compatible (RF-05) se completa en `CU003` como parte de RF-12; en `CU002` cae la parte de "elegir".
- **Precondición:** Existe una secuencia query cargada en la sesión (postcondición de `CU001`).
- **Disparador:** El investigador quiere parametrizar la búsqueda que va a lanzar sobre esa secuencia.
- **Garantía de éxito:** El formulario de la búsqueda queda armado con modo, base de datos, programa y parámetros pre-búsqueda; la interfaz habilita el botón "Validar búsqueda" que dispara `CU003`.
- **Garantía mínima:** El sistema no permite dejar un campo obligatorio del formulario sin llenar; si el investigador cambia el modo, la lista de bases de datos se actualiza; si cambia el programa, los defaults de parámetros se recargan según el programa.

### Flujo principal

1. El investigador elige el **modo de ejecución**: local o remoto (NCBI). La interfaz muestra una única opción alternativa, para que la decisión sea clara.
2. El investigador selecciona la **base de datos** de una lista: si eligió modo local, aparecen las bases de datos del catálogo del laboratorio (leídas de D1); si eligió modo remoto, las bases estándar de NCBI.
3. El investigador elige el **programa BLAST** a ejecutar (`blastn`, `blastp`, `blastx`, `tblastn`, `tblastx`).
4. El investigador ajusta los **parámetros pre-búsqueda** (E-value máximo, matriz de sustitución, tamaño de palabra, penalización de gaps). La interfaz ofrece valores por defecto sensatos según el programa.

**Postcondición:** El formulario de la búsqueda está completo. El investigador puede iniciar `CU003` para validarla; nada obliga a hacerlo en ese momento (puede seguir tocando el formulario o abandonar).

### Slices del CU

```
CU002 · Configurar los parámetros de la búsqueda
├─ Camino feliz
│  └─ CU002_B    — pasos 1-4:  elegir modo, BD, programa y parámetros pre-búsqueda
└─ Caminos alternativos (slices A)
   └─ CU002_A1   — base de datos local no disponible
```

### Slice alternativo — descripción

- **`CU002_A1` · Base de datos local no disponible.** En el paso 2, el investigador seleccionó modo local y una base de datos que en ese momento no está lista en D1 (por ejemplo, se está actualizando desde P3, o su índice quedó marcado con error). El sistema informa el estado de esa base de datos y su motivo, y devuelve al investigador al paso 2 con la lista de bases de datos locales actualizada. El investigador decide por su cuenta qué hacer a continuación (elegir otra base local, cambiar de modo, o abandonar); el sistema **no** propone equivalencias entre bases locales y remotas, porque no las hay: una base propia del laboratorio no es intercambiable con las bases estándar de NCBI. **Realiza:** RF-03.

---

## CU003 · Validar la búsqueda

- **Deriva del proceso:** P1 · Ejecutar búsqueda BLAST
- **Actor principal:** Investigador/a
- **Objetivo:** Obtener del sistema una verificación semántica de la configuración armada en `CU002` (alfabeto de la secuencia compatible con el programa elegido, parámetros dentro de los rangos válidos del programa, combinación programa/query/base de datos compatible), y dejar la búsqueda marcada como "válida y ejecutable" para que `CU004` la pueda lanzar.
- **Realiza:** RF-12 (validación semántica completa), y por su relación con los campos del formulario también RF-04 (verificar rangos de parámetros) y RF-05 (verificar compatibilidad programa/query/base de datos)
- **Precondición:** Existe una secuencia cargada (postcondición de `CU001`) y un formulario de búsqueda completo (postcondición de `CU002`).
- **Disparador:** El investigador quiere confirmar que la búsqueda armada es lanzable, antes de comprometer tiempo de BLAST+.
- **Garantía de éxito:** La configuración de búsqueda queda marcada como "válida y lista para ejecutar" en la sesión; la interfaz habilita el botón "Ejecutar búsqueda" que dispara `CU004`.
- **Garantía mínima:** El sistema nunca deja "pasar como válida" una configuración con alfabeto incompatible, parámetro fuera de rango o combinación programa/query/BD incompatible. Si algo falla, la configuración queda marcada como no ejecutable hasta que el investigador la corrija y vuelva a validar.

### Flujo principal

1. El investigador presiona **Validar búsqueda**.
2. El sistema verifica que la secuencia (con el alfabeto inferido en `CU001`) sea coherente con el programa BLAST elegido en `CU002`, que los parámetros pre-búsqueda estén dentro de los rangos lógicos del programa, y que la combinación programa / tipo de query / tipo de base de datos sea compatible. Si todas las verificaciones pasan, el sistema marca la configuración como "válida y lista para ejecutar" y habilita el botón **Ejecutar búsqueda** que dispara `CU004`.

**Postcondición:** El sistema tiene registrada una configuración de búsqueda validada para la sesión. El investigador puede iniciar `CU004` para ejecutarla; nada obliga a hacerlo en ese momento.

### Slices del CU

```
CU003 · Validar la búsqueda
├─ Camino feliz
│  └─ CU003_B    — pasos 1-2:  disparar la validación y recibir el visto bueno
└─ Terminaciones abruptas (slices E)
   ├─ CU003_E1   — parámetros pre-búsqueda fuera de rango
   └─ CU003_E2   — combinación programa / query / base de datos incompatible
```

### Slice básico — descripción

- **`CU003_B` · Validar semánticamente la búsqueda (pasos 1-2).** El investigador dispara la validación y el sistema chequea alfabeto, rangos y compatibilidad. Al pasar, marca la configuración como ejecutable y habilita el disparador de `CU004`. **Valor entregado:** el investigador tiene la confirmación explícita del sistema de que su búsqueda es lanzable, y `CU004` queda habilitado. **Realiza:** RF-04, RF-05, RF-12.

### Slices de excepción — descripción

Son terminaciones abruptas del flujo: el sistema detecta una condición que impide marcar la búsqueda como válida, corta la ejecución del CU y notifica al investigador. La postcondición del CU no se alcanza (la configuración no queda marcada como ejecutable) y BLAST+ no es invocado.

- **`CU003_E1` · Parámetros pre-búsqueda fuera de rango.** En el paso 2, la validación detecta al menos un parámetro con valor imposible para el programa elegido (E-value negativo, tamaño de palabra fuera del rango soportado por el programa, penalización de gap fuera de escala). El sistema corta el flujo y señala qué campo corregir y cuál es el rango esperado. **Realiza:** RF-04, RF-12.
- **`CU003_E2` · Combinación programa / query / base de datos incompatible.** En el paso 2, la verificación de compatibilidad detecta que el programa BLAST elegido no coincide con el tipo de la secuencia query o con el tipo de la base de datos (por ejemplo `blastp` con query de nucleótidos, o `blastn` contra una base de datos de proteínas). El sistema corta el flujo, indica el motivo y sugiere qué combinaciones sí son válidas para lo que el usuario ya cargó. **Realiza:** RF-05, RF-12.

---

## CU004 · Ejecutar la búsqueda

- **Deriva del proceso:** P1 · Ejecutar búsqueda BLAST
- **Actor principal:** Investigador/a
- **Actor secundario:** Motor **BLAST+** (invocado por el sistema en ambos modos: local, y remoto con la flag `-remote` — es BLAST+ el que se comunica con NCBI del otro lado, nunca directamente nuestra GUI)
- **Objetivo:** Correr la búsqueda ya validada en `CU003`, en segundo plano, con indicador de progreso y opción de cancelación, hasta obtener el conjunto crudo de alineamientos que devuelve BLAST+.
- **Realiza:** RF-07
- **Precondición:** Existe en la sesión una configuración de búsqueda validada (postcondición de `CU003`); el botón "Ejecutar búsqueda" está habilitado.
- **Disparador:** El investigador decide lanzar la búsqueda ya validada.
- **Garantía de éxito:** BLAST+ terminó la ejecución exitosamente y el conjunto crudo de alineamientos queda disponible en la sesión para que `CU005` lo presente y persista.
- **Garantía mínima:** El sistema nunca deja búsquedas parcialmente ejecutadas consumiendo recursos indefinidamente. Si la ejecución se aborta (cancelación manual o fallo remoto), nada se le pasa a `CU005` y nada se persiste en D2.

### Flujo principal

1. El investigador presiona **Ejecutar búsqueda** sobre una configuración ya validada por `CU003`.
2. El sistema **invoca a BLAST+** en segundo plano con la combinación de opciones armada a partir de la configuración validada (programa, ruta de la base de datos, query, parámetros pre-búsqueda, y la flag `-remote` cuando el modo elegido es remoto), y muestra un indicador de progreso sin bloquear la interfaz. La comunicación con NCBI, cuando corresponde, la realiza BLAST+ internamente por la flag `-remote`; el sistema solo espera su respuesta.
3. Cuando BLAST+ termina, el sistema recibe el conjunto crudo de alineamientos y dispara `CU005` para presentarlos y persistirlos.

**Postcondición:** El conjunto crudo de alineamientos está disponible en memoria de la sesión; `CU005` toma el control para mostrarlo y persistirlo.

### Slices del CU

```
CU004 · Ejecutar la búsqueda
├─ Camino feliz
│  └─ CU004_B    — pasos 1-3:  invocar BLAST+, monitorear la ejecución, obtener resultados crudos
├─ Caminos alternativos (slices A)
│  └─ CU004_A1   — cancelación manual de la búsqueda en curso
└─ Terminaciones abruptas (slices E)
   └─ CU004_E1   — fallo del modo remoto de BLAST+
```

### Slice básico — descripción

- **`CU004_B` · Invocar BLAST+ y obtener resultados crudos (pasos 1-3).** El sistema invoca a BLAST+ en segundo plano, muestra progreso, permite cancelar y, al terminar exitosamente, deja el conjunto crudo de alineamientos disponible en la sesión y dispara `CU005`. **Valor entregado:** BLAST+ hizo el trabajo pesado y sus resultados quedan disponibles para el siguiente CU. **Realiza:** RF-07.

### Slice alternativo — descripción

- **`CU004_A1` · Cancelación manual de la búsqueda.** Mientras la búsqueda está en ejecución (durante el paso 2 del camino feliz), el investigador presiona **Cancelar**. El sistema aborta el subproceso local o cancela la solicitud remota a través de BLAST+, y deja la interfaz lista para iniciar una nueva búsqueda. La postcondición del CU no se alcanza; es una decisión explícita del actor de abandonar el objetivo actual. Al no haber ejecución exitosa, `CU005` no se dispara y no hay persistencia en D2. **Realiza:** RF-07.

### Slice de excepción — descripción

- **`CU004_E1` · Fallo del modo remoto de BLAST+.** Durante el paso 2, con modo remoto seleccionado, BLAST+ reporta un error de comunicación con NCBI (sin respuesta, timeout, o error explícito devuelto por la API). El sistema captura el error, corta el flujo del CU e informa al investigador con el detalle recibido. Un reintento posterior es un CU nuevo, no la continuación de este. Al no haber ejecución exitosa, `CU005` no se dispara y no hay persistencia en D2. **Realiza:** RF-07.

---

## CU005 · Ver los resultados y persistir la búsqueda en el historial

- **Deriva del proceso:** P1 · Ejecutar búsqueda BLAST
- **Actor principal:** Investigador/a
- **Objetivo:** Presentar los alineamientos crudos que dejó `CU004` en una tabla visible para el investigador, y dejar la búsqueda registrada en el historial D2 para uso posterior.
- **Realiza:** RF-08, RF-11
- **Precondición:** Existe en memoria de la sesión un conjunto crudo de alineamientos, entregado por una ejecución exitosa de `CU004`.
- **Disparador:** `CU004` termina exitosamente y libera los resultados crudos.
- **Garantía de éxito:** El investigador ve la tabla de alineamientos en la interfaz, y la búsqueda (con sus resultados crudos) queda persistida en D2. Esos resultados quedan disponibles en la sesión para que el investigador los procese después con `CU006` (refinar) o `CU007` (descargar), si así lo decide.
- **Garantía mínima:** La presentación y la persistencia son consistentes entre sí: si la tabla se muestra, la entrada en D2 también queda escrita con el mismo conjunto crudo; nunca se ve una cosa sin la otra.

### Flujo principal

1. El sistema muestra la **lista de alineamientos** (hits) en una tabla, con columnas mínimas: identificador del hit, score, E-value observado, % identidad, % cobertura.
2. El sistema **persiste la búsqueda con sus resultados crudos en D2** (parámetros pre-búsqueda, base de datos usada, timestamp y lista completa de alineamientos antes de cualquier filtro).

**Postcondición:** El investigador ve la tabla de alineamientos de su búsqueda en la interfaz, y la búsqueda queda persistida en D2. Los resultados quedan disponibles en la sesión para que el investigador los use en `CU006` (refinar) o `CU007` (descargar) si así lo decide.

### Por qué este CU no tiene slices secundarios

`CU005` es corto (2 pasos) y opera sobre datos que ya son válidos (BLAST+ terminó exitosamente en `CU004`): en el momento en que `CU005` se dispara, no hay decisiones del actor ni condiciones de error nuevas que puedan interrumpirlo. Un fallo al escribir en D2 se trata como un error de infraestructura del sistema (fuera del alcance del TP1) y no como un slice del CU. El slice básico es entonces uno solo, identificado como `CU005_B`.

### Slices del CU

```
CU005 · Ver los resultados y persistir la búsqueda en el historial
└─ Camino feliz
   └─ CU005_B    — pasos 1-2:  presentar la tabla de alineamientos y persistir en D2
```

---

## CU006 · Refinar los resultados con filtros post-búsqueda

- **Deriva del proceso:** P2 · Filtrar y entregar resultados
- **Actor principal:** Investigador/a
- **Objetivo:** Ver la lista de alineamientos filtrada por criterios post-búsqueda (identidad, cobertura, E-value observado, taxonomía), sin re-ejecutar BLAST.
- **Realiza:** RF-09
- **Precondición:** Existe una búsqueda con resultados visibles en la interfaz (postcondición de `CU005`). En una versión futura del sistema, cuando D2 sea legible desde la interfaz, esos resultados también podrán provenir del historial sin haber ejecutado `CU004`/`CU005` en la sesión actual.
- **Disparador:** El investigador quiere restringir la vista a un subconjunto de los alineamientos según criterios post-búsqueda.
- **Garantía de éxito:** La tabla muestra los alineamientos que superan los criterios elegidos. No se ejecuta BLAST+ ni se persiste nada nuevo en D2 (la búsqueda ya quedó registrada en `CU005` con sus resultados crudos).
- **Garantía mínima:** La tabla filtrada nunca "inventa" hits que no estaban en el conjunto crudo; los filtros son estrictamente restrictivos sobre el conjunto ya calculado.

### Flujo principal

1. El investigador ajusta los **filtros post-búsqueda** (umbrales de identidad, cobertura, E-value observado; filtro por taxonomía cuando la información esté disponible).
2. El sistema re-filtra la tabla en el momento, mostrando únicamente los hits que superan todos los umbrales fijados, **sin volver a invocar a BLAST+**.

**Postcondición:** La tabla de resultados visible en la interfaz refleja los filtros post-búsqueda actuales. Los resultados crudos originales siguen intactos en la sesión (y en D2), disponibles para probar otros filtros o para descargar sin filtrar.

### Por qué este CU no se subdivide en slices

`CU006` es corto (2 pasos) y no tiene módulos internos con valor separado: ajustar filtros sin ver la tabla re-filtrada no aporta nada, y la re-filtración sin el ajuste previo no tiene sentido. El slice básico es entonces uno solo, identificado como `CU006_B`. Tampoco tiene alternativas ni excepciones dignas de nota: el caso "el filtro deja la tabla vacía" no interrumpe el CU (la tabla vacía es un resultado válido del filtro); es un problema recién si el investigador intenta descargar esa tabla vacía, y por eso ese caso vive en `CU007_A1`.

### Slices del CU

```
CU006 · Refinar los resultados con filtros post-búsqueda
└─ Camino feliz
   └─ CU006_B   — pasos 1-2:  ajustar filtros post-búsqueda y ver la tabla re-filtrada
```

---

## CU007 · Descargar los resultados en un formato

- **Deriva del proceso:** P2 · Filtrar y entregar resultados
- **Actor principal:** Investigador/a
- **Objetivo:** Obtener, en su equipo, un archivo con los alineamientos actualmente visibles en la interfaz, en el formato adecuado para su análisis posterior.
- **Realiza:** RF-10
- **Precondición:** Existe una búsqueda con resultados visibles en la interfaz (postcondición de `CU005`). Los resultados pueden estar filtrados (postcondición de `CU006`) o no; en ambos casos `CU007` descarga lo que está a la vista. En una versión futura del sistema, cuando D2 sea legible desde la interfaz, `CU007` también podrá iniciarse a partir de una búsqueda cargada del historial, sin haber ejecutado `CU004`/`CU005` en la sesión actual.
- **Disparador:** El investigador quiere llevarse un archivo con los resultados.
- **Garantía de éxito:** El investigador tiene, en su equipo, un archivo en el formato pedido con los alineamientos que estaban visibles al momento de presionar **Descargar**.
- **Garantía mínima:** El archivo entregado nunca contiene hits que no estuvieran visibles en la tabla al momento de descargar, ni omite hits que sí lo estaban.

### Flujo principal

1. El investigador elige el **formato de descarga** (CSV, JSON, FASTA, tabular BLAST `-outfmt 6`, o XML) y presiona **Descargar**.
2. El sistema arma el archivo con los alineamientos actualmente visibles en la tabla, en el formato pedido, e incluye una sección de metadatos con parámetros pre-búsqueda, base de datos usada, timestamp y filtros post-búsqueda aplicados (si los hay).
3. El sistema entrega el archivo al investigador.

**Postcondición:** El archivo con los resultados (filtrados o no, según el estado de la tabla al momento de la descarga) está en el equipo del investigador. No se modifica D2 (la persistencia ya la hizo `CU005_B` al finalizar la ejecución).

### Por qué este CU no se subdivide en slices

`CU007` es corto (3 pasos) y sus pasos no son separables en módulos con valor propio: elegir formato sin descargar no deja nada útil, y descargar sin elegir formato daría un default arbitrario. El slice básico es entonces uno solo, identificado como `CU007_B`.

### Slices del CU

```
CU007 · Descargar los resultados en un formato
├─ Camino feliz
│  └─ CU007_B   — pasos 1-3:  elegir formato y descargar los resultados actualmente visibles
└─ Caminos alternativos
   └─ CU007_A1  — ningún resultado supera los filtros post-búsqueda
```

### Slices alternativos — descripción

- **`CU007_A1` · Ningún resultado supera los filtros post-búsqueda.** El investigador aplicó filtros que dejan la tabla vacía y de todos modos pide descargar. El sistema no impide la descarga: entrega un archivo con encabezados y la sección de metadatos de la búsqueda (parámetros, base de datos, timestamp, filtros aplicados) pero sin filas de hits, para que el investigador tenga constancia del intento. No hay persistencia adicional (la búsqueda ya está en D2 con sus resultados crudos, desde `CU005_B`). **Realiza:** RF-10.

## Trazabilidad RF → CU → slice

La tabla `RF → CU → slice → HU` (con las HU incluidas) está en [`historias-usuario.md`](historias-usuario.md). Acá se resume la parte `RF → CU → slice`:

| RF | CU | Slice(s) que lo realizan |
|---|---|---|
| RF-01 | CU001 | CU001_B |
| RF-02 | CU002 | CU002_B |
| RF-03 | CU002 | CU002_B, CU002_A1 |
| RF-04 | CU002, CU003 | CU002_B, CU003_B, CU003_E1 |
| RF-05 | CU002, CU003 | CU002_B, CU003_B, CU003_E2 |
| RF-06 | CU001 | CU001_B, CU001_E1 |
| RF-07 | CU004 | CU004_B, CU004_A1, CU004_E1 |
| RF-08 | CU005 | CU005_B |
| RF-09 | CU006 | CU006_B |
| RF-10 | CU007 | CU007_B, CU007_A1 |
| RF-11 | CU005 | CU005_B |
| RF-12 | CU003 | CU003_B, CU003_E1, CU003_E2 |

Dos RFs cruzan más de un CU:

- **RF-04** (rangos de parámetros) aparece en `CU002` (donde el investigador los elige, con los defaults del programa) y en `CU003` (donde el sistema verifica que estén dentro del rango válido del programa).
- **RF-05** (compatibilidad programa/query/BD) aparece en `CU002` (donde el investigador elige el programa) y en `CU003` (donde el sistema verifica la coherencia con la query y la BD ya elegidas).

Además, `RF-06` (validación sintáctica) y `RF-12` (validación semántica) son dos RFs conceptualmente emparentados pero **separados**: cubren facetas distintas de "el sistema debe validar antes de ejecutar" que ocurren en momentos distintos del flujo (al cargar la secuencia vs. al pedir el visto bueno), en CUs distintos (`CU001` vs. `CU003`), y con criterios de aceptación distintos. En una versión temprana del SRS eran un mismo RF con dos facetas anotadas como sufijo `(sint.)/(sem.)`; ver la Entrada 12 de la bitácora de IA para el detalle de por qué los separamos.

Un mismo RF puede aparecer también en varios slices del mismo CU — por ejemplo RF-12 se realiza en el camino feliz `CU003_B` (cuando la validación semántica pasa) y también en `CU003_E1` y `CU003_E2` (cuando falla y corta el flujo). Esa dispersión es esperable: los slices de excepción son otra forma en que se cumple el RF de validación.
