# Evaluación heurística — Pantalla 1: Nueva búsqueda · Secuencia query

- **Mockup inicial evaluado:** [`../mockups/pantalla-01-carga-secuencia_HU01-HU02_inicial.html`](../mockups/pantalla-01-carga-secuencia_HU01-HU02_inicial.html)
- **Mockup final tras ciclo adicional:** [`../mockups/pantalla-01-carga-secuencia_HU01-HU02_final.html`](../mockups/pantalla-01-carga-secuencia_HU01-HU02_final.html)
- **HUs cubiertas:** `HU01_CU001_B` (carga de la secuencia query, inferencia de alfabeto), `HU02_CU001_E1` (rechazo con mensaje diagnóstico)
- **Perfil y escenario de referencia:** `docs/ui/user-profiles/investigador.md`

---

## 1. Primer ciclo — Generación del HTML (resumen)

El prompt completo y los criterios acordados por el grupo antes de pedirle a la IA la generación del maquetado están registrados en [`../mockups/README.md`](../mockups/README.md) (secciones 1 y 2). No se repiten acá para evitar la duplicación: ese README es la fuente única del ciclo 1.

Lo que la IA entregó para esta pantalla es exactamente el archivo [`pantalla-01-carga-secuencia_HU01-HU02_inicial.html`](../mockups/pantalla-01-carga-secuencia_HU01-HU02_inicial.html), que el grupo tomó tal cual para abrir el ciclo 2 (evaluación heurística).

---

## 2. Segundo ciclo — Evaluación heurística con IA

### 2.1 Prompt utilizado

Se abrió una **conversación nueva** con la IA (sin arrastrar el contexto del ciclo de generación) y se le adjuntaron tres archivos: el HTML inicial de la pantalla, el perfil del Investigador/a y el catálogo de historias de usuario. El prompt literal fue:

> **Prompt:**
>
> Actuá como especialista en interfaces de usuario. Te paso tres archivos:
>
> 1. `pantalla-01-carga-secuencia_HU01-HU02_inicial.html` — una pantalla web (HTML+CSS, sin JS) de nuestro proyecto LocalBlast, una GUI para BLAST+. La pantalla cubre la **carga de la secuencia query** (HU01_CU001_B) y el **rechazo de secuencia con formato inválido** (HU02_CU001_E1). Para que puedas verla sin interactuar, el archivo muestra apilados cuatro estados: formulario vacío, secuencia cargada correctamente, excepción por carácter inválido, excepción por FASTA sin cuerpo.
> 2. `investigador.md` — el perfil del único actor principal del sistema. Importante: su nivel técnico es un **rango** que va de estudiante de grado (puede dudar frente a elegir programa BLAST o fijar un E-value) a investigador sénior (quiere control de parámetros y velocidad). Están explícitas también sus limitaciones y frustraciones.
> 3. `historias-usuario.md` — las HU que respalda la pantalla, con criterios Given-When-Then.
>
> Necesitamos que evalúes esta pantalla **heurística por heurística** según las **10 heurísticas de usabilidad de Nielsen**, teniendo en cuenta este perfil concreto y **no** un usuario genérico. Para cada heurística:
>
> - Indicá si se **cumple**, se **cumple parcialmente** o se **incumple**.
> - Fundamentá por qué, con referencias concretas a elementos del HTML (banner de error, dropzone, textarea, etc.) y, cuando aplique, al perfil o a la HU puntual.
> - Si corresponde, sugerí una mejora concreta.
>
> Evaluá los **cuatro estados apilados**, no solo el formulario vacío. Dejá el veredicto por heurística en formato breve y accionable; no inventes problemas donde la pantalla claramente cumple.

### 2.2 Respuesta de la IA (completa)

> La respuesta se transcribe literal, respetando el orden de las diez heurísticas y la redacción de la IA. El grupo discute cada punto en la sección 3.

**H1 — Visibilidad del estado del sistema. Cumple parcialmente.**
El stepper superior ("Secuencia query → Configuración → Ejecución → Resultados") deja claro en qué paso del flujo está el investigador, y la tarjeta verde de "✓ Secuencia cargada correctamente" muestra con precisión qué sabe el sistema de la carga (fuente, registros, alfabeto, longitud). Lo que no está representado es el momento en que el investigador **arrastra o selecciona** el archivo: entre esos dos extremos no hay feedback intermedio, y para archivos grandes (hasta 10 MB según la zona de drop) eso puede dejar al usuario sin saber si pasó algo. Sugerencia: estado intermedio "subiendo…" o barra de progreso de upload.

