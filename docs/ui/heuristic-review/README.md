# Evaluación heurística — Segundo ciclo del maquetado asistido por IA

Esta carpeta contiene la evaluación heurística de usabilidad de las pantallas del flujo de navegación del Investigador/a, siguiendo el **segundo ciclo** del proceso de maquetado asistido por IA definido en la guía del TP2 (sección 4.4) y los ciclos subsiguientes de revisión crítica del grupo (4.5) y de ajuste de la interfaz (4.6).

El punto de partida son los mockups HTML generados en el primer ciclo (`docs/ui/mockups/pantalla-NN-..._inicial.html`). Para cada pantalla, el ciclo de evaluación consistió en:

1. **Evaluación por IA.** Se le entregó el HTML de la pantalla a la IA en una nueva interacción (sin arrastrar el contexto del ciclo de generación) y se le pidió que asumiera el rol de especialista en interfaz de usuario y evaluara la pantalla **heurística por heurística** según las diez heurísticas de usabilidad de Nielsen, teniendo en cuenta el **perfil del Investigador/a** (`docs/ui/user-profiles/investigador.md`) y el **escenario de uso de referencia** definidos, y no un usuario genérico. Para cada heurística, la IA debía indicar si se cumple, si se cumple parcialmente o si se incumple, y por qué.
2. **Revisión crítica del grupo.** El grupo revisó cada hallazgo devuelto por la IA y, para cada uno, decidió aceptarlo o rechazarlo, documentando el motivo de la decisión. Esta revisión es el núcleo pedagógico de la actividad: la IA identifica posibles problemas, pero el criterio sobre su validez y aplicabilidad al Investigador/a y al proyecto concretos es responsabilidad del grupo.
3. **Ciclo adicional de ajuste.** Para los hallazgos aceptados, el grupo pidió a la IA una variante ajustada del HTML con las mejoras aplicadas. El resultado es el archivo `pantalla-NN-..._final.html` de la carpeta de mockups.

## Documentos

| Pantalla | Documento | HUs cubiertas | Mockup inicial | Mockup final |
|---|---|---|---|---|
| 1 — Carga de secuencia | [`pantalla-01-carga-secuencia_HU01-HU02.md`](pantalla-01-carga-secuencia_HU01-HU02.md) | `HU01_CU001_B`, `HU02_CU001_E1` | [`_inicial`](../mockups/pantalla-01-carga-secuencia_HU01-HU02_inicial.html) | [`_final`](../mockups/pantalla-01-carga-secuencia_HU01-HU02_final.html) |
| 2 — Configuración y validación | [`pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07.md`](pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07.md) | `HU03_CU002_B`, `HU04_CU002_A1`, `HU05_CU003_B`, `HU06_CU003_E1`, `HU07_CU003_E2` | [`_inicial`](../mockups/pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_inicial.html) | [`_final`](../mockups/pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_final.html) |
| 3 — Ejecución | [`pantalla-03-ejecucion_HU08-HU09-HU10.md`](pantalla-03-ejecucion_HU08-HU09-HU10.md) | `HU08_CU004_B`, `HU09_CU004_A1`, `HU10_CU004_E1` | [`_inicial`](../mockups/pantalla-03-ejecucion_HU08-HU09-HU10_inicial.html) | [`_final`](../mockups/pantalla-03-ejecucion_HU08-HU09-HU10_final.html) |
| 4 — Resultados, filtros y descarga | [`pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14.md`](pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14.md) | `HU11_CU005_B`, `HU12_CU006_B`, `HU13_CU007_B`, `HU14_CU007_A1` | [`_inicial`](../mockups/pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_inicial.html) | [`_final`](../mockups/pantalla-04-resultados-filtros-descarga_HU11-HU12-HU13-HU14_final.html) |

## Qué incluye cada documento

Siguiendo la sección 4.7 de la guía del TP2, cada documento contiene:

- **Referencia al prompt de generación de HTML y a la respuesta de la IA** del primer ciclo, con enlace al archivo donde ya quedaron registrados (`docs/ui/mockups/README.md`), para no duplicar su transcripción.
- **Prompt literal utilizado para la evaluación heurística** (ciclo 2) y la **respuesta completa de la IA** con el veredicto por cada una de las diez heurísticas.
- **Revisión crítica del grupo**: para cada hallazgo, decisión de aceptación o rechazo con la justificación correspondiente.
- **Ciclos adicionales de ajuste**, cuando el grupo decidió aplicar cambios al HTML: prompt del ajuste, resumen de la respuesta de la IA, y la lista de modificaciones efectivamente aplicadas al `_final.html`.

## Heurísticas de Nielsen utilizadas (10)

Para unificar el vocabulario, cada evaluación referencia las heurísticas por número y nombre en español:

1. **Visibilidad del estado del sistema**
2. **Correspondencia entre el sistema y el mundo real**
3. **Control y libertad del usuario**
4. **Consistencia y estándares**
5. **Prevención de errores**
6. **Reconocimiento en lugar de recuerdo**
7. **Flexibilidad y eficiencia de uso**
8. **Diseño estético y minimalista**
9. **Ayudar al usuario a reconocer, diagnosticar y recuperarse de errores**
10. **Ayuda y documentación**

## Nota sobre el perfil de usuario en la evaluación

En todas las interacciones con la IA se le pasó como contexto el perfil del Investigador/a (`docs/ui/user-profiles/investigador.md`), incluidas sus limitaciones y frustraciones y el rango de nivel técnico (desde estudiante de grado hasta investigador sénior). Esto es relevante porque varios hallazgos cambian de signo según se evalúen contra "un usuario genérico" o contra el Investigador/a: por ejemplo, la ausencia de un tutorial inicial (heurística 10) es un problema para un usuario genérico, pero no para alguien que ya sabe qué es BLAST y viene a hacer un alineamiento concreto.
