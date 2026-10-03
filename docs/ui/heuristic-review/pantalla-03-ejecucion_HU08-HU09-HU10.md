# Evaluación heurística — Pantalla 3: Ejecución en progreso

- **Mockup inicial:** [`../mockups/pantalla-03-ejecucion_HU08-HU09-HU10_inicial.html`](../mockups/pantalla-03-ejecucion_HU08-HU09-HU10_inicial.html)
- **Mockup final:** [`../mockups/pantalla-03-ejecucion_HU08-HU09-HU10_final.html`](../mockups/pantalla-03-ejecucion_HU08-HU09-HU10_final.html)
- **HUs cubiertas:** `HU08_CU004_B`, `HU09_CU004_A1`, `HU10_CU004_E1`

---

## 1. Primer ciclo (generación del HTML)

Prompt y resumen de la generación: ver [`../mockups/README.md`](../mockups/README.md). La salida es `_inicial.html`.

---

## 2. Segundo ciclo — Evaluación heurística con IA

### 2.1 Prompt que le pasamos a la IA

> Actuá como especialista en interfaz de usuario. Te paso el HTML de la pantalla de **ejecución** de LocalBlast, el perfil del Investigador/a y las 3 HU cubiertas. Evaluala **heurística por heurística** según las 10 heurísticas de Nielsen, con este perfil concreto. Para cada una: **cumple / parcial / incumple**, por qué, y una mejora si corresponde. La pantalla muestra 4 estados apilados: ejecución en curso, cancelación, timeout de NCBI, rechazo explícito de NCBI. Evaluá los cuatro.

### 2.2 Respuesta de la IA

| # | Heurística | Veredicto | Fundamento (resumen) |
|---|---|---|---|
| 1 | Visibilidad del estado | cumple | Barra de progreso, tiempo, metadatos, spinner, y chip "corriendo" en la barra lateral. |
| 2 | Mundo real | cumple | "Ejecutando `blastp` contra `nr` (NCBI remoto)" + bloque `[BLAST+ stderr]` para los errores. |
| 3 | Control y libertad | cumple | Botón "Cancelar" visible y hint "podés seguir trabajando". |
| 4 | Consistencia | cumple | Componentes y paleta coherentes con el resto. |
| 5 | Prevención de errores | parcial | "Cancelar búsqueda" no pide confirmación. Un click accidental tira varios minutos. |
| 6 | Reconocimiento | cumple | Toda la config que llevó a esta ejecución está visible arriba. |
| 7 | Flexibilidad | cumple | Barra lateral permite navegar sin interrumpir la ejecución. |
| 8 | Minimalista | cumple | Es la pantalla menos cargada del flujo. |
| 9 | Recuperación de errores | cumple | Mensajes distinguen timeout de rechazo, muestran stderr literal, ofrecen "Reintentar". |
| 10 | Ayuda y documentación | parcial | Nada que aclare qué pasa si se cierra la pestaña durante la ejecución. |

### 2.3 Lo que la IA sugirió para los parciales

- H5: confirmación de dos pasos antes de cancelar.
- H9 (observación suelta dentro del "cumple"): mostrar la garantía de "no se guardó nada" **antes** de cancelar, no solo después.
- H10: línea sobre qué pasa si se cierra la ventana.

---

## 3. Revisión del grupo

| Hallazgo | Decisión | Por qué |
|---|---|---|
| H5 — confirmar cancelación | **aceptado** | Mismo criterio que las pantallas anteriores: acción destructiva pide confirmación. Entra al ajuste. |
| H9 (refuerzo) — "no se guardó" durante la ejecución | **aceptado** | Lo tomamos del comentario de la IA dentro de H9 y lo levantamos como hallazgo propio. HU11 CA-02 dice que la persistencia es al final. Si el investigador no sabe eso, duda en cancelar. Entra al ajuste. |
| H10 — qué pasa si cierro la pestaña | **rechazado** | El comportamiento concreto depende de la implementación, no está definido en TP1. Prometerlo en el maquetado y después no cumplirlo es peor que no decir nada. |

**Cambios que entran al ciclo adicional:** chip "aún no persistida en el historial" durante la ejecución; bloque de confirmación antes de cancelar.

---

## 4. Ciclo adicional (ajuste del HTML)

### 4.1 Prompt del ajuste

> Sobre `_inicial.html`, aplicá dos cambios y devolvemelo como `_final.html`, con la regla "sin JS":
>
> 1. Al lado del porcentaje de progreso, agregá un chip ámbar "aún no persistida en el historial", para dejar visible desde el principio que la persistencia ocurre al final (HU11 CA-02).
> 2. Antes del botón "Cancelar búsqueda" original, agregá un bloque de confirmación que simule el click: texto "¿Cancelar la búsqueda en curso? Se abortará la invocación a BLAST+. La búsqueda **no** se va a guardar en el historial", más dos botones: "No, seguir corriendo" y "Sí, cancelar" (rojo firme, no `btn-danger` suave).

### 4.2 Qué quedó en el `_final.html`

- Chip "aún no persistida en el historial" al lado del porcentaje.
- Bloque de confirmación con dos botones antes del botón original "Cancelar búsqueda".
- Nota del maquetado al pie, reescrita.

### 4.3 Qué cambiamos nosotros sobre lo que devolvió la IA

- La IA puso el chip en una línea aparte. Lo movimos a la misma línea del porcentaje para que se lea "62% + aún no persistida" como una sola unidad.
- La IA dejó el botón "Sí, cancelar" con el mismo `btn-danger` suave que el botón original. Lo cambiamos a rojo oscuro firme para que haya diferencia visual entre "muestro la intención" y "confirmo"; si no, el modal pierde propósito.
- Descartamos una propuesta de la IA de agregar cuenta regresiva al botón de confirmación ("Sí, cancelar (5)"). El perfil no describe comportamientos impulsivos y la cuenta regresiva molesta al caso legítimo (ya sé que me equivoqué, quiero cancelar ya).

### 4.4 Resultado

El `_final.html` tiene los dos cambios aceptados. El `_inicial.html` queda para poder comparar.
