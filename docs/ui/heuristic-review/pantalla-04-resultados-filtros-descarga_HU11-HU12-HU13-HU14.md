# Evaluación heurística — Pantalla 4: Resultados · filtros · descarga

- **Mockup inicial evaluado:** [`../mockups/pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_inicial.html`](../mockups/pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_inicial.html)
- **Mockup final tras ciclo adicional:** [`../mockups/pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_final.html`](../mockups/pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_final.html)
- **HUs cubiertas:** `HU11_CU005_B` (tabla y persistencia automática), `HU12_CU006_B` (filtros post-búsqueda), `HU13_CU007_B` (descarga en formato), `HU14_CU007_A1` (descarga con tabla vacía)
- **Perfil y escenario de referencia:** `docs/ui/user-profiles/investigador.md`

---

## 1. Primer ciclo — Generación del HTML (resumen)

El prompt completo y los criterios del grupo del primer ciclo están registrados en [`../mockups/README.md`](../mockups/README.md).

La IA entregó [`pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_inicial.html`](../mockups/pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_inicial.html) con dos estados apilados: estado primario con 12 de 54 alineamientos visibles bajo filtros de identidad ≥ 80% y cobertura ≥ 60%, y estado alternativo de HU14 con cero hits visibles por filtros demasiado estrictos (identidad ≥ 99%).

---

## 2. Segundo ciclo — Evaluación heurística con IA

### 2.1 Prompt utilizado

Conversación nueva. Adjuntos: HTML inicial, perfil del Investigador/a y las cuatro HU cubiertas.

> **Prompt:**
>
> Actuá como especialista en interfaces de usuario. Te paso tres archivos:
>
> 1. `pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_inicial.html` — pantalla de LocalBlast (GUI para BLAST+) correspondiente a **resultados**, **filtros post-búsqueda** y **descarga**. Cubre cuatro HU: HU11 (tabla con columnas mínimas y persistencia automática en el historial), HU12 (filtros interactivos que se aplican sin re-ejecutar BLAST), HU13 (descarga del subconjunto visible en el formato elegido), HU14 (descarga válida aunque la tabla esté vacía por filtros). El archivo muestra apilados dos estados: tabla filtrada con 12/54 hits visibles, y tabla vacía por filtros demasiado estrictos.
> 2. `investigador.md` — perfil del único actor principal, con su rango de nivel técnico.
> 3. `historias-usuario.md` — las cuatro HU con criterios Given-When-Then.
>
> Puntos de dominio importantes que vas a necesitar al evaluar:
>
> - Los filtros se aplican **sobre el conjunto crudo original**, no sobre el filtro anterior. Es una decisión fuerte del dominio: aflojar un filtro recupera hits previos sin re-ejecutar BLAST.
> - El **historial (D2) nunca se modifica** por filtros ni por descarga: siempre guarda los 54 crudos.
> - Los **cinco formatos** de descarga tienen propósitos distintos (CSV, JSON, FASTA, BLAST XML, Tabular `-outfmt 6`); el usuario sénior sabe distinguirlos de memoria, el estudiante quizás no.
>
> Evaluá la pantalla **heurística por heurística** según las **10 heurísticas de Nielsen**, con el perfil concreto en mente. Para cada una: **cumple / parcial / incumple**, por qué, y una mejora si corresponde. Evaluá los dos estados.

### 2.2 Respuesta de la IA (completa)

**H1 — Visibilidad del estado del sistema. Cumple.**
Mucha señalización explícita: "Mostrando 12 de 54 alineamientos", el badge "2 filtros activos", el chip verde "Guardado en el historial · 14:34:21", la línea de metadatos superior (query, programa, base, E-value máx, matriz, timestamp), y el botón "Descargar 12 hits visibles" que cambia el número según los filtros. En el estado alternativo (tabla vacía), "Mostrando 0 de 54" es igualmente explícito. La separación entre conjunto crudo y vista filtrada se ve a simple vista.

**H2 — Correspondencia entre el sistema y el mundo real. Cumple.**
Las columnas son las que el investigador espera (Hit ID, Descripción, Score, E-value obs., % Identidad, % Cobertura). Los filtros usan los nombres de siempre. Los formatos de descarga también (BLAST XML, Tabular `-outfmt 6`).

