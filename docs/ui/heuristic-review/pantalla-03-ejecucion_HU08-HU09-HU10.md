# Evaluación heurística — Pantalla 3: Ejecución en progreso

- **Mockup inicial evaluado:** [`../mockups/pantalla-03-ejecucion_HU08-HU09-HU10_inicial.html`](../mockups/pantalla-03-ejecucion_HU08-HU09-HU10_inicial.html)
- **Mockup final tras ciclo adicional:** [`../mockups/pantalla-03-ejecucion_HU08-HU09-HU10_final.html`](../mockups/pantalla-03-ejecucion_HU08-HU09-HU10_final.html)
- **HUs cubiertas:** `HU08_CU004_B` (ejecución asíncrona con progreso), `HU09_CU004_A1` (cancelación manual), `HU10_CU004_E1` (fallo del modo remoto, mensaje literal)
- **Perfil y escenario de referencia:** `docs/ui/user-profiles/investigador.md`

---

## 1. Primer ciclo — Generación del HTML (resumen)

El prompt completo y los criterios del grupo del primer ciclo están registrados en [`../mockups/README.md`](../mockups/README.md).

La IA entregó esta pantalla como [`pantalla-03-ejecucion_HU08-HU09-HU10_inicial.html`](../mockups/pantalla-03-ejecucion_HU08-HU09-HU10_inicial.html), con cuatro estados apilados: ejecución primaria con barra de progreso + barra lateral navegable, estado posterior a cancelación, estado de excepción por timeout de NCBI y estado de excepción por rechazo explícito de NCBI (rate limit).

---

## 2. Segundo ciclo — Evaluación heurística con IA

### 2.1 Prompt utilizado

Conversación nueva. Se le adjuntaron el HTML inicial, el perfil del Investigador/a y las tres HU cubiertas.

> **Prompt:**
>
> Actuá como especialista en interfaces de usuario. Te paso tres archivos:
>
> 1. `pantalla-03-ejecucion_HU08-HU09-HU10_inicial.html` — pantalla de LocalBlast (GUI para BLAST+) correspondiente a la **ejecución** de una búsqueda. Cubre tres HU: HU08 (ejecución asíncrona con indicador de progreso visible y posibilidad de seguir navegando en la aplicación), HU09 (cancelación manual) y HU10 (fallo del modo remoto; mostrar el mensaje literal de BLAST+ sin reinterpretar). El archivo muestra apilados los cuatro estados: ejecución en curso, cancelación confirmada, timeout de NCBI, rechazo explícito de NCBI.
> 2. `investigador.md` — perfil del único actor principal.
> 3. `historias-usuario.md` — las tres HU con criterios Given-When-Then.
>
> Un dato importante del dominio para esta pantalla: en el perfil se habla explícitamente de que *"BLAST+ y NCBI fallan seguido en la práctica. Timeouts, rate limits, errores remotos. El Investigador necesita que, cuando algo falla, la interfaz le muestre el mensaje literal, para distinguir un problema de red temporal de uno más grave."* La HU10 refleja esto.
>
> Evaluá la pantalla **heurística por heurística** según las **10 heurísticas de Nielsen**, con el perfil concreto en mente. Para cada una: **cumple / parcial / incumple**, por qué, y una mejora si corresponde. Evaluá los cuatro estados.

### 2.2 Respuesta de la IA (completa)

**H1 — Visibilidad del estado del sistema. Cumple.**
Varios refuerzos simultáneos y coherentes: barra de progreso con porcentaje aproximado (62%), tiempo transcurrido (01:47), metadatos de la ejecución (programa, BD, E-value máx, query, hora de inicio), spinner visible, y —muy importante para HU08— un chip animado "corriendo" en la barra lateral del ítem "Ejecución en curso". Eso materializa el requerimiento de que el usuario pueda cambiar de sección sin perder el estado de la ejecución. En los estados de error, el sistema deja claro qué pasó y por qué no se persistió nada.

**H2 — Correspondencia entre el sistema y el mundo real. Cumple.**
"Ejecutando `blastp` contra `nr` (NCBI remoto)" es exactamente el lenguaje del investigador. El bloque de error con la salida literal `[BLAST+ stderr]` también: el investigador se encuentra con ese mismo texto cuando usa la línea de comandos.

**H3 — Control y libertad del usuario. Cumple.**
El botón "⨯ Cancelar búsqueda" está siempre visible y es el único botón del estado primario, lo cual lo hace trivial de encontrar. El hint "Podés seguir trabajando. La búsqueda sigue corriendo..." es un control implícito de libertad: el usuario sabe que no está atado a la pantalla. En los estados de error, el botón "Reintentar búsqueda" devuelve el control.

**H4 — Consistencia y estándares. Cumple.**
Los mismos componentes de siempre (barra lateral, panel central, banner de error rojo, bloque mono para la salida literal). La convención de "cancelación es un botón rojo" se respeta. La paleta sigue siendo la de las pantallas anteriores.

