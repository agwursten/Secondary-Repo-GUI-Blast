# Maquetado HTML — Primer ciclo de generación con IA

Esta carpeta contiene el maquetado HTML del flujo de navegación del Investigador/a, generado en el **primer ciclo** del proceso de maquetado asistido por IA. Cada archivo corresponde a una de las pantallas definidas en el flujo de navegación del perfil ([`../user-profiles/investigador.md`](../user-profiles/investigador.md), sección 3) y lleva en el nombre las historias de usuario que respalda.

## Archivos

| Archivo | Pantalla del flujo | HUs cubiertas |
|---|---|---|
| [`pantalla-01-carga-secuencia_HU01-HU02.html`](pantalla-01-carga-secuencia_HU01-HU02.html) | Nueva búsqueda — Secuencia query | `HU01_CU001_B`, `HU02_CU001_E1` |
| [`pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07.html`](pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07.html) | Nueva búsqueda — Configuración + validación | `HU03_CU002_B`, `HU04_CU002_A1`, `HU05_CU003_B`, `HU06_CU003_E1`, `HU07_CU003_E2` |
| [`pantalla-03-ejecucion_HU08-HU09-HU10.html`](pantalla-03-ejecucion_HU08-HU09-HU10.html) | Ejecución en progreso | `HU08_CU004_B`, `HU09_CU004_A1`, `HU10_CU004_E1` |
| [`pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14.html`](pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14.html) | Resultados · filtros · descarga | `HU11_CU005_B`, `HU12_CU006_B`, `HU13_CU007_B`, `HU14_CU007_A1` |

Las **14 HUs del catálogo** del TP1 que requieren interfaz quedan cubiertas por estos cuatro archivos. La pantalla de autenticación mencionada en el flujo del perfil **no se maqueta** en esta iteración: no hay HU que la respalde y el principio de diseño del grupo es *"si una pantalla no está respaldada por alguna HU, no se maqueta"*. El resto del flujo asume sesión ya iniciada.

Cada archivo HTML muestra apilados el **estado primario** (camino feliz) y los **estados alternativos y de excepción** cubiertos por sus HUs, cada uno con una etiqueta visible que indica a qué HU y a qué criterio de aceptación corresponde. Esta decisión se tomó para que la evaluación visual pueda recorrer todos los estados sin necesidad de interactuar. En la implementación final solo un estado será visible al mismo tiempo.

---

## 1. Criterios definidos por el grupo antes de pedir a la IA

Antes de redactar el prompt, el grupo acordó los siguientes criterios para evitar que la IA eligiera por su cuenta decisiones que son de dominio del proyecto:

### 1.1 Tipo de sistema

- **Aplicación web** (SRS §1.3 fija *"Interfaz web"* en el alcance), específicamente una GUI para BLAST+.
- **Pensada para desktop/laptop** con navegador moderno; el perfil del Investigador/a lo marca explícitamente (*"el sistema no está pensado para uso cómodo en celular"* — [`investigador.md`](../user-profiles/investigador.md) §1.3). El maquetado se diseña para anchos típicos de desktop (~1024-1280 px), con layouts que degradan razonablemente pero sin tratamiento mobile-first.

### 1.2 Lenguaje y framework del maquetado

- **HTML + CSS puro**, sin framework. Un archivo `.html` autocontenido por pantalla, con el CSS en una etiqueta `<style>` embebida, para que cada archivo se abra en cualquier navegador sin build-step.
- **Sin JavaScript** (ni interactividad real): el objetivo del primer ciclo es la maqueta de interfaz, no el prototipo funcional. Los distintos estados por HU se renderizan apilados en el mismo archivo con etiquetas visibles, en vez de intercambiarse por script.
- Esta decisión difiere de cómo luego se implementará el sistema, pero se tomó para que el entregable sea legible en un commit, revisable visualmente sin tooling y portable entre máquinas del grupo.

### 1.3 Perfil de usuario y escenario de uso

