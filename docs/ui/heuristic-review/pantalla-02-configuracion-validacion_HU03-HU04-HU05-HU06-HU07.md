# Evaluación heurística — Pantalla 2: Nueva búsqueda · Configuración y validación

- **Mockup inicial evaluado:** [`../mockups/pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_inicial.html`](../mockups/pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_inicial.html)
- **Mockup final tras ciclo adicional:** [`../mockups/pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_final.html`](../mockups/pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_final.html)
- **HUs cubiertas:** `HU03_CU002_B` (configuración completa), `HU04_CU002_A1` (base local no disponible), `HU05_CU003_B` (validación semántica), `HU06_CU003_E1` (parámetros fuera de rango), `HU07_CU003_E2` (combinación incompatible)
- **Perfil y escenario de referencia:** `docs/ui/user-profiles/investigador.md`

---

## 1. Primer ciclo — Generación del HTML (resumen)

El prompt completo y los criterios acordados por el grupo antes de pedirle a la IA la generación del maquetado están registrados en [`../mockups/README.md`](../mockups/README.md). No se repiten acá para no duplicar.

La IA entregó esta pantalla como [`pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_inicial.html`](../mockups/pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_inicial.html), con cinco estados apilados: formulario primario (programa `blastp`, modo remoto NCBI, defaults aplicados), estado posterior de validación exitosa, estado alternativo de BD local no disponible, estado de excepción de parámetros fuera de rango y estado de excepción de combinación programa/query/BD incompatible.

---

## 2. Segundo ciclo — Evaluación heurística con IA

### 2.1 Prompt utilizado

Conversación nueva con la IA. Se le adjuntaron el HTML inicial de la pantalla, el perfil del Investigador/a y las cinco HU que respalda la pantalla.

> **Prompt:**
>
> Actuá como especialista en interfaces de usuario. Te paso tres archivos:
>
> 1. `pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_inicial.html` — pantalla web (HTML+CSS, sin JS) de LocalBlast, una GUI para BLAST+. Es la **configuración y validación** de la búsqueda, cubre cinco HU: HU03 (configurar modo, BD, programa, parámetros), HU04 (base de datos local no disponible), HU05 (validación semántica exitosa), HU06 (parámetros fuera de rango), HU07 (combinación programa/query/BD incompatible). El archivo muestra apilados los cinco estados.
> 2. `investigador.md` — perfil del único actor principal. Nivel técnico es un **rango**: del estudiante que puede dudar frente a elegir `blastn` vs. `blastp` o fijar un E-value, al investigador sénior que elige matriz de sustitución de memoria.
> 3. `historias-usuario.md` — las cinco HU con criterios Given-When-Then.
>
> Evaluá la pantalla **heurística por heurística** según las **10 heurísticas de Nielsen**, teniendo en cuenta este perfil concreto. Para cada una indicá si **cumple / cumple parcialmente / incumple**, por qué, y una mejora si corresponde. Evaluá los cinco estados, no solo el primero.

### 2.2 Respuesta de la IA (completa)

**H1 — Visibilidad del estado del sistema. Cumple.**
El stepper mantiene el paso 2 activo con los pasos previos marcados como completados (`✓`). El resumen de la secuencia cargada arriba del formulario (`sp_P0A6F5.fasta · proteína · 548 aa`) deja claro contra qué se está configurando. El estado posterior a validar muestra un banner verde explícito y el aviso "si cambiás cualquier campo del formulario, el visto bueno se invalida" — eso es visibilidad de estado al nivel que `HU05_CU003_B` CA-02 exige.

**H2 — Correspondencia entre el sistema y el mundo real. Cumple.**
Lenguaje del dominio: modo local / remoto, `blastp` / `blastn` / `blastx` con una línea explicativa, BLOSUM, PAM, "penalización de gaps" apertura/extensión. El hint "modo local usa las bases del catálogo del laboratorio. Modo remoto invoca a BLAST+ con `-remote` contra NCBI" es exactamente el lenguaje que el investigador usa en su cabeza.

**H3 — Control y libertad del usuario. Cumple parcialmente.**
Botón "← Volver" visible en todos los estados, bien. El botón "Restaurar defaults" es útil pero es una acción destructiva que no pide confirmación: si el investigador sénior venía ajustando word-size y matriz a mano porque trabaja con una base muy particular, un click accidental le borra ese trabajo. Sugerencia: pedir confirmación antes de restaurar.

**H4 — Consistencia y estándares. Cumple.**
Dropdowns, radio buttons, campos de texto y `<details>` para la sección "Parámetros pre-búsqueda" son todos elementos estándar. La paleta y los botones son consistentes con la pantalla anterior. El banner verde para éxito, ámbar para advertencia y rojo para error siguen la convención aceptada.

