# Casos de Uso — LocalBlast

Los casos de uso se redactan en **formato textual estructurado (Cockburn)** — actor, objetivo, precondición, flujo principal, alternativos, excepciones, postcondición — según pide el TP1, y **no** como diagrama gráfico (Mermaid no incluye un tipo de diagrama de casos de uso nativo).

> El grupo maneja igualmente la notación UML de casos de uso —actor, elipse, límite del sistema, relaciones `<<include>>` / `<<extend>>`, generalización de actores— y puede dibujarla a mano si el docente lo solicita en la presentación. Ej:

<img width="2400" height="1440" alt="casos-de-uso-localblast (3)" src="https://github.com/user-attachments/assets/f585918d-d291-4d89-9012-a77d93b6459a" />

Todos los casos de uso de este documento derivan del proceso profundizado **P1 · Ejecutar búsqueda BLAST** del DFD Nivel 1. Los procesos P2 y P3 quedan documentados a nivel de alcance en el DFD y en el modelo de dominio, pero **no** tienen casos de uso propios en este TP (ver justificación en la sección 5 del [SRS](srs.md#5-selección-de-procesos-a-profundizar)).

Cada caso de uso declara qué requerimientos funcionales realiza. La cadena completa de trazabilidad es:

**RF → CU → slice → HU**

- Un **CU** puede realizar uno o varios RF.
- Cuando el camino feliz de un CU es largo y contiene módulos que aportan valor por sí mismos, se descompone en **slices básicos** (`B1`, `B2`, `B3`, …). Los caminos alternativos válidos se numeran como **slices alternativos** (`A1`, `A2`, …) y las terminaciones abruptas del flujo como **slices de excepción** (`E1`, `E2`, …).
- La relación **slice ↔ HU es 1:1**. La HU que detalla un slice conserva su identificador de origen (por ejemplo `HU01_CU001_B1` detalla el slice `CU001_B1`).

Los slices detallados como HU en este TP son los tres del camino feliz (`B1`, `B2`, `B3`) y una excepción representativa (`E1`). El resto están **nombrados** en este archivo — su detalle como HU llegará cuando algún TP posterior (UX en TP2, diseño en TP4, pruebas en TP5) lo necesite, como aclara la propia guía del TP1.

---

## CU001 · Ejecutar búsqueda BLAST

- **Actor principal:** Investigador/a
- **Actor secundario:** Motor **BLAST+** (invocado por el sistema en ambos modos: local, y remoto con la flag `-remote` — es BLAST+ el que se comunica con NCBI del otro lado, nunca directamente nuestra GUI)
- **Objetivo:** Obtener un conjunto de alineamientos de una secuencia query contra una base de datos, con parámetros configurables, y llevarlos a un archivo descargable en el formato elegido.
- **Realiza:** RF-01, RF-02, RF-03, RF-04, RF-05, RF-06, RF-07, RF-08, RF-09, RF-10
- **Precondición:** Existe al menos una base de datos disponible (local, con su entrada en D1, o remota entre las que ofrece NCBI). El investigador accedió a la interfaz web.
- **Disparador:** El investigador decide iniciar una nueva búsqueda BLAST.
- **Garantía de éxito:** El investigador obtiene un archivo con los alineamientos filtrados en su equipo, y la búsqueda queda registrada en el historial del sistema.
- **Garantía mínima:** El sistema nunca lanza una búsqueda con datos que no pasaron validación, ni deja búsquedas parcialmente ejecutadas que consuman recursos indefinidamente.

### Flujo principal (camino feliz)

1. El investigador ingresa la **secuencia query** subiendo un archivo FASTA desde su equipo o pegando la secuencia como texto en el formulario.
2. El investigador elige el **modo de ejecución**: local o remoto (NCBI). La interfaz muestra una única opción, alternativa, para que la decisión sea clara.
3. El investigador selecciona la **base de datos** de una lista: si eligió modo local, aparecen las bases de datos del catálogo del laboratorio (leídas de D1); si eligió modo remoto, las bases de datos estándar de NCBI.
4. El investigador elige el **programa BLAST** a ejecutar (`blastn`, `blastp`, `blastx`, `tblastn`, `tblastx`).
5. El investigador ajusta los **parámetros pre-búsqueda** (E-value máximo, matriz de sustitución, tamaño de palabra, penalización de gaps). La interfaz ofrece valores por defecto sensatos para no obligar al usuario a completarlos.
6. El investigador presiona **Ejecutar búsqueda**.
7. El sistema **valida** que la secuencia sea reconocible como ADN, ARN o proteína, que los parámetros estén dentro de rangos lógicos, y que la combinación de programa BLAST elegido, tipo de la secuencia query y tipo de la base de datos seleccionada sea **compatible** (por ejemplo, no dejar correr `blastp` sobre una secuencia de nucleótidos).
8. El sistema **invoca a BLAST+** en segundo plano con la combinación de opciones armada a partir de la configuración del formulario (programa, ruta de la base de datos, query, parámetros pre-búsqueda, y la flag `-remote` cuando el modo elegido es remoto), y muestra un indicador de progreso sin bloquear la interfaz. La comunicación con los servidores de NCBI, cuando corresponde, la hace BLAST+ internamente por la flag `-remote`; el sistema solo espera su respuesta.
9. Cuando termina, el sistema muestra la **lista de alineamientos** (hits) en una tabla, con columnas mínimas: identificador del hit, score, E-value observado, % identidad, % cobertura.
10. El investigador ajusta los **filtros post-búsqueda** (umbrales de identidad, cobertura, E-value observado, taxonomía). La tabla se re-filtra en el momento, sin volver a correr BLAST.
11. El investigador elige el **formato de descarga** (CSV, JSON, FASTA, tabular BLAST o XML) y presiona **Descargar**.
12. El sistema entrega el archivo con los resultados filtrados y guarda una copia de la búsqueda en el historial (D2).

**Postcondición:** El investigador tiene un archivo con los alineamientos filtrados en su equipo. La búsqueda queda registrada en el historial del sistema.

### Descomposición en slices

El camino feliz de 12 pasos es grande y contiene tres módulos que aportan valor en sí mismos hacia el objetivo del CU: configurar y validar una búsqueda (deja lista una búsqueda ejecutable), ejecutar y ver los resultados crudos (deja los alineamientos frente al investigador), y refinar y descargar (deja el archivo entregable). Se descompone en tres slices básicos, más los slices alternativos y de excepción que se explican debajo.

```
CU001 · Ejecutar búsqueda BLAST
├─ Camino feliz (slices básicos)
│  ├─ CU001_B1  — pasos 1-7:  cargar, configurar y validar la búsqueda
│  ├─ CU001_B2  — pasos 8-9:  ejecutar la búsqueda y presentar resultados crudos
│  └─ CU001_B3  — pasos 10-12: filtrar, descargar y persistir la búsqueda
├─ Caminos alternativos (slices A)
│  ├─ CU001_A1  — cancelación manual de la búsqueda en curso
│  ├─ CU001_A2  — ningún resultado supera los filtros post-búsqueda
│  └─ CU001_A3  — base de datos local no disponible
└─ Terminaciones abruptas (slices E)
   ├─ CU001_E1  — secuencia query con formato inválido
   ├─ CU001_E2  — parámetros pre-búsqueda fuera de rango
   ├─ CU001_E3  — combinación programa / query / base de datos incompatible
   └─ CU001_E4  — fallo del modo remoto de BLAST+
```

### Slices básicos — descripción

- **`CU001_B1` · Cargar, configurar y validar la búsqueda (pasos 1-7).** El investigador ingresa la secuencia query, elige el modo (local o remoto), la base de datos correspondiente, el programa BLAST y los parámetros pre-búsqueda; al presionar **Ejecutar búsqueda**, el sistema valida el alfabeto de la secuencia, los rangos de los parámetros y la compatibilidad programa/query/base de datos. **Valor entregado:** una búsqueda queda configurada y validada, lista para ser ejecutada. **Realiza:** RF-01, RF-02, RF-03, RF-04, RF-05, RF-06.
- **`CU001_B2` · Ejecutar la búsqueda y presentar resultados crudos (pasos 8-9).** El sistema invoca a BLAST+ con la configuración ya validada, muestra un indicador de progreso sin bloquear la interfaz y, al terminar, presenta la tabla de alineamientos con las columnas mínimas. **Valor entregado:** el investigador ve los hits crudos de BLAST. **Realiza:** RF-07, RF-08.
- **`CU001_B3` · Filtrar, descargar y persistir la búsqueda (pasos 10-12).** El investigador aplica filtros post-búsqueda sobre la tabla (sin volver a correr BLAST), elige un formato de descarga y baja el archivo; el sistema guarda la búsqueda y sus resultados en el historial (D2). **Valor entregado:** un archivo de resultados filtrados en el equipo del investigador. **Realiza:** RF-09, RF-10.

### Slices alternativos — descripción

Son caminos válidos alternativos al flujo principal; el sistema sigue funcionando y el CU puede alcanzar (o no) el objetivo por otra ruta.

- **`CU001_A1` · Cancelación manual de la búsqueda.** Mientras la búsqueda está en ejecución (durante el slice `CU001_B2`), el investigador presiona **Cancelar**. El sistema aborta el subproceso local o cancela la solicitud remota a través de BLAST+, y deja la interfaz lista para iniciar una nueva búsqueda. **Realiza:** RF-07.
- **`CU001_A2` · Ningún resultado supera los filtros post-búsqueda.** En el slice `CU001_B3`, los filtros elegidos por el investigador dejan la tabla vacía. El sistema no impide la descarga: entrega un archivo con encabezados y los metadatos de la búsqueda (parámetros, base de datos, timestamp) pero sin filas de hits, y guarda igualmente la búsqueda en D2, para que el investigador tenga constancia del intento. **Realiza:** RF-09, RF-10.
- **`CU001_A3` · Base de datos local no disponible.** En el paso 3, el investigador seleccionó modo local y una base de datos que en ese momento no está lista en D1 (por ejemplo, se está actualizando desde P3, o su índice quedó marcado con error). El sistema informa el estado de esa base de datos y su motivo, y devuelve al investigador al paso 3 con la lista de bases de datos locales actualizada. El investigador decide por su cuenta qué hacer a continuación (elegir otra base local, cambiar de modo, o cancelar); el sistema **no** propone equivalencias entre bases locales y remotas, porque no las hay: una base propia del laboratorio no es intercambiable con las bases estándar de NCBI. **Realiza:** RF-03.

### Slices de excepción — descripción

Son terminaciones abruptas del flujo: el sistema detecta una condición que impide continuar, corta la ejecución del CU y notifica al investigador. La postcondición del CU no se alcanza.

- **`CU001_E1` · Secuencia query con formato inválido.** En el paso 7, la validación detecta que la secuencia ingresada no tiene formato reconocible (caracteres fuera del alfabeto de ADN/ARN/proteína, FASTA mal formado, encabezado sin cuerpo, longitud fuera de rango). El sistema no invoca a BLAST+, corta el flujo y muestra un mensaje que indica exactamente el problema y dónde aparece. **Realiza:** RF-06.
- **`CU001_E2` · Parámetros pre-búsqueda fuera de rango.** En el paso 7, la validación detecta al menos un parámetro con valor imposible (E-value negativo, tamaño de palabra fuera del rango soportado, penalización de gap fuera de escala). El sistema corta el flujo y señala qué campo corregir y cuál es el rango esperado. **Realiza:** RF-04, RF-06.
- **`CU001_E3` · Combinación programa / query / base de datos incompatible.** En el paso 7, la verificación de compatibilidad detecta que el programa BLAST elegido no coincide con el tipo de la secuencia query o con el tipo de la base de datos seleccionada (por ejemplo `blastp` con query de nucleótidos, o `blastn` contra una base de datos de proteínas). El sistema corta el flujo, indica el motivo de la incompatibilidad y sugiere qué combinaciones sí son válidas para lo que el usuario ya cargó. **Realiza:** RF-05.
- **`CU001_E4` · Fallo del modo remoto de BLAST+.** En el paso 8, con modo remoto seleccionado, BLAST+ reporta un error de comunicación con NCBI (sin respuesta, timeout, o error explícito devuelto por la API). El sistema captura el error de BLAST+, corta el flujo del CU e informa al investigador con el detalle del error. Un reintento posterior es un CU nuevo, no la continuación de este. **Realiza:** RF-07.

---

## Trazabilidad RF → CU → slice

La tabla completa `RF → CU → slice → HU` (con las HU incluidas) está en [`historias-usuario.md`](historias-usuario.md). Acá se resume la parte `RF → CU → slice`:

| RF | CU | Slice(s) que lo realizan |
|---|---|---|
| RF-01 | CU001 | B1 |
| RF-02 | CU001 | B1 |
| RF-03 | CU001 | B1, A3 |
| RF-04 | CU001 | B1, E2 |
| RF-05 | CU001 | B1, E3 |
| RF-06 | CU001 | B1, E1, E2 |
| RF-07 | CU001 | B2, A1, E4 |
| RF-08 | CU001 | B2 |
| RF-09 | CU001 | B3, A2 |
| RF-10 | CU001 | B3, A2 |

Un mismo RF puede aparecer en varios slices — por ejemplo RF-06 (validación pre-ejecución) se realiza parcialmente en el camino feliz (`B1`, cuando la validación pasa) y también en las excepciones `E1` y `E2` (cuando la validación falla y corta el flujo). Esa dispersión es esperable: los slices de excepción son, justamente, otra forma en que se cumple el RF de validación.
