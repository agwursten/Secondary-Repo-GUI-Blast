# Maquetado HTML — Primer ciclo de generación con IA

Esta carpeta contiene el maquetado HTML del flujo de navegación del Investigador/a, generado en el **primer ciclo** del proceso de maquetado asistido por IA. Cada archivo corresponde a una de las pantallas definidas en el flujo de navegación del perfil ([`../user-profiles/investigador.md`](../user-profiles/investigador.md), sección 3) y lleva en el nombre las historias de usuario que respalda.

## Archivos

Cada pantalla aparece en dos versiones: `_inicial.html` (salida del primer ciclo tal como la devolvió la IA, sin modificaciones) y `_final.html` (versión ajustada tras el segundo ciclo, con los hallazgos de la evaluación heurística que el grupo aceptó aplicados — ver [`../heuristic-review/`](../heuristic-review/)).

| Pantalla del flujo | HUs cubiertas | Versión inicial (ciclo 1) | Versión final (ciclo adicional) |
|---|---|---|---|
| Nueva búsqueda — Secuencia query | `HU01_CU001_B`, `HU02_CU001_E1` | [`pantalla-01-carga-secuencia_HU01-HU02_inicial.html`](pantalla-01-carga-secuencia_HU01-HU02_inicial.html) | [`pantalla-01-carga-secuencia_HU01-HU02_final.html`](pantalla-01-carga-secuencia_HU01-HU02_final.html) |
| Nueva búsqueda — Configuración + validación | `HU03_CU002_B`, `HU04_CU002_A1`, `HU05_CU003_B`, `HU06_CU003_E1`, `HU07_CU003_E2` | [`pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_inicial.html`](pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_inicial.html) | [`pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_final.html`](pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_final.html) |
| Ejecución en progreso | `HU08_CU004_B`, `HU09_CU004_A1`, `HU10_CU004_E1` | [`pantalla-03-ejecucion_HU08-HU09-HU10_inicial.html`](pantalla-03-ejecucion_HU08-HU09-HU10_inicial.html) | [`pantalla-03-ejecucion_HU08-HU09-HU10_final.html`](pantalla-03-ejecucion_HU08-HU09-HU10_final.html) |
| Resultados · filtros · descarga | `HU11_CU005_B`, `HU12_CU006_B`, `HU13_CU007_B`, `HU14_CU007_A1` | [`pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_inicial.html`](pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_inicial.html) | [`pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_final.html`](pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_final.html) |

Las **14 HUs del catálogo** del TP1 que requieren interfaz quedan cubiertas por estos cuatro pares de archivos. La pantalla de autenticación mencionada en el flujo del perfil **no se maqueta** en esta iteración: no hay HU que la respalde y el principio de diseño del grupo es *"si una pantalla no está respaldada por alguna HU, no se maqueta"*. El resto del flujo asume sesión ya iniciada.

Cada archivo HTML muestra apilados el **estado primario** (camino feliz) y los **estados alternativos y de excepción** cubiertos por sus HUs, cada uno con una etiqueta visible que indica a qué HU y a qué criterio de aceptación corresponde. Esta decisión se tomó para que la evaluación visual pueda recorrer todos los estados sin necesidad de interactuar. En la implementación final solo un estado será visible al mismo tiempo.

### Por qué conservamos ambas versiones

El `_inicial.html` **no es un archivo viejo que haya que borrar**: es la línea base contra la que se verifica la evaluación heurística. Cualquiera que lea el repositorio puede abrir `_inicial.html` y `_final.html` lado a lado y confirmar que las diferencias se corresponden una a una con los hallazgos aceptados en los documentos de [`../heuristic-review/`](../heuristic-review/). Esa trazabilidad explícita es lo que la cátedra pide como núcleo pedagógico del segundo ciclo (TP2 sección 4.5).

---

## 1. Criterios definidos por el grupo antes de pedir a la IA

Antes de redactar el prompt, el grupo acordó los siguientes criterios para evitar que la IA eligiera por su cuenta decisiones que son de dominio del proyecto:

### 1.1 Tipo de sistema

- **Aplicación web** (SRS 1.3 fija *"Interfaz web"* en el alcance), específicamente una GUI para BLAST+.
- **Pensada para desktop/laptop** con navegador moderno; el perfil del Investigador/a lo marca explícitamente (*"el sistema no está pensado para uso cómodo en celular"* — [`investigador.md`](../user-profiles/investigador.md) 1.3). El maquetado se diseña para anchos típicos de desktop.

### 1.2 Lenguaje y framework del maquetado

- **HTML + CSS puro**, sin framework. Un archivo `.html` autocontenido por pantalla, con el CSS en una etiqueta `<style>` embebida, para que cada archivo se abra en cualquier navegador sin build-step.
- **Sin JavaScript** (ni interactividad real): el objetivo del primer ciclo es la maqueta de interfaz, no el prototipo funcional. Los distintos estados por HU se renderizan apilados en el mismo archivo con etiquetas visibles, en vez de intercambiarse por script.