- **Único actor con historias de usuario:** Investigador/a (ver [`investigador.md`](../user-profiles/investigador.md)).
- **Escenario de uso de referencia:** camino feliz construido alrededor de `HU13_CU007_B` (descargar los alineamientos actualmente visibles en un formato), que cierra el ciclo completo de valor y encadena naturalmente las HUs necesarias para llegar hasta allí.
- **Variantes realistas** que el maquetado debe sostener: secuencia inválida y base local no disponible, además de los demás caminos de excepción (`HU06`, `HU07`, `HU09`, `HU10`, `HU14`).

### 1.4 Otros criterios relevantes para este proyecto

- **Rango de nivel técnico del usuario.** El perfil del Investigador cubre desde estudiante de grado hasta investigador sénior. La interfaz debe ser accesible para el extremo inferior (defaults sensatos, mensajes de error diagnósticos) **sin** sacarle control al extremo superior (poder ajustar parámetros, elegir bases locales, descargar en formatos como BLAST XML o tabular `-outfmt 6`).
- **Defaults por programa.** Los valores por defecto de los parámetros pre-búsqueda deben verse como *"recalculados según el programa BLAST elegido"* (RF-06): el maquetado tiene que mostrar explícitamente ese comportamiento, no fijar un único juego de números.
- **Mensajes diagnósticos, no genéricos.** Los estados de excepción deben mostrar el campo exacto en problema y, cuando corresponde, el mensaje literal de BLAST+ (`HU10`) sin reinterpretarlo. Esto está en el perfil (sección "Limitaciones y frustraciones").
- **Separación entre conjunto crudo y vista filtrada.** En la pantalla de resultados tiene que ser visible que los filtros se aplican sobre el conjunto crudo (no sobre el resultado anterior), que la descarga toma los visibles, y que el historial (D2) nunca se modifica por filtros ni por descarga. Es la base del escenario de calidad de Operabilidad y de la lógica de `HU12`/`HU13`/`HU14`.
- **Columnas mínimas de la tabla de resultados.** Según `HU11_CU005_B` CA-01: identificador del hit, score, E-value observado, % de identidad, % de cobertura. El maquetado debe mostrar al menos esas columnas (puede sumar descripción del hit como ayuda visual, pero no reemplazarlas).
- **Trazabilidad explícita HU ↔ pantalla.** El nombre de archivo debe incluir el identificador de la pantalla y las HUs cubiertas (ej.: `pantalla-01-carga-secuencia_HU01-HU02.html`), para que la correspondencia con el catálogo de HU sea verificable a simple vista.

---

## 2. Prompt utilizado

El prompt se le pasó a la IA junto con el repositorio actual (todos los archivos de `docs/`, principalmente el SRS, `historias-usuario.md` y el perfil del Investigador/a):