**H5 — Prevención de errores. Cumple parcialmente.**
El punto flaco es puntual: el botón "⨯ Cancelar búsqueda" no pide confirmación. Para una búsqueda larga (una `blastp` contra `nr` puede tomar varios minutos), un click accidental descarta todo el trabajo. En producción el patrón habitual es un modal confirmatorio ("¿Seguro que querés cancelar?"). El perfil dice explícitamente que BLAST+/NCBI fallan seguido, lo cual **ya** genera repeticiones; sumar una repetición por cancelación accidental es un costo real. Sugerencia: confirmación de dos pasos.

**H6 — Reconocimiento en lugar de recuerdo. Cumple.**
Toda la configuración que llevó a esta ejecución está visible en el panel de metadatos (modo, programa, BD, E-value, query, hora). El investigador no necesita acordarse de qué configuró; lo tiene arriba.

**H7 — Flexibilidad y eficiencia de uso. Cumple.**
La barra lateral con "Nueva búsqueda", "Búsquedas recientes", "Guardadas" y "Bases de datos locales" materializa la navegación paralela que exige HU08 CA-01. El usuario sénior puede empezar a armar otra búsqueda mientras esta corre; el chip "corriendo" le recuerda que la primera sigue viva.

**H8 — Diseño estético y minimalista. Cumple.**
Es la pantalla menos cargada del flujo: pocas acciones, estado dominante (progreso), y lo demás es información de contexto. Las ventanas de error no decoran.

**H9 — Ayudar al usuario a reconocer, diagnosticar y recuperarse de errores. Cumple.**
Dos aciertos importantes. Primero, los mensajes de error distinguen explícitamente **tipo** de fallo ("Timeout de comunicación con NCBI" vs "NCBI rechazó la búsqueda") y aclaran que **no** es un problema de los parámetros, lo cual libera al investigador de ir a revisar la configuración por error. Segundo, el bloque `[BLAST+ stderr]` muestra el mensaje literal — eso cumple HU10 CA-01 y CA-02 al pie de la letra. Los botones "Volver a la configuración" y "Reintentar búsqueda" ofrecen rutas de recuperación concretas. Lo que podría mejorar es un detalle: en el estado de cancelación, aparece dicho que "la búsqueda no quedó guardada en el historial". Esa misma garantía debería ser visible **antes** de cancelar, para que el investigador pueda decidir con información completa.

**H10 — Ayuda y documentación. Cumple parcialmente.**
Para los estados de error, la pantalla ya documenta explícitamente qué pasó y cómo seguir, con lo cual el usuario no necesita documentación externa. Para la ejecución en curso, no hay información de "cuánto más va a tardar" ni "qué pasa si cierro la pestaña". El perfil no exige lo primero (es una estimación cara y poco confiable para BLAST remoto), pero sí sería útil aclarar lo segundo. Sugerencia: línea breve sobre qué pasa si se cierra la ventana.

---

## 3. Revisión crítica del grupo

### H5 — Confirmación antes de cancelar

- **Decisión del grupo:** **aceptado.** Es coherente con las decisiones que ya tomamos en las pantallas 1 y 2 ("Reemplazar secuencia", "Restaurar defaults"): acciones con efecto destructivo piden confirmación. En este caso el efecto destructivo es "tirar varios minutos de ejecución a la basura". Entra al ciclo adicional.

### H9 — Mostrar la garantía de "aún no persistida" **durante** la ejecución, no solo tras cancelar

- **Decisión del grupo:** **aceptado.** El hallazgo es más fuerte de lo que la IA le dio: la `HU11_CU005_B` CA-02 dice que la persistencia en el historial **sucede al final de la ejecución exitosa**, no antes. Si el investigador no sabe eso, puede dudar en cancelar ("¿pierdo todo si cancelo?"); con la garantía visible desde el inicio, decide con información completa. Entra al ciclo adicional.

### H10 — Línea sobre qué pasa si se cierra la ventana

- **Decisión del grupo:** **rechazado por ahora.** El comportamiento concreto depende de la implementación (si el servidor sigue ejecutando o aborta la sesión), y esa decisión no está tomada en el TP1. Prometer en el maquetado un comportamiento que después quizás no implementemos es peor que no decir nada. Lo anotamos para cuando se implemente HU08 y haya una decisión real.

### Heurísticas donde la IA dijo "cumple" (H1, H2, H3, H4, H6, H7, H8)

- **Decisión del grupo:** acordamos sin cambios. En particular registramos como acierto del primer ciclo:
  - El chip "corriendo" en la barra lateral, que materializa HU08 CA-01 ("permite seguir navegando").
  - El bloque mono-espaciado con la salida literal `[BLAST+ stderr]`, que cumple HU10 CA-01/CA-02 al pie de la letra.
  Son dos cosas que fueron costosas de pedir en el primer ciclo y que ahora quedan validadas.