### 1.3 Perfil de usuario y escenario de uso

- **Único actor con historias de usuario:** Investigador/a (ver [`investigador.md`](../user-profiles/investigador.md)).
- **Escenario de uso de referencia:** camino feliz construido alrededor que cierra el ciclo completo de valor y encadena naturalmente las HUs necesarias.
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
> Les paso el repositorio actual del proyecto LocalBlast (TP de Ingeniería de Software). El perfil de usuario ya está definido y validado en `docs/ui/user-profiles/investigador.md` — ahí están el escenario de uso de referencia y el flujo de navegación con las pantallas y las HUs que respaldan a cada una. El catálogo completo de 14 HUs está en `docs/requeriments/historias-usuario.md`, con sus criterios Given-When-Then; los RF-01 a RF-12 están en `docs/requeriments/srs.md` 6.
>
> Necesitamos el **maquetado HTML del flujo de navegación** correspondiente a las pantallas que lista `investigador.md` 3. Pedimos un archivo `.html` por pantalla, no un prototipo navegable: el objetivo de este primer ciclo es la maqueta visual.
>
> **Reglas que acordamos antes y queremos que respetes:**
>
> 1. **Una pantalla, un archivo HTML.** Nombres de archivo con el formato `pantalla-NN-<slug>_HU<X>-HU<Y>.html`, donde los HU listados son todos los que la pantalla cubre. Ejemplo del formato que pidió la cátedra: `pantalla-01-carga-secuencia_HU01-HU02.html`.
> 2. **No maquetar la pantalla de autenticación.** No tiene HU asociada y el principio de diseño del proyecto es *"si una pantalla no está respaldada por alguna HU, no se maqueta"*. El flujo arranca en "Nueva búsqueda — Secuencia query" asumiendo sesión ya iniciada; podés poner un chip de usuario en el header para dejarlo visible.
> 3. **HTML + CSS puro, sin framework, sin JS.** Cada archivo autocontenido, con el CSS en `<style>` embebido. Que se pueda abrir con doble-click sin servidor local ni build-step.
> 4. **Pensado para desktop/laptop.** No priorizar mobile; podés dejar que degrade razonablemente pero el ancho objetivo es desktop.
> 5. **Cada pantalla debe mostrar el estado primario (camino feliz) y los estados alternativos / de excepción** de las HUs que cubre, apilados en el mismo archivo, con una etiqueta visible por sección que diga a qué HU y a qué criterio de aceptación (CA-01, CA-02, …) corresponde cada estado. Esto nos permite revisar visualmente la cobertura sin tener que interactuar.
> 6. **Lenguaje y defaults del dominio.** Los parámetros pre-búsqueda (E-value, matriz, tamaño de palabra, gaps) tienen que verse *"recalculados según el programa BLAST elegido"* como pide RF-06: el default de `blastp` no es el de `blastn`. En la pantalla de configuración, mostrar la vista con `blastp` por defecto y dejar explícito que los números corresponden a ese programa.
> 7. **Pantalla de ejecución asíncrona.** Dejar visualmente evidente que el usuario puede seguir navegando mientras BLAST+ corre (barra lateral con el resto de la aplicación disponible y un chip de "corriendo", por ejemplo). Botón "Cancelar búsqueda" bien visible.
> 8. **Pantalla de resultados.** Tabla con las columnas mínimas que exige `HU11_CU005_B` CA-01 (hit ID, score, E-value observado, % identidad, % cobertura). Panel de filtros a un costado con identidad, cobertura, E-value y taxonomía; que se vea que son filtros post-búsqueda (no re-ejecutan BLAST). Selector de formato de descarga (CSV, JSON, FASTA, BLAST XML, tabular `-outfmt 6`) y botón Descargar que diga cuántos hits visibles descarga. Chip "Guardado en el historial" para la persistencia automática de `HU11`. Mostrar también el estado alternativo de `HU14_CU007_A1` (tabla vacía por filtros, descarga válida solo con metadatos).
> **Dejanos todos los archivos en `docs/ui/mockups/`** y agregá un `README.md` ahí mismo con el índice, los criterios que te pasamos acá, el prompt y un resumen de la respuesta.

---

## 3. Segundo ciclo (evaluación heurística) y ciclos adicionales

El trabajo del segundo ciclo —evaluación heurística con IA sobre cada HTML, revisión crítica del grupo sobre cada hallazgo, y los ciclos adicionales de ajuste que terminaron en los `_final.html`— está documentado en una carpeta dedicada, un documento por pantalla:

👉 [`../heuristic-review/`](../heuristic-review/)

Cada documento de esa carpeta incluye el prompt literal de la evaluación, la respuesta completa de la IA (las 10 heurísticas de Nielsen una por una), la decisión del grupo para cada hallazgo (aceptado/rechazado + justificación), y el prompt + respuesta del ciclo adicional de ajuste cuando lo hubo. La bitácora de IA (`docs/uso-ia.md`) tiene una entrada por cada ciclo (Entradas 18 y 19).
