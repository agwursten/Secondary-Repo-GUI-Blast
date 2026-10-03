# Evaluación heurística — Pantalla 1: Carga de secuencia

- **Mockup inicial:** [`../mockups/pantalla-01-carga-secuencia_HU01-HU02_inicial.html`](../mockups/pantalla-01-carga-secuencia_HU01-HU02_inicial.html)
- **Mockup final:** [`../mockups/pantalla-01-carga-secuencia_HU01-HU02_final.html`](../mockups/pantalla-01-carga-secuencia_HU01-HU02_final.html)
- **HUs cubiertas:** `HU01_CU001_B`, `HU02_CU001_E1`

---

## 1. Primer ciclo (generación del HTML)

El prompt usado para la generación del HTML y el resumen de la respuesta de la IA están en [`../mockups/README.md`](../mockups/README.md). La salida del primer ciclo es el archivo `_inicial.html`.

---

## 2. Segundo ciclo — Evaluación heurística con IA

### 2.1 Prompt que le pasamos a la IA

> Actuá como especialista en interfaz de usuario. Te paso el HTML de una pantalla de nuestro proyecto LocalBlast (GUI para BLAST+), el perfil del Investigador/a y las HU que cubre la pantalla. Evaluala **heurística por heurística** según las 10 heurísticas de Nielsen, teniendo en cuenta este perfil y no un usuario genérico. Para cada heurística decime si **se cumple, se cumple parcialmente o se incumple**, y por qué. La pantalla muestra apilados cuatro estados (vacío, cargado, carácter inválido, FASTA sin cuerpo): evaluá los cuatro.

### 2.2 Respuesta de la IA

| # | Heurística | Veredicto | Fundamento (resumen) |
|---|---|---|---|
| 1 | Visibilidad del estado | parcial | El stepper y la tarjeta de "cargada" son claros, pero no hay feedback mientras se sube un archivo. |
| 2 | Mundo real | cumple | Lenguaje del dominio (FASTA, alfabeto, aa, inferido). |
| 3 | Control y libertad | parcial | "Reemplazar secuencia" no pide confirmación y la secuencia es la base de todo lo que sigue. |
| 4 | Consistencia | cumple | Botones, zona de drop y banners siguen convenciones web. |
| 5 | Prevención de errores | parcial | Validar on-blur ahorraría un ciclo al estudiante. |
| 6 | Reconocimiento | parcial | El ejemplo FASTA solo aparece como placeholder gris, se pierde al escribir. |
| 7 | Flexibilidad | parcial | No hay reutilización de últimas secuencias ni atajos para el sénior. |
| 8 | Minimalista | cumple | Paleta sobria, sin decoración. |
| 9 | Recuperación de errores | parcial | El error de carácter inválido es excelente; el de "FASTA sin cuerpo" no muestra un ejemplo del formato correcto. |
| 10 | Ayuda y documentación | incumple | No hay ningún link ni popover de ayuda sobre qué es un FASTA. |

### 2.3 Lo que la IA sugirió para los parciales / incumplidos

- H1: estado "subiendo…" para archivos grandes.
- H3: pedir confirmación antes de reemplazar.
- H5: validar on-blur apenas se pega el texto.
- H6 + H10: popover "¿qué es un FASTA?" con ejemplo siempre visible.
- H7: historial de últimas secuencias cargadas; atajo de teclado.
- H9: incluir mini-ejemplo en el banner de error de "FASTA sin cuerpo".

---

## 3. Revisión del grupo

| Hallazgo | Decisión | Por qué |
|---|---|---|
| H1 — feedback de upload | **rechazado** | Las queries típicas son chicas (decenas de KB). Para 10 MB sí haría falta pero no es el caso de las HU del TP1. Backlog. |
| H3 — confirmar "Reemplazar secuencia" | **aceptado** | Reemplazar invalida la config vinculada (HU01 CA-03). Entra al ajuste. |
| H5 — validar on-blur | **rechazado** | Requiere JS y el maquetado se acordó sin JS. Lo anotamos para la implementación. |
| H6 + H10 — ayuda FASTA visible | **aceptado** (fusionados) | Los dos piden lo mismo: ejemplo visible que no desaparezca. Entra al ajuste. |
| H7 — reutilización + atajos | **rechazado** | No hay HU que lo respalde. Backlog. |
| H9 — ejemplo en banner de error | **aceptado** | Coherente con lo que decidimos en H6+H10, aplicado al error. Entra al ajuste. |

**Cambios que entran al ciclo adicional:** confirmación de "Reemplazar", popover con ejemplo FASTA, mini-ejemplo en el banner CA-02.

---

## 4. Ciclo adicional (ajuste del HTML)

### 4.1 Prompt del ajuste

> Sobre el mismo `_inicial.html`, aplicá tres cambios y devolvemelo como `_final.html`, manteniendo todo lo demás y la regla "sin JS":
>
> 1. Popover inline "¿Qué es un FASTA?" junto al título "Secuencia query" del panel, con un recuadro mono-espaciado que muestre un FASTA mínimo bien formado (encabezado + un par de líneas de secuencia proteína). Visible siempre, no solo al hover.
> 2. Debajo de la tarjeta "✓ Secuencia cargada correctamente", agregá un bloque de confirmación con "Mantener la actual" y "Sí, reemplazar" para simular el click en "Reemplazar secuencia".
> 3. En el banner de la excepción "FASTA sin cuerpo" (HU02 CA-02), agregá el mismo recuadro con el FASTA mínimo como ejemplo.

### 4.2 Qué quedó en el `_final.html`

- Popover de ayuda con ejemplo de FASTA al lado del título del panel.
- Bloque de confirmación de "Reemplazar secuencia" con dos botones (mantener / confirmar).
- Mini-ejemplo del FASTA correcto debajo del mensaje de error CA-02.
- Nota del maquetado al pie, reescrita, apuntando a este documento.

### 4.3 Qué cambiamos nosotros sobre lo que devolvió la IA

- Alargamos el ejemplo del FASTA de 2 a 3 líneas, para que se vea el caso típico de secuencia larga.
- Cambiamos el color del botón "Sí, reemplazar" de azul (primario) a ámbar (warning), porque reemplazar borra la configuración vinculada.

### 4.4 Resultado

El `_final.html` tiene los tres cambios aceptados. El `_inicial.html` queda para poder comparar.