### Resumen de la revisión

| Heurística | Veredicto IA | Decisión grupo | Entra al ciclo adicional |
|---|---|---|---|
| H1 — Visibilidad | cumple | — (reforzado por la mejora de H9) | — |
| H2 — Mundo real | cumple | — | — |
| H3 — Control y libertad | cumple | — | — |
| H4 — Consistencia | cumple | — | — |
| H5 — Prevención de errores | parcial | **aceptado** (confirmación de cancelación) | **sí** |
| H6 — Reconocimiento | cumple | — | — |
| H7 — Flexibilidad | cumple | — | — |
| H8 — Minimalista | cumple | — | — |
| H9 — Recuperación de errores | cumple | **aceptado el refuerzo** ("aún no persistida" visible siempre) | **sí** |
| H10 — Ayuda y documentación | parcial | rechazado (comportamiento al cerrar ventana no está definido en TP1) | no |

---

## 4. Ciclo adicional — Ajuste de la interfaz

### 4.1 Prompt del ajuste

> **Prompt:**
>
> Sobre `pantalla-03-ejecucion_HU08-HU09-HU10_inicial.html`, aplicá dos cambios y devolveme `_final.html`. Mantené todo lo demás y la regla "sin JS":
>
> 1. **H1 + H9 reforzado.** En la zona del progreso del estado primario (justo donde dice "Progreso aproximado: 62%"), agregá un chip visible —de color ámbar, no verde, para marcar que es un estado transitorio— con el texto "aún no persistida en el historial". El chip refuerza visualmente la garantía de HU11_CU005_B CA-02: la persistencia ocurre al final, no durante. Que el chip quede inmediatamente al lado del porcentaje para que un investigador que mire el progreso lo vea sin esfuerzo.
>
> 2. **H5.** Agregá un bloque de confirmación que simule el estado posterior al click del botón "Cancelar búsqueda" del estado primario. El bloque va **antes** del botón original (en el flujo real sería un modal; en el maquetado va apilado) y contiene: texto "¿Cancelar la búsqueda en curso? Se abortará la invocación a BLAST+. La búsqueda **no** se va a guardar en el historial (ya está marcada como 'aún no persistida')." más dos botones: "No, seguir corriendo" (neutro, blanco con borde) y "Sí, cancelar" (rojo oscuro, firme, no `btn-danger` suave).
>
> Actualizá la nota del maquetado al pie para que explique los dos cambios y referencie este documento.

### 4.2 Respuesta de la IA (resumen y modificaciones aplicadas)

La IA devolvió el HTML con los dos cambios. Lo que quedó en [`pantalla-03-ejecucion_HU08-HU09-HU10_final.html`](../mockups/pantalla-03-ejecucion_HU08-HU09-HU10_final.html):

- **CSS nuevo:** `.not-saved-chip` para el chip ámbar inline; `.confirm-cancel` + `.btn-neutral` + `.btn-danger-firm` para la confirmación de cancelación.
- **Zona de progreso:** chip "aún no persistida en el historial" agregado al lado del porcentaje.
- **Panel del estado primario:** se añadió el bloque de confirmación de cancelación arriba del botón "Cancelar búsqueda" original. En implementación, uno y otro son excluyentes; en el maquetado se muestran juntos.
- **Nota del maquetado:** reescrita, lista los dos cambios y apunta a este documento.

### 4.3 Qué modificamos sobre la devolución de la IA

- **Posición del chip.** La IA en una primera versión lo puso en una línea aparte, debajo de la barra de progreso. Lo movimos a la misma línea del porcentaje porque allí es donde el investigador mira primero y donde el chip tiene efecto cognitivo real ("62% + aún no persistida" se lee junto, "62% \n aún no persistida" se lee como dato aparte y se puede ignorar).
- **Tono del botón de cancelación firme.** La IA inicialmente lo dejó con el mismo `btn-danger` suave que ya existía en el estado primario. Lo cambiamos a `btn-danger-firm` (rojo oscuro, borde propio) para que **sí haya diferencia visual** entre "voy a mostrar la intención de cancelar" (soft) y "confirmo que cancelo" (firme). Si los dos botones son iguales, el modal confirmatorio pierde propósito.

### 4.4 Qué descartamos del ajuste

- Una propuesta de la IA de agregar también una cuenta regresiva de 5 segundos en el botón "Sí, cancelar" ("Sí, cancelar (5)"), inspirada en patrones de desinstaladores agresivos. La rechazamos: el perfil del Investigador/a no describe comportamientos impulsivos, y la cuenta regresiva molesta justamente al escenario legítimo (vi que configuré algo mal, quiero cancelar ya). El doble click de confirmación alcanza.

### 4.5 Resultado

El `_final.html` cubre los dos hallazgos aceptados. El `_inicial.html` se conserva como línea base.