**H5 — Prevención de errores. Cumple parcialmente.**
Hay varios aciertos: la lista de bases en modo local muestra el estado de cada una (`✓ lista`, `↻ actualizándose`, `✗ con error`), el resumen "Estado del catálogo: ✓ 2 listas, ↻ 1 actualizándose, ✗ 1 con error" avisa de un vistazo. Lo que no previene es el intento mismo de validar sin elegir una BD utilizable: en el estado alternativo de HU04, el botón "Validar búsqueda" aparece deshabilitado, pero no hay una explicación cerca del botón de **qué** falta para que se habilite. Un investigador que no vio la lista con cuidado se queda sin saber qué le piden corregir. Sugerencia: una pista "Validar está deshabilitado porque [X]".

**H6 — Reconocimiento en lugar de recuerdo. Cumple parcialmente.**
Las opciones de los dropdowns de programa y BD están todas listadas. El hint "valores por defecto para `blastp`" junto a la sección de parámetros marca que los números dependen del programa, sin tener que recordarlo. Lo que no está presente es la explicación de qué controla cada parámetro: "E-value máximo", "Matriz de sustitución", "Tamaño de palabra", "Penalización de gaps" son nombres que el investigador sénior reconoce; el estudiante del extremo bajo del perfil puede necesitar un recordatorio al vuelo. Sugerencia: tooltips con una línea explicativa en cada parámetro.

**H7 — Flexibilidad y eficiencia de uso. Cumple parcialmente.**
Para el investigador sénior, la sección "Parámetros pre-búsqueda" en `<details>` abierta por default es correcta (ve todo y ajusta). Para el estudiante, no hay un "modo guiado" ni plantillas pre-armadas. Dado el perfil, cubrir al sénior sin molestar al estudiante es lo prioritario; la ausencia del modo guiado no es un problema serio. Lo que sí falta es la posibilidad de **guardar una configuración** como plantilla para reusarla. Sugerencia: guardar/cargar presets.

**H8 — Diseño estético y minimalista. Cumple parcialmente.**
En el estado primario, el formulario está bien organizado. Lo que lastima la lectura es la **cantidad de estados apilados**: cinco secciones una debajo de la otra, cada una con su propio panel, convierten la pantalla en un documento más que en una interfaz. Entiendo que es una decisión del maquetado y que en producción solo se ve uno a la vez; en ese caso, cumple.

**H9 — Ayudar al usuario a reconocer, diagnosticar y recuperarse de errores. Cumple.**
Los mensajes de error son de muy buena calidad: en HU06 señalan el campo exacto, dicen el rango válido y explican la causa ("Para el programa `blastn`, el tamaño de palabra mínimo es 7. Subí el valor o cambiá el programa."). En HU07 enumeran las combinaciones válidas con lo que el investigador ya tiene cargado. Son mensajes diagnósticos, no genéricos — exactamente lo que pide el perfil.

**H10 — Ayuda y documentación. Incumple.**
No hay ningún elemento de ayuda contextual. Para el estudiante del extremo bajo del perfil, los nombres "BLOSUM62", "PAM30", "word size 3" no son autoevidentes. Un tooltip "?" al lado de cada parámetro con una línea explicativa cerraría el loop sin desordenar la pantalla.

---

## 3. Revisión crítica del grupo

### H3 — Confirmación antes de "Restaurar defaults"

- **Decisión del grupo:** **aceptado.** El argumento conecta con un patrón del laboratorio: el investigador sénior que corre contra una base particular tiene valores pensados que no quiere perder. Es la misma lógica que la que usamos en la pantalla 1 para "Reemplazar secuencia", y es coherente seguir el mismo criterio. Entra al ciclo adicional.

### H5 — Explicación de por qué "Validar búsqueda" está deshabilitado

- **Decisión del grupo:** **aceptado.** El hallazgo es puntual pero importante: la `HU04_CU002_A1` termina devolviendo al investigador al paso 2 con la lista actualizada, y el flujo quedaría trabado si no se entiende por qué el botón "Validar" sigue grisado. Una línea de pista explícita cerca del botón resuelve el problema sin tocar el flujo. Entra al ciclo adicional.

### H6 + H10 — Tooltips de ayuda en los parámetros pre-búsqueda

- **Decisión del grupo:** **aceptado.** Los dos hallazgos piden lo mismo desde ángulos distintos (reconocimiento vs. documentación), igual que pasó en la pantalla 1. La solución es un ícono `?` junto a cada etiqueta de parámetro con una línea de explicación, visible al pasar el mouse. Decidimos usar CSS `::after` + `attr(data-tip)` para no romper la regla de "sin JS". Entra al ciclo adicional, fusionados.

### H7 — Guardar presets de configuración

- **Decisión del grupo:** **rechazado por ahora.** No está respaldado por ninguna HU del catálogo del TP1 — y el principio del grupo es no maquetar lo que no tiene HU detrás. Lo anotamos como ampliación futura del producto.

### H8 — Densidad excesiva de la pantalla apilada

- **Decisión del grupo:** **rechazado como hallazgo.** La propia IA aclaró que "si en producción solo se ve uno a la vez, cumple", y esa **es** la realidad de la implementación — los estados apilados son un recurso del maquetado para que un revisor pueda verlos sin interactuar, no la UI final.

### Heurísticas donde la IA dijo "cumple" (H1, H2, H4, H9)

