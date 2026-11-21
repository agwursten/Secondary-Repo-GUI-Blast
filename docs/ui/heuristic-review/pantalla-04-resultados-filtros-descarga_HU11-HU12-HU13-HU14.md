# Evaluación heurística — Pantalla 4: Resultados, filtros y descarga

- **Mockup inicial:** [`../mockups/pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_inicial.html`](../mockups/pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_inicial.html)
- **Mockup final:** [`../mockups/pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_final.html`](../mockups/pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_final.html)
- **HUs cubiertas:** `HU11_CU005_B`, `HU12_CU006_B`, `HU13_CU007_B`, `HU14_CU007_A1`

---

## 1. Primer ciclo (generación del HTML)

Prompt y resumen de la generación: ver [`../mockups/README.md`](../mockups/README.md). La salida es `_inicial.html`.

---

## 2. Segundo ciclo — Evaluación heurística con IA

### 2.1 Prompt que le pasamos a la IA

> Actuá como especialista en interfaz de usuario. Te paso el HTML de la pantalla de **resultados, filtros y descarga** de LocalBlast, el perfil del Investigador/a y las 4 HU cubiertas. Evaluala **heurística por heurística** según las 10 heurísticas de Nielsen, con este perfil concreto. Para cada una: **cumple / parcial / incumple**, por qué, y una mejora si corresponde. La pantalla muestra 2 estados apilados: tabla filtrada con 12/54 hits visibles, y tabla vacía por filtros estrictos. Evaluá los dos.

### 2.2 Respuesta de la IA

| # | Heurística | Veredicto | Fundamento (resumen) |
|---|---|---|---|
| 1 | Visibilidad del estado | cumple | "12 de 54", badge de filtros activos, chip "Guardado en el historial", botón "Descargar N visibles" dinámico. |
| 2 | Mundo real | cumple | Columnas y filtros con los nombres esperados; formatos con nombres del dominio. |
| 3 | Control y libertad | parcial | "Limpiar filtros" es un link subrayado chico, poco visible. |
| 4 | Consistencia | cumple | Panel lateral + tabla + radios + botón primario. Componentes esperables. |
| 5 | Prevención de errores | parcial | El input de E-value es texto libre sin validación visible. |
| 6 | Reconocimiento | parcial | Columnas y formatos tienen nombre pero no definición. |
| 7 | Flexibilidad | cumple | Cinco formatos, sliders rápidos, descarga con metadatos. |
| 8 | Minimalista | parcial | Las mini-barras junto a los porcentajes podrían competir con el número. (La IA aclara: en pantalla ayudan, en papel se ven cargadas.) |
| 9 | Recuperación de errores | parcial | El banner de tabla vacía informa, pero no da un click para salir del estado. |
| 10 | Ayuda y documentación | incumple | Sin tooltips ni ayuda contextual para formatos y columnas. |

### 2.3 Lo que la IA sugirió para los parciales / incumplidos

- H3: "Limpiar filtros" como botón real con jerarquía propia.
- H5: validación del input de E-value.
- H6 + H10: tooltips en columnas de la tabla y en los formatos de descarga.
- H9: botones de sugerencia accionables en el estado vacío.

---

## 3. Revisión del grupo

| Hallazgo | Decisión | Por qué |
|---|---|---|
| H3 — "Limpiar filtros" como botón real | **aceptado** | El investigador afloja y aprieta filtros con fluidez; "volver a cero" tiene que ser tan visible como aplicar. Entra al ajuste. |
| H5 — validación del input de E-value | **rechazado** | Requiere JS. Backlog para la implementación. |
| H6 + H10 — tooltips en columnas y formatos | **aceptado** (fusionados) | Igual criterio que en pantalla 2. Hacemos tooltips CSS puros. Entra al ajuste. |
| H8 — mini-barras cargadas | **rechazado** | La propia IA aclara que en pantalla ayudan. Las dejamos. |
| H9 — sugerencias accionables en tabla vacía | **aceptado** | Un click para salir del estado vacío, en vez de mover tres sliders a mano. Entra al ajuste. |

**Cambios que entran al ciclo adicional:** tooltips en encabezados de tabla y formatos de descarga, "Limpiar filtros" como botón de ancho completo, chips de sugerencia en el estado vacío.

---

## 4. Ciclo adicional (ajuste del HTML)

### 4.1 Prompt del ajuste

> Sobre `_inicial.html`, aplicá tres cambios y devolvemelo como `_final.html`, con la regla "sin JS":
>
> 1. Tooltips CSS (`?` con `::after` + `attr(data-tip)`, mismo patrón que la pantalla 2) en los cinco encabezados de columna (Hit ID, Score, E-value obs., % Identidad, % Cobertura) y en los cinco formatos de descarga (CSV, JSON, FASTA, BLAST XML, Tabular). Para columnas: definición breve. Para formatos: "cuándo usarlo". Dejá expandido por default el de E-value obs.
> 2. Reemplazá el link "Limpiar filtros" por un botón real de ancho completo al final del panel de filtros. Aplicá el cambio en los dos estados apilados.
> 3. En el estado de tabla vacía (HU14), debajo del banner, agregá una fila con tres chips de sugerencia accionables: "Bajar identidad a ≥ 80%", "Aflojar E-value a ≤ 1e-10", "↺ Limpiar todos los filtros".

### 4.2 Qué quedó en el `_final.html`

- 10 tooltips `?` en total (5 columnas + 5 formatos). El de E-value obs. expandido por default.
- "Limpiar filtros" como botón de ancho completo en los dos estados.
- Tres chips de sugerencia accionables en el banner de tabla vacía.
- Nota del maquetado al pie, reescrita.

### 4.3 Qué cambiamos nosotros sobre lo que devolvió la IA

- La IA escribió los primeros tooltips como definiciones de diccionario. Los reescribimos con lenguaje funcional (qué valor típico, cuándo bajarlo, cuándo usar cada formato).
- El ícono `?` en los encabezados de tabla salía en azul brillante y competía con el nombre de la columna. Le pusimos una regla CSS específica para `th .help-icon` que lo pasa a gris claro.
- En el chip "Aflojar E-value", la IA había puesto `≤ 0.001`. Lo cambiamos a `1e-10` para que fuera coherente con el valor del input de ese estado (`1e-50`): "aflojar" tiene que ser menos estricto pero no abrir del todo.
- La IA, en una variante intermedia, propuso agregar al banner un botón "Ver todos los 54 hits sin filtros". Lo descartamos porque "Limpiar todos los filtros" ya hace eso y era redundante.
- La IA en la primera pasada reemplazó el link por el botón solo en el estado primario, se olvidó del estado alternativo HU14. Lo detectamos al abrir el `_final.html` y le pedimos la segunda pasada.

### 4.4 Resultado

El `_final.html` tiene los tres cambios aceptados. El `_inicial.html` queda para poder comparar.