> **Prompt:**
>
> Les paso el repositorio actual del proyecto LocalBlast (TP de Ingeniería de Software). El perfil de usuario ya está definido y validado en `docs/ui/user-profiles/investigador.md` — ahí están el escenario de uso de referencia (construido alrededor de `HU13_CU007_B`, con camino feliz y variantes realistas) y el flujo de navegación con las pantallas y las HUs que respaldan a cada una. El catálogo completo de 14 HUs está en `docs/requeriments/historias-usuario.md`, con sus criterios Given-When-Then; los RF-01 a RF-12 están en `docs/requeriments/srs.md` §6.
>
> Necesitamos el **maquetado HTML del flujo de navegación** correspondiente a las pantallas que lista `investigador.md` §3. Pedimos un archivo `.html` por pantalla, no un prototipo navegable: el objetivo de este primer ciclo es la maqueta visual.
>
> **Reglas que acordamos antes y queremos que respetes:**
>
> 1. **Una pantalla, un archivo HTML.** Nombres de archivo con el formato `pantalla-NN-<slug>_HU<X>-HU<Y>.html`, donde los HU listados son todos los que la pantalla cubre. Ejemplo del formato que pidió la cátedra: `pantalla-01-carga-secuencia_HU01-HU02.html`.
> 2. **No maquetar la pantalla de autenticación.** No tiene HU asociada y el principio de diseño del proyecto es *"si una pantalla no está respaldada por alguna HU, no se maqueta"*. El flujo arranca en "Nueva búsqueda — Secuencia query" asumiendo sesión ya iniciada; podés poner un chip de usuario en el header para dejarlo visible.
> 3. **HTML + CSS puro, sin framework, sin JS.** Cada archivo autocontenido, con el CSS en `<style>` embebido. Que se pueda abrir con doble-click sin servidor local ni build-step.
> 4. **Pensado para desktop/laptop.** No priorizar mobile; podés dejar que degrade razonablemente pero el ancho objetivo es ~1024-1280 px.
> 5. **Cada pantalla debe mostrar el estado primario (camino feliz) y los estados alternativos / de excepción** de las HUs que cubre, apilados en el mismo archivo, con una etiqueta visible por sección que diga a qué HU y a qué criterio de aceptación (CA-01, CA-02, …) corresponde cada estado. Esto nos permite revisar visualmente la cobertura sin tener que interactuar.
> 6. **Lenguaje y defaults del dominio.** Los parámetros pre-búsqueda (E-value, matriz, tamaño de palabra, gaps) tienen que verse *"recalculados según el programa BLAST elegido"* como pide RF-06: el default de `blastp` no es el de `blastn`. En la pantalla de configuración, mostrar la vista con `blastp` por defecto y dejar explícito que los números corresponden a ese programa.
> 7. **Mensajes diagnósticos, no genéricos.**
>    - Secuencia inválida (`HU02_CU001_E1`): indicar carácter y posición exactos.
>    - Parámetros fuera de rango (`HU06`): señalar el campo y el rango válido para ese programa.
>    - Combinación incompatible (`HU07`): dar las opciones válidas con lo que ya está cargado.
>    - Base local no disponible (`HU04`): informar explícitamente el estado y refrescar la lista, **sin** proponer un cambio automático a modo remoto (eso ya lo decidimos cuando armamos las HU: no hay equivalencias reales entre bases locales y bases de NCBI).
>    - Fallo de modo remoto (`HU10`): mostrar el mensaje literal de BLAST+/NCBI en un bloque monoespaciado, sin reinterpretarlo.
> 8. **Pantalla de ejecución asíncrona.** Dejar visualmente evidente que el usuario puede seguir navegando mientras BLAST+ corre (barra lateral con el resto de la aplicación disponible y un chip de "corriendo", por ejemplo). Botón "Cancelar búsqueda" bien visible.
> 9. **Pantalla de resultados.** Tabla con las columnas mínimas que exige `HU11_CU005_B` CA-01 (hit ID, score, E-value observado, % identidad, % cobertura). Panel de filtros a un costado con identidad, cobertura, E-value y taxonomía; que se vea que son filtros post-búsqueda (no re-ejecutan BLAST). Selector de formato de descarga (CSV, JSON, FASTA, BLAST XML, tabular `-outfmt 6`) y botón Descargar que diga cuántos hits visibles descarga. Chip "Guardado en el historial" para la persistencia automática de `HU11`. Mostrar también el estado alternativo de `HU14_CU007_A1` (tabla vacía por filtros, descarga válida solo con metadatos).
> 10. **Estética.** Que lea como una herramienta académica/científica (tono NCBI/ENA, no SaaS llamativo), tipografías de sistema y una paleta sobria. Que se vea seria y usable, no una presentación de ventas.
>
> **Dejanos todos los archivos en `docs/ui/mockups/`** y agregá un `README.md` ahí mismo con el índice, los criterios que te pasamos acá, el prompt y un resumen de la respuesta.

---

## 3. Respuesta obtenida de la IA

### 3.1 Qué generó