- **Decisión del grupo:** acordamos. En particular H9 nos interesa dejar reflejado: los mensajes diagnósticos de HU06/HU07 fueron un acierto del primer ciclo y la IA del segundo ciclo lo validó explícitamente.

### Resumen de la revisión

| Heurística | Veredicto IA | Decisión grupo | Entra al ciclo adicional |
|---|---|---|---|
| H1 — Visibilidad | cumple | — | — |
| H2 — Mundo real | cumple | — | — |
| H3 — Control y libertad | parcial | **aceptado** (confirmar "Restaurar defaults") | **sí** |
| H4 — Consistencia | cumple | — | — |
| H5 — Prevención de errores | parcial | **aceptado** (pista de por qué Validar está deshabilitado) | **sí** |
| H6 — Reconocimiento | parcial | **aceptado** (fusionado con H10) | **sí** |
| H7 — Flexibilidad | parcial | rechazado (presets no respaldados por HU) | no |
| H8 — Minimalista | parcial | rechazado (artefacto del maquetado, no de la UI final) | no |
| H9 — Recuperación de errores | cumple | — | — |
| H10 — Ayuda y documentación | incumple | **aceptado** (tooltips, fusionado con H6) | **sí** |

---

## 4. Ciclo adicional — Ajuste de la interfaz

### 4.1 Prompt del ajuste

> **Prompt:**
>
> Sobre `pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_inicial.html`, aplicá tres cambios y devolveme `_final.html`. Mantené todo lo demás y la regla "sin JS":
>
> 1. **H6 + H10.** Agregá un ícono `?` tipo "help" junto a cada una de las cuatro etiquetas de parámetros pre-búsqueda (E-value máximo, matriz de sustitución, tamaño de palabra, penalización de gaps). Cada ícono muestra, al pasar el mouse, una línea explicativa breve (menos de 300 caracteres), dirigida a alguien que entiende BLAST en general pero no se acuerda del parámetro puntual. Implementalo con CSS puro usando `::after` + `attr(data-tip)`; que al menos uno de los tooltips se vea expandido por default (clase `show-tip`) para que un revisor del maquetado pueda verlo en papel sin tener que mover el mouse.
>
> 2. **H3.** Debajo del botón "Restaurar defaults" (en el estado primario), agregá un bloque de confirmación simulando el estado posterior al click: mensaje "Esto va a sobrescribir los valores que modificaste manualmente con los defaults de `blastp`" y dos botones "Mantener mis valores" (secundario) y "Sí, restaurar defaults" (warning, ámbar).
>
> 3. **H5.** En el estado alternativo de HU04 (base de datos local no disponible), agregá cerca del botón "Validar búsqueda" (que está deshabilitado) una pista explícita de **por qué** está deshabilitado: "Validar búsqueda está deshabilitado porque falta elegir una base de datos utilizable. Elegí una marcada como *lista*".
>
> Actualizá la nota del maquetado al pie para que explique los tres cambios y referencie este documento.

### 4.2 Respuesta de la IA (resumen y modificaciones aplicadas)

La IA devolvió el HTML con los tres cambios. Lo que quedó en [`pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_final.html`](../mockups/pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_final.html):

- **CSS nuevo:** `.help-icon` + `.help-icon::after` + `.help-icon.show-tip` para los tooltips; `.confirm-restore` + `.btn-warning` para la confirmación del Restaurar defaults; `.validate-hint` para la pista en el estado de BD no disponible.
- **Panel de parámetros pre-búsqueda:** cuatro íconos `?` agregados, uno por parámetro. El del E-value tiene la clase `show-tip` para que se vea expandido en el maquetado (lo acordamos para la revisión en papel).
- **Bloque de confirmación de "Restaurar defaults":** agregado como sección apilada en el estado primario, con los dos botones.
- **Estado alternativo HU04:** se añadió el bloque `.validate-hint` sobre el botón Validar, con el texto exacto.
- **Nota del maquetado:** reescrita, lista los tres cambios y apunta a este documento.

### 4.3 Qué modificamos sobre la devolución de la IA

- **Texto del tooltip de E-value.** La primera versión de la IA decía solo "Umbral de significancia estadística para los hits". Lo expandimos a la versión actual, que menciona explícitamente el default del `blastp` y el valor típico cuando se quiere ser más estricto, porque sin esos dos números concretos el tooltip quedaba poco útil para alguien que no viene del día a día de BLAST.
- **Texto del tooltip de matriz.** Lo mismo: pedimos que mencione BLOSUM62 y PAM30 con un caso de uso para cada una, no que las defina genéricamente. El tooltip es espacio escaso y nos interesa que oriente la decisión concreta.

### 4.4 Qué descartamos del ajuste

- Una propuesta de la IA, en una variante intermedia, de agregar también tooltips a los dropdowns de "Modo de ejecución" y "Programa BLAST". La rechazamos: los nombres "Remoto (NCBI) / Local" y la lista de programas con su línea de descripción (`blastp — proteína vs. proteína`) ya son autoexplicativos. Más tooltips suman ruido sin agregar información.

### 4.5 Resultado

El `_final.html` cubre los tres hallazgos aceptados. El `_inicial.html` queda como línea base para la verificación.