**H3 — Control y libertad del usuario. Cumple parcialmente.**
El panel de filtros deja al investigador ajustar cualquier umbral en cualquier momento, bien. Lo que falta en jerarquía visual es el **deshacer de filtros**: "Limpiar filtros" aparece como un link pequeño subrayado, abajo a la derecha del panel, con la misma tipografía que los textos de ayuda. Para el escenario donde el investigador se da cuenta de que apretó demasiado y quiere empezar de nuevo, ese link es demasiado tímido. Sugerencia: botón real, con jerarquía propia.

**H4 — Consistencia y estándares. Cumple.**
Los componentes son los esperados: panel lateral de filtros + tabla principal, sliders de rango para umbrales porcentuales, input de texto para E-value y taxonomía, radio buttons para formatos, botón de descarga primario. Las barras horizontales junto a los porcentajes son un refuerzo visual del número, no un reemplazo — bien.

**H5 — Prevención de errores. Cumple parcialmente.**
El input del E-value es un campo de texto libre (`value="1e-10"`) sin validación visible — un valor como `abc` o `-5` no se rechaza en el formulario. Para el estudiante del extremo bajo del perfil, es fácil escribir algo que después no filtre nada. En producción esto se maneja con validación en vivo, pero al menos el placeholder podría guiar más. El resto de los filtros (sliders de porcentaje) sí previenen rangos inválidos por diseño.

**H6 — Reconocimiento en lugar de recuerdo. Cumple parcialmente.**
Las columnas de la tabla tienen nombre pero no definición: "E-value obs." es el E-value **observado** (distinto del E-value máximo que fue filtro pre-búsqueda), y esa distinción es relevante para no confundirse al leer. El estudiante quizás no la haga. Lo mismo con "Score" (bruto, no E-value). Sugerencia: tooltip con una línea definitoria en cada encabezado. Igual con los cinco formatos de descarga: los nombres son autoevidentes para el sénior, no para el estudiante — un tooltip con "cuándo usar cada uno" sería valioso.

**H7 — Flexibilidad y eficiencia de uso. Cumple.**
Para el sénior: cinco formatos de descarga cubren todos los pipelines plausibles. Los sliders son más rápidos que escribir números. La descarga con metadatos permite reconstruir el contexto fuera del sistema (lo pide HU13 CA-01). Para el estudiante: el camino por default (CSV, defaults, descarga) funciona sin tener que decidir nada técnico.

**H8 — Diseño estético y minimalista. Cumple parcialmente.**
El layout de dos columnas (filtros a la izquierda, tabla a la derecha) es claro y jerárquico. La tabla no abusa de colores. Las barras horizontales de identidad y cobertura, muy chicas, podrían dividir atención con el número al lado — en una revisión en papel se ven algo cargadas, pero en pantalla ayudan a comparar hits de un vistazo. En equilibrio, aceptable.

**H9 — Ayudar al usuario a reconocer, diagnosticar y recuperarse de errores. Cumple parcialmente.**
El estado alternativo de tabla vacía por filtros es informativo ("Ningún hit supera los filtros vigentes. La búsqueda devolvió 54 alineamientos crudos — podés aflojar los filtros para verlos de nuevo") y sugiere qué hacer ("probá bajar el umbral de identidad o quitar el filtro taxonómico"). Lo que no está es un camino de **un click** para salir de ese estado: el investigador tiene que ir al panel de filtros y ajustar manualmente los umbrales. Para un error del propio usuario (apretó demasiado), eso es tolerable; para la frustración de ver cero resultados sin saber por qué fallaron los umbrales, sumar botones de sugerencia accionables ("Bajar identidad a ≥ 80%", "Aflojar E-value a ≤ 1e-10", "Limpiar todos los filtros") cerraría el ciclo rápido.

**H10 — Ayuda y documentación. Incumple.**
Igual que en pantallas anteriores, no hay documentación contextual. Los conceptos "E-value observado", "Score", "Tabular (-outfmt 6)", "BLAST XML" son recordados por el sénior y poco por el estudiante. Un tooltip breve en cada encabezado de columna y en cada opción de formato cerraría el gap sin romper la estética sobria.

---

## 3. Revisión crítica del grupo

### H3 — Jerarquía visual del botón "Limpiar filtros"