- **4 archivos HTML** en esta carpeta (uno por pantalla del flujo que respaldan HU; no se maquetó autenticación).
- Un sistema visual común a todas las pantallas (variables CSS compartidas, misma paleta, misma tipografía, mismo chrome del header y mismo stepper), para que el flujo lea como una sola aplicación.
- Dentro de cada archivo, el **estado primario** encima y debajo los **estados alternativos y de excepción**, cada uno precedido por una etiqueta tipo `ESTADO DE EXCEPCIÓN · HU02_CU001_E1 · CA-01`, para que la cobertura por HU y por criterio de aceptación se vea sin interactuar.
- Una **nota de maquetado** al pie de cada pantalla explicando qué HUs cubre y por qué los estados se muestran apilados.
- En la pantalla de configuración, defaults coherentes con `blastp` (BLOSUM62, word-size 3, E-value 10) y un hint explícito *"valores por defecto para blastp"* para dejar visible que los números dependen del programa.
- En la pantalla de ejecución, barra lateral con el resto de la aplicación disponible y un chip animado *"corriendo"* junto al ítem "Ejecución en curso", para reforzar visualmente la propiedad de ejecución asíncrona que pide `HU08`.
- En la pantalla de resultados, barras horizontales pequeñas junto a los porcentajes de identidad y cobertura (ayuda visual que no reemplaza al número) y una fila de metadatos arriba de la tabla (query, programa, base, E-value, matriz, timestamp) que corresponde a la que después se incluye en la descarga.

### 3.2 Qué aceptamos

- La estructura de **un archivo por pantalla con los estados apilados**: facilita la revisión por parte de la cátedra, mantiene uno a uno la relación pantalla ↔ archivo y permite leer la cobertura de HUs de un vistazo. Alternativas discutidas antes del prompt (una carpeta con subarchivos por estado, o un único HTML con tabs JS) se descartaron por complicar la navegación por archivos o por romper la regla de "sin JS".
- El sistema visual común, con stepper arriba, chip de usuario, barra lateral solo en la pantalla de ejecución (donde la navegabilidad en paralelo es parte del valor), y paleta sobria tipo herramienta académica.
- Las etiquetas de estado con el formato `ESTADO <X> · HU<ID> · CA-<n>`, que leen bien y mantienen la trazabilidad al criterio de aceptación.
- El tratamiento del mensaje literal de BLAST+ en bloque monoespaciado oscuro (como un terminal), que diferencia visualmente *"esto es lo que respondió BLAST+, sin filtros"* de los mensajes de la aplicación.
- En resultados: barras horizontales pequeñas para % identidad / cobertura, formato de descarga como pills, y el chip verde *"Guardado en el historial · hh:mm:ss"* arriba a la derecha.

### 3.3 Qué modificamos

- **Nombre del botón de validación.** La IA había puesto *"Verificar"* en el primer borrador, pero la HU dice literalmente *"Validar búsqueda"* (`HU05_CU003_B` CA-01). Cambiamos a *"Validar búsqueda"* para que coincida con el GWT.
- **Chip del encabezado en la pantalla de ejecución.** El primer borrador tenía *"La búsqueda está en progreso. Esperá a que termine"* como copy principal, que es exactamente lo opuesto a `HU08_CU004_B` CA-01 (*"la interfaz permanece navegable"*). Lo reescribimos como *"BLAST+ está procesando tu consulta en segundo plano. Podés navegar por el resto de la aplicación mientras tanto; esta ejecución no se interrumpe"* y agregamos la nota en el panel: *"Podés seguir trabajando. La búsqueda sigue corriendo aunque cambies de sección…"*.
- **Formato del mensaje de error de HU10.** En el primer borrador, la IA había traducido el error de BLAST+ a prosa natural (*"La conexión con NCBI superó el tiempo de espera, intentá más tarde"*). La HU exige mostrar el mensaje **literal**. Lo pusimos de vuelta en un `<pre>` monoespaciado con el stderr tal como lo produce BLAST+, y arriba una explicación breve de la aplicación (*"Timeout de comunicación con NCBI. No es un problema con los parámetros…"*) separada del bloque literal.
- **Base local no disponible: lista propuesta de alternativas.** La IA había puesto, debajo del mensaje de base no disponible, un botón *"Usar base equivalente en modo remoto (nr)"*. Lo sacamos: es exactamente la decisión que ya habíamos rechazado en el documento del perfil y en la bitácora de uso de IA (Entradas 4 y 5 de `uso-ia.md`): no hay equivalencias reales entre una base del laboratorio y una pública de NCBI, y proponer el cambio es científicamente engañoso. En su lugar, el estado alternativo refresca la lista con el estado de cada base (lista / actualizándose / con errores) y deja la decisión al Investigador.
- **Columna extra en la tabla de resultados.** La IA había agregado una columna *"Alignment length"* al borrador, pero no es una de las columnas mínimas de `HU11_CU005_B` CA-01 ni está pedida por ningún otro CA del flujo actual. La sacamos para no sobrecargar la tabla; si el equipo decide después que suma valor, se incorpora en la próxima iteración.
- **Pantalla de autenticación.** La IA, por costumbre de prototipado web, había generado también una pantalla de login (*"total es un flujo típico y queda más completo"*). La borramos del entregable: el principio de diseño del proyecto es claro, y la bitácora ya tiene registro de que *"Si una pantalla no está respaldada por alguna HU, no se maqueta"*.