**H2 — Correspondencia entre el sistema y el mundo real. Cumple.**
El lenguaje es el del dominio: FASTA, alfabeto (ADN / ARN / proteína), carácter inválido, longitud en `aa`. Para el perfil del Investigador/a esto es apropiado. No se abusa de jerga de UI genérica. El término "Confirmar carga" para el botón primario es preciso.

**H3 — Control y libertad del usuario. Cumple parcialmente.**
Hay botón "Cancelar" y botón "Limpiar", lo cual está bien para un formulario. Lo que falta es protección contra una acción destructiva: el link "Reemplazar secuencia" en la tarjeta de secuencia cargada reemplazaría en silencio una secuencia que el investigador recién vinculó al resto del formulario — y según el escenario del perfil, esa secuencia es la base de todo lo que sigue. Sugerencia: pedir confirmación explícita antes de reemplazar.

**H4 — Consistencia y estándares. Cumple.**
Botón primario azul, secundario blanco con borde, ghost sin fondo: coherente con convenciones web. La zona de arrastre con línea punteada es un patrón estándar. El banner de error en rojo con icono "✗" también. No hay inconsistencias.

**H5 — Prevención de errores. Cumple parcialmente.**
La zona de drop lista los formatos aceptados y el tamaño máximo antes de que el investigador suba nada, lo cual previene errores evidentes. El textarea tiene un placeholder con un FASTA mínimo, también preventivo. Lo que falta es validación en el momento de pegar: la pantalla espera a "Confirmar carga" para avisar sobre un carácter inválido, cuando podría destacarlo apenas se pega el texto. Para el estudiante de grado del extremo bajo del perfil, un indicador en vivo ahorraría un ciclo. Sugerencia: validación on-blur en el textarea.

**H6 — Reconocimiento en lugar de recuerdo. Cumple parcialmente.**
Los formatos aceptados (`.fasta`, `.fa`, `.fna`, `.faa`, `.txt`) están visibles, el tamaño máximo también, el placeholder del textarea da un ejemplo. Lo que no se ve es un recordatorio de **cómo** luce un FASTA válido fuera del placeholder (que es gris claro y pequeño). El investigador sénior lo recuerda; el estudiante quizás no. Sugerencia: un ejemplo de FASTA visible siempre, no solo como placeholder dentro del textarea.

**H7 — Flexibilidad y eficiencia de uso. Cumple parcialmente.**
Para el estudiante que carga por primera vez, la dupla "arrastrar archivo / pegar texto" es correcta. Para el investigador sénior que usa esta pantalla todos los días, no hay atajos: no hay "pegar último FASTA usado", no hay drag-and-drop desde la terminal, no hay atajo de teclado para "Confirmar carga". Dado que el perfil contempla "uso cotidiano durante proyectos de investigación activos", esta ausencia pesa. Sugerencia: historial de últimas secuencias cargadas; atajo Ctrl+Enter para confirmar.

**H8 — Diseño estético y minimalista. Cumple.**
La paleta es sobria, hay suficiente espacio en blanco, no hay elementos decorativos. Para una herramienta académica es el tono correcto. Las etiquetas "ESTADO POSTERIOR · HU01_CU001_B · CA-01" sobre cada panel apilado son del maquetado, no van en la versión final.

**H9 — Ayudar al usuario a reconocer, diagnosticar y recuperarse de errores. Cumple parcialmente.**
El error por carácter inválido es excelente: nombra el carácter concreto (`1`), su posición (`línea 3, columna 42`) y la causa probable ("un número de posición o un carácter de puntuación al copiar"). El error de "FASTA con encabezado sin cuerpo", en cambio, se queda a mitad de camino: dice qué está mal pero no muestra qué se esperaría. Para alguien del extremo bajo del perfil, un mini-ejemplo del formato correcto cerraría el loop. Sugerencia: incluir un ejemplo mínimo del formato esperado en el propio banner del error.

**H10 — Ayuda y documentación. Incumple.**
La pantalla asume que el investigador sabe qué es un FASTA. Para el extremo sénior del perfil, correcto. Para el extremo estudiantil, no hay dónde ir si duda del formato: no hay link a documentación, ni tooltip, ni popover. El placeholder del textarea no es documentación, es un hint que desaparece al escribir. Sugerencia: link "¿qué es un FASTA?" o popover inline con ejemplo del formato.

---

## 3. Revisión crítica del grupo

Para cada hallazgo, discutimos entre nosotros si corresponde al Investigador/a de este proyecto y a esta pantalla concreta, y decidimos aceptarlo o rechazarlo.

### H1 — Feedback intermedio durante la carga de archivo