- **Decisión del grupo:** **aceptado.** Es un caso claro del principio "una acción destructiva de alta frecuencia merece su botón". En el escenario del perfil el investigador ajusta y afloja filtros con fluidez; necesita que "volver a cero" sea tan visible como "aplicar". Entra al ciclo adicional.

### H5 — Validación del input de E-value

- **Decisión del grupo:** **rechazado para esta iteración.** Mismo motivo que en la pantalla 1: la validación en vivo requiere JavaScript, y el maquetado del TP2 se acordó sin JS. Lo anotamos como requerimiento del front en la implementación.

### H6 + H10 — Tooltips en encabezados de columna y en formatos de descarga

- **Decisión del grupo:** **aceptado.** Es la misma decisión que tomamos en la pantalla 2 para los parámetros pre-búsqueda, aplicada ahora a resultados. Los dos hallazgos piden lo mismo desde ángulos distintos (reconocimiento vs. documentación) y se resuelven con una sola acción: íconos `?` + tooltips CSS. Entra al ciclo adicional, fusionados.

### H9 — Sugerencias accionables en el estado vacío

- **Decisión del grupo:** **aceptado.** El hallazgo encaja con el perfil: el investigador sénior quiere velocidad para iterar sobre umbrales, no quiere mover tres sliders a mano cuando ve una tabla vacía. Y para el estudiante, el hallazgo tiene además valor pedagógico: ver qué filtro se sugiere aflojar primero le enseña por dónde empezar a aflojar. Entra al ciclo adicional.

### H8 — Barras horizontales de identidad y cobertura

- **Decisión del grupo:** **rechazado como hallazgo**, pero con matiz. La propia IA se contradice ("en papel se ven cargadas, en pantalla ayudan a comparar") y el grupo coincide con la lectura en pantalla: las mini-barras son un refuerzo visual útil para comparar hits de un vistazo (el ojo detecta el patrón antes que leer el número). No las sacamos. Lo registramos como ejemplo donde la crítica se contradice sola.

### Heurísticas donde la IA dijo "cumple" (H1, H2, H4, H7)

- **Decisión del grupo:** acordamos. En particular H1 y H4 refuerzan dos decisiones del primer ciclo que nos interesaba validar: (a) la línea de metadatos arriba de la tabla, que coincide con la que después aparece en el archivo descargado — eso ancla el chip "Guardado en el historial" y el requerimiento de persistencia de HU11; (b) el botón "Descargar N hits visibles" con el contador dinámico, que materializa HU13 CA-01/CA-02 ("entrega los hits visibles al momento del click").

### Resumen de la revisión

| Heurística | Veredicto IA | Decisión grupo | Entra al ciclo adicional |
|---|---|---|---|
| H1 — Visibilidad | cumple | — | — |
| H2 — Mundo real | cumple | — | — |
| H3 — Control y libertad | parcial | **aceptado** ("Limpiar filtros" como botón real) | **sí** |
| H4 — Consistencia | cumple | — | — |
| H5 — Prevención de errores | parcial | rechazado (requiere JS) | no |
| H6 — Reconocimiento | parcial | **aceptado** (fusionado con H10) | **sí** |
| H7 — Flexibilidad | cumple | — | — |
| H8 — Minimalista | parcial | rechazado (contradicción interna del hallazgo; en pantalla ayudan) | no |
| H9 — Recuperación de errores | parcial | **aceptado** (sugerencias accionables en tabla vacía) | **sí** |
| H10 — Ayuda y documentación | incumple | **aceptado** (fusionado con H6) | **sí** |

---

## 4. Ciclo adicional — Ajuste de la interfaz

### 4.1 Prompt del ajuste