### 3.4 Qué descartamos

- Una propuesta inicial de **separar los estados en archivos distintos** (`pantalla-01-A-primario.html`, `pantalla-01-B-excepcion.html`, …). Prolijo en teoría pero complicaba la revisión y multiplicaba archivos; el patrón "estados apilados en un archivo con etiquetas" quedó más legible.
- La idea de **agregar interactividad real con JavaScript** para intercambiar los estados de forma dinámica. Fue tentador en la pantalla de resultados (filtros sliders que efectivamente filtren una tabla local), pero se tomó como criterio del grupo que el primer ciclo es maquetado, no prototipo funcional. Se evaluará para ciclos posteriores si corresponde.
- Una propuesta de **usar íconos de un set externo** (Material Icons o Lucide). Habría requerido cargar un CSS externo o una fuente, violando la regla de "autocontenido". Reemplazamos los íconos por glifos Unicode simples (`✓`, `✗`, `⚠`, `⊘`, `⤓`) que no requieren recursos adicionales.
- Un **panel de historial** en el side-nav con búsquedas anteriores listadas. No corresponde a este primer ciclo (ninguna HU pide una pantalla de historial listable; `HU11` solo exige la persistencia). Quedó mencionado en la barra lateral como ítem de nav pero sin pantalla propia.

### 3.5 Errores / imprecisiones detectadas

- **Reinterpretación del mensaje de error de BLAST+.** Como se detalló arriba, la IA tiende a convertir mensajes de sistema en prosa amable, lo cual rompe el requisito explícito de `HU10` de mostrar el mensaje literal. Es el mismo patrón que ya habíamos anotado en la Entrada 4 de la bitácora: la IA mejora la "experiencia percibida" sin considerar que el investigador necesita el error crudo para diagnosticar. Hubo que señalárselo explícitamente.
- **Sugerencia de fallback automático a modo remoto para base local no disponible.** Volvió a aparecer, por tercera vez (ya había pasado en Entradas 4 y 5 de la bitácora). La IA no "aprende" entre sesiones y, salvo que se le indique en el prompt, repone esta propuesta cada vez porque es un patrón UX habitual en apps web. El grupo lo rechaza siempre con el mismo argumento: no existen equivalencias reales entre bases locales y públicas, el fallback silencioso sería engañoso.
- **Columnas de la tabla.** La IA sumó una columna que la HU no pide. Patrón recurrente: tiende a *"redondear"* un entregable incorporando campos razonables de dominio, aunque no estén en el catálogo. Para este TP el criterio es ceñirse a las columnas mínimas; se revisa después si corresponde ampliar.
- **Generación no pedida (login).** La IA generó una pantalla de login por costumbre de prototipado típico; patrón de *"completar el flujo"* que ya anotamos en Entradas anteriores. Hubo que recordarle el principio de diseño del proyecto.

---

## 4. Qué queda para los próximos ciclos

Este entregable corresponde al **primer ciclo (generación)**. Las correcciones que surjan de la evaluación interna del grupo o de la devolución de cátedra se van a aplicar en el ciclo siguiente, dejando constancia en este README y en la bitácora de uso de IA ([`../../uso-ia.md`](../../uso-ia.md)) de qué cambió y por qué.