- **Hallazgo IA:** cumple parcialmente; falta estado "subiendo..." para archivos grandes.
- **Decisión del grupo:** **rechazado.** El archivo FASTA de proteína del escenario de referencia pesa decenas de KB, no 10 MB. Para los casos del día a día del perfil (secuencia individual que querés alinear), el upload es instantáneo y agregar un indicador de progreso introduce un parpadeo innecesario. Si el laboratorio empieza a subir queries grandes (varios cromosomas, por ejemplo) habrá que revisar la decisión, pero no es el caso de las HU del TP1. Lo registramos como posible mejora futura, sin ciclo adicional ahora.

### H3 — Confirmación antes de reemplazar la secuencia cargada

- **Hallazgo IA:** cumple parcialmente; "Reemplazar secuencia" es un link que no pide confirmación.
- **Decisión del grupo:** **aceptado.** El argumento de la IA conecta con una decisión real del dominio: cuando el investigador reemplaza la secuencia, la configuración de `CU002` (programa BLAST, parámetros) que se armó para la secuencia anterior puede dejar de tener sentido (ejemplo típico: pasa de proteína a nucleótido y el programa `blastp` ya no es válido). La `HU01_CU001_B` CA-03 dice explícitamente que "la secuencia sigue disponible sin necesidad de volver a cargarla", y la operación inversa —tirar la secuencia a la basura— merece confirmación. Entra al ciclo adicional.

### H5 — Validación en vivo del textarea al pegar

- **Hallazgo IA:** cumple parcialmente; validar on-blur ahorraría un ciclo al estudiante.
- **Decisión del grupo:** **rechazado para esta iteración.** No por falta de utilidad —la propuesta es sana— sino porque todo el maquetado del TP2 se acordó explícitamente **sin JavaScript** (ver `docs/ui/mockups/README.md` sección 1.2). Validación en vivo necesita JS y queda para la fase de implementación. Lo anotamos como requerimiento del front cuando se implemente, no como cambio del maquetado.

### H6 + H10 — Ejemplo de FASTA siempre visible / documentación de qué es un FASTA

- **Hallazgos IA:** H6 cumple parcialmente, H10 incumple. Ambos piden lo mismo desde ángulos distintos: un ejemplo de FASTA visible que no desaparezca.
- **Decisión del grupo:** **aceptado.** Los dos hallazgos tocan el mismo problema real del extremo bajo del perfil: "entiende qué es una secuencia FASTA" (per el perfil) **no** es lo mismo que "sabe de memoria cómo luce una". Un popover con un FASTA mínimo (encabezado + un par de líneas de secuencia) resuelve ambos hallazgos sin inflar la pantalla. En vez de dos cambios, lo tratamos como uno. Entra al ciclo adicional.

### H7 — Flexibilidad para el investigador sénior

- **Hallazgo IA:** cumple parcialmente; faltan atajos y reutilización de últimas secuencias.
- **Decisión del grupo:** **rechazado por ahora.** La reutilización de la última secuencia es efectivamente útil pero no está respaldada por ninguna HU del catálogo del TP1 — y el principio de diseño del grupo es "nada que no esté respaldado por HU se maqueta". Los atajos de teclado son razonables pero no exigidos. Dejamos ambos anotados en el backlog del proyecto; no se tocan en este ciclo.

### H9 — Mini-ejemplo del formato esperado en el error de FASTA sin cuerpo

- **Hallazgo IA:** cumple parcialmente; el error no muestra ejemplo del formato correcto.
- **Decisión del grupo:** **aceptado.** Es consistente con la decisión que ya tomamos para H6/H10, aplicada ahora al punto de recuperación de un error específico. El criterio es el mismo: el investigador del extremo bajo del perfil se beneficia de ver el formato correcto en el mismo lugar donde se le dice que su input está mal. Entra al ciclo adicional.

### Heurísticas donde la IA dijo "cumple" (H2, H4, H8)

- **Decisión del grupo:** las revisamos puntualmente y acordamos con el veredicto. No hay cambios.

### Resumen de la revisión

| Heurística | Veredicto IA | Decisión grupo | Entra al ciclo adicional |
|---|---|---|---|
| H1 — Visibilidad | parcial | rechazado (upload rápido para los casos reales) | no |
| H2 — Mundo real | cumple | — | — |
| H3 — Control y libertad | parcial | **aceptado** (confirmar reemplazo) | **sí** |
| H4 — Consistencia | cumple | — | — |
| H5 — Prevención de errores | parcial | rechazado (requiere JS, fuera de alcance del maquetado) | no |
| H6 — Reconocimiento | parcial | **aceptado** (fusionado con H10) | **sí** |
| H7 — Flexibilidad | parcial | rechazado (no respaldado por HU del TP1) | no |
| H8 — Minimalista | cumple | — | — |
| H9 — Recuperación de errores | parcial | **aceptado** (ejemplo en banner del error) | **sí** |
| H10 — Ayuda y documentación | incumple | **aceptado** (fusionado con H6) | **sí** |