> **Prompt:**
>
> Sobre `pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_inicial.html`, aplicá tres cambios y devolveme `_final.html`. Mantené todo lo demás y la regla "sin JS":
>
> 1. **H6 + H10.** Agregá un ícono `?` tipo tooltip CSS (mismo patrón `::after` + `attr(data-tip)` que usamos en la pantalla 2) en los cinco encabezados de columna de la tabla (Hit ID, Score, E-value obs., % Identidad, % Cobertura) y al lado de cada una de las cinco opciones de formato de descarga (CSV, JSON, FASTA, BLAST XML, Tabular). El tooltip tiene que ser una línea breve y accionable: para columnas, definición breve; para formatos, "cuándo usarlo". Dejá al menos un tooltip expandido por default (clase `show-tip`) para que el revisor del maquetado lo vea en papel; sugerimos el de E-value obs., que es el que más confunde.
>
> 2. **H3.** Reemplazá el link "Limpiar filtros" (que hoy es `<button class="reset-btn">` con estilo de link subrayado) por un botón real, con jerarquía propia, estilo secundario (fondo claro, borde, no subrayado), al final del panel de filtros. Que ocupe el ancho del panel para que sea imposible pasarlo por alto. Aplicá el mismo cambio en el estado alternativo (HU14) donde el link también aparece.
>
> 3. **H9.** En el estado alternativo HU14 (tabla vacía por filtros estrictos), debajo del texto "Sin hits visibles — probá bajar el umbral de identidad o aflojar el E-value", agregá una fila de tres botones de sugerencia accionables: "Bajar identidad a ≥ 80%", "Aflojar E-value a ≤ 1e-10", "↺ Limpiar todos los filtros". Estilo "chip botón" claro (fondo celeste suave, borde, texto azul), no botones primarios.
>
> Actualizá la nota del maquetado para que explique los tres cambios y referencie este documento.

### 4.2 Respuesta de la IA (resumen y modificaciones aplicadas)

La IA devolvió el HTML con los tres cambios. Lo que quedó en [`pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_final.html`](../mockups/pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_final.html):

- **CSS nuevo:** `.help-icon` + `.help-icon::after` + `.help-icon.show-tip` (misma convención que la pantalla 2), con una regla extra `th .help-icon { background: #e2e8f0; color: var(--color-text-muted); }` para que en los encabezados de la tabla el ícono tenga menos peso visual y no compita con el nombre de la columna; `.clear-filters-btn` para el botón de limpiar; `.empty-suggest-row` + `.btn-sugg` para los chips de sugerencia; `.format-help` (reservado para un uso futuro, no se usó finalmente).
- **Encabezados de la tabla:** cinco íconos `?` agregados, uno por columna. El del E-value obs. tiene la clase `show-tip` para que se vea expandido en el maquetado.
- **Opciones de formato de descarga:** cinco íconos `?` agregados, con tooltips orientados a "cuándo usar".
- **Botón "Limpiar filtros":** en los dos estados (primario y HU14) se reemplazó el link subrayado por el botón de ancho completo `clear-filters-btn`.
- **Estado alternativo HU14:** se agregaron los tres chips de sugerencia debajo del banner `empty-table`.
- **Nota del maquetado:** reescrita, lista los tres cambios y apunta a este documento.

### 4.3 Qué modificamos sobre la devolución de la IA

- **Textos de los tooltips de columnas.** La primera devolución tenía definiciones genéricas tomadas de Wikipedia ("E-value: expectation value, a parameter in sequence alignment"). Las reemplazamos por frases funcionales y específicas de BLAST ("E-value observado para este hit puntual: cuántas veces se esperaría un alineamiento de este score por azar en una base del mismo tamaño. Más bajo = más significativo."), que es lo que al investigador le sirve al leer la tabla.
- **Peso visual del `?` en encabezados.** Reglamos el ícono para que en los `<th>` se vea en gris claro, no en azul, porque en azul compite con el nombre de la columna y rompe la jerarquía de lectura de la tabla. Fuera de la tabla sigue en azul.
- **Sugerencia de "Aflojar E-value".** La IA había propuesto "Aflojar E-value a ≤ 0.001" en el chip del estado vacío. Lo cambiamos a `1e-10` para que sea coherente con el valor que el usuario inicialmente puso en el input de ese estado (`1e-50`): "aflojar" significa pasar a un umbral menos estricto, y `1e-10` es menos estricto que `1e-50` pero sigue siendo un valor típico de laboratorio. `0.001` es demasiado permisivo y daría la impresión de que estamos abriendo la compuerta.

### 4.4 Qué descartamos del ajuste

- Una propuesta de la IA de agregar, además de los chips, un botón "Ver todos los 54 hits sin filtros" en el banner del estado vacío. Lo descartamos como redundante: "Limpiar todos los filtros" ya hace eso, y es uno de los tres chips. Dos acciones con el mismo efecto a dos clicks de distancia solo generan dudas.

### 4.5 Resultado

El `_final.html` cubre los tres hallazgos aceptados. El `_inicial.html` queda como línea base verificable.
