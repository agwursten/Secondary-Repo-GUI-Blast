# Evaluación heurística — Pantalla 2: Configuración y validación

- **Mockup inicial:** [`../mockups/pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_inicial.html`](../mockups/pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_inicial.html)
- **Mockup final:** [`../mockups/pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_final.html`](../mockups/pantalla-02-configuracion-validacion_HU03-HU04-HU05-HU06-HU07_final.html)
- **HUs cubiertas:** `HU03_CU002_B`, `HU04_CU002_A1`, `HU05_CU003_B`, `HU06_CU003_E1`, `HU07_CU003_E2`

---

## 1. Primer ciclo (generación del HTML)

Prompt y resumen de la generación: ver [`../mockups/README.md`](../mockups/README.md). La salida es `_inicial.html`.

---

## 2. Segundo ciclo — Evaluación heurística con IA

### 2.1 Prompt que le pasamos a la IA

> Actuá como especialista en interfaz de usuario. Te paso el HTML de la pantalla de **configuración y validación** de LocalBlast, el perfil del Investigador/a y las 5 HU cubiertas. Evaluala **heurística por heurística** según las 10 heurísticas de Nielsen, con este perfil concreto. Para cada una: **cumple / parcial / incumple**, por qué, y una mejora si corresponde. La pantalla muestra 5 estados apilados: formulario primario, validación OK, BD local no disponible, parámetros fuera de rango, combinación incompatible. Evaluá los cinco.

### 2.2 Respuesta de la IA

| # | Heurística | Veredicto | Fundamento (resumen) |
|---|---|---|---|
| 1 | Visibilidad del estado | cumple | Stepper, resumen de la secuencia cargada, banner verde al validar, aviso de "si cambiás, se invalida". |
| 2 | Mundo real | cumple | Modo local/remoto, programas BLAST con descripción, "penalización de gaps" apertura/extensión. |
| 3 | Control y libertad | parcial | "Restaurar defaults" borra en silencio los ajustes manuales del sénior. |
| 4 | Consistencia | cumple | Dropdowns, radios, `<details>` — todos estándar. |
| 5 | Prevención de errores | parcial | En el estado de BD no disponible, "Validar" aparece deshabilitado sin decir por qué. |
| 6 | Reconocimiento | parcial | Los parámetros tienen nombre pero no definición. El estudiante no sabe qué es BLOSUM62. |
| 7 | Flexibilidad | parcial | Falta guardar configuraciones como preset. |
| 8 | Minimalista | parcial | Los 5 estados apilados cargan la pantalla. (La IA aclara: si en producción se ve uno a la vez, cumple.) |
| 9 | Recuperación de errores | cumple | Los mensajes de HU06 y HU07 son diagnósticos (campo + rango + opciones válidas). |
| 10 | Ayuda y documentación | incumple | No hay tooltips ni links de ayuda sobre los parámetros. |

### 2.3 Lo que la IA sugirió para los parciales / incumplidos

- H3: confirmación antes de restaurar defaults.
- H5: pista "Validar está deshabilitado porque [X]".
- H6 + H10: tooltips "?" con una línea explicativa en cada parámetro pre-búsqueda.
- H7: guardar/cargar presets.

---

## 3. Revisión del grupo

| Hallazgo | Decisión | Por qué |
|---|---|---|
| H3 — confirmar "Restaurar defaults" | **aceptado** | Mismo criterio que en pantalla 1: acción destructiva pide confirmación. Entra al ajuste. |
| H5 — pista de por qué "Validar" está deshabilitado | **aceptado** | Si no se dice, el flujo queda trabado. Entra al ajuste. |
| H6 + H10 — tooltips de parámetros | **aceptado** (fusionados) | Los dos piden lo mismo. Hacemos tooltips con CSS puro (sin JS). Entra al ajuste. |
| H7 — presets | **rechazado** | No hay HU que lo respalde. Backlog. |
| H8 — densidad excesiva | **rechazado** | Es efecto del maquetado apilado, no de la UI final. La propia IA lo aclara. |

**Cambios que entran al ciclo adicional:** confirmación de "Restaurar defaults", pista de por qué "Validar" está deshabilitado, tooltips sobre los parámetros pre-búsqueda.

---

## 4. Ciclo adicional (ajuste del HTML)

### 4.1 Prompt del ajuste

> Sobre `_inicial.html`, aplicá tres cambios y devolvemelo como `_final.html`, con la regla "sin JS":
>
> 1. Agregá un ícono `?` tipo tooltip (CSS puro con `::after` + `attr(data-tip)`) al lado de cada etiqueta de parámetro pre-búsqueda (E-value, matriz, tamaño de palabra, gaps). Que al menos uno quede expandido por default (clase `show-tip`) para la revisión en papel.
> 2. Debajo del botón "Restaurar defaults", agregá un bloque de confirmación con "Mantener mis valores" y "Sí, restaurar defaults".
> 3. En el estado alternativo de HU04 (BD local no disponible), agregá cerca del botón "Validar" deshabilitado una pista: "Validar está deshabilitado porque falta elegir una base de datos utilizable. Elegí una marcada como *lista*".

### 4.2 Qué quedó en el `_final.html`

- Cuatro íconos `?` con tooltips en los parámetros pre-búsqueda (el de E-value expandido por default).
- Bloque de confirmación de "Restaurar defaults".
- Pista explícita de por qué "Validar" está deshabilitado en el estado de BD no disponible.
- Nota del maquetado al pie, reescrita.

### 4.3 Qué cambiamos nosotros sobre lo que devolvió la IA

- Reescribimos los textos de los tooltips: la IA los había puesto como definiciones de diccionario ("E-value: expectation value, a parameter in sequence alignment"). Los dejamos orientados a decidir: default de `blastp`, cuándo bajarlo, en qué casos usar PAM30 vs BLOSUM62.
- La IA, en una variante intermedia, propuso tooltips también en los dropdowns de "Modo" y "Programa BLAST". No los aceptamos: esos campos ya son autoexplicativos (cada opción tiene su descripción al lado). Más tooltips era ruido.

### 4.4 Resultado

El `_final.html` tiene los tres cambios aceptados. El `_inicial.html` queda para poder comparar.