---

## 4. Ciclo adicional — Ajuste de la interfaz

### 4.1 Prompt del ajuste

> **Prompt:**
>
> Sobre el mismo `pantalla-01-carga-secuencia_HU01-HU02_inicial.html` que te pasé, aplicá los siguientes tres cambios y devolveme la versión ajustada como `_final.html`. Mantené todo lo demás (estructura, estados apilados, variables CSS, etiquetas de estado), y mantené la regla de "sin JavaScript":
>
> 1. **H6 + H10 fusionados.** Agregá un popover de ayuda "¿Qué es un FASTA?" visible siempre junto al título "Secuencia query" del panel principal, con un bloque mono-espaciado que muestre un FASTA mínimo bien formado (encabezado con `>` y un par de líneas de secuencia de proteína). Que no sea solo tooltip al hover, porque sin JS no se puede garantizar accesibilidad al tooltip; mostrá el ejemplo expandido en un recuadro inline.
>
> 2. **H3.** Debajo de la tarjeta "✓ Secuencia cargada correctamente", agregá un bloque de confirmación que simule el estado posterior al click del link "Reemplazar secuencia": mensaje "Si reemplazás la secuencia actual, perdés la configuración vinculada a esta carga" y dos botones "Mantener la actual" (secundario) y "Sí, reemplazar" (warning, no destructivo). El bloque se muestra apilado como un estado más del maquetado.
>
> 3. **H9.** En el banner del estado de excepción "FASTA con encabezado sin cuerpo" (HU02_CU001_E1 CA-02), agregá debajo del texto del error el mismo recuadro mono-espaciado con el FASTA mínimo bien formado, para que el investigador vea en el mismo lugar qué se esperaba.
>
> Actualizá al final la "Nota del maquetado" para que explique qué cambió respecto a `_inicial.html` y referencie este documento (`docs/ui/heuristic-review/pantalla-01-carga-secuencia_HU01-HU02.md`).

### 4.2 Respuesta de la IA (resumen y modificaciones aplicadas)

La IA devolvió el archivo con los tres cambios aplicados tal como se los pedimos, más la nota del maquetado reescrita. Los cambios concretos que quedaron en [`pantalla-01-carga-secuencia_HU01-HU02_final.html`](../mockups/pantalla-01-carga-secuencia_HU01-HU02_final.html):

- **CSS nuevo:** `.help-link`, `.help-box` (recuadro con el ejemplo FASTA), `.confirm-replace` + `.btn-warning` (bloque de confirmación de reemplazo).
- **Panel "Secuencia query":** se añadió el link "¿Qué es un FASTA?" junto al título y, debajo del hint existente, el recuadro con el FASTA de ejemplo (header `>sp|P0A6F5|CH60_ECOLI` + 3 líneas de secuencia).
- **Tarjeta "secuencia cargada":** se añadió el bloque de confirmación de reemplazo con los dos botones.
- **Banner de excepción CA-02:** se añadió el recuadro con el mini FASTA como ejemplo del formato esperado.
- **Nota del maquetado:** reescrita para listar los tres cambios y apuntar a este documento.

### 4.3 Qué modificamos sobre la devolución de la IA

- **Expansión del ejemplo del popover.** La IA puso un FASTA de 2 líneas de secuencia; lo extendimos a 3 líneas para que el ejemplo cubra el caso típico del laboratorio (secuencia que no cabe en una sola línea) y para que la indentación de las líneas de continuación sea evidente.
- **Botón de confirmación.** La IA lo había puesto como `btn-primary` (azul). Lo cambiamos a `btn-warning` (ámbar) porque reemplazar es una acción con efecto destructivo sobre la configuración vinculada, no una acción "feliz". El azul podía normalizar la operación.

### 4.4 Qué descartamos del ajuste

Nada en esta iteración: los tres cambios acordados en la sección 3 se aplicaron íntegramente.

### 4.5 Resultado

El `_final.html` queda como el entregable de esta pantalla. El `_inicial.html` se conserva en el repo como insumo verificable de la evaluación: cualquier revisor puede abrir ambos lado a lado y constatar que las tres modificaciones corresponden a los tres hallazgos aceptados.
