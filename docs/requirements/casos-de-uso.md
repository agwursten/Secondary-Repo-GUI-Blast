# Casos de Uso — LocalBlast

Los casos de uso se redactan en **formato textual estructurado (Cockburn)** — actor, objetivo, precondición, flujo principal, postcondición — según pide el TP1, y **no** como diagrama gráfico (Mermaid no incluye un tipo de diagrama de casos de uso nativo).

> El grupo maneja igualmente la notación UML de casos de uso —actor, elipse, límite del sistema, relaciones `<<include>>` / `<<extend>>`, generalización de actores— y puede dibujarla a mano si el docente lo solicita en la presentación.

Cada caso de uso declara qué requerimientos funcionales realiza (trazabilidad **RF → CU → slice → HU**). Los slices secundarios se **nombran** en este TP; su detalle como historias de usuario está en [`historias-usuario.md`](historias-usuario.md).

---

## CU-01 · Ejecutar búsqueda BLAST

- **Actor principal:** Investigador/a
- **Actor secundario:** Servicio remoto NCBI (en modo remoto), Motor BLAST+ local (en modo local)
- **Objetivo:** Obtener un conjunto de alineamientos de una secuencia query contra una base de datos, con parámetros configurables, y llevarlos a un archivo descargable en el formato elegido.
- **Realiza:** RF-01, RF-02, RF-03, RF-04, RF-05, RF-06, RF-07, RF-08, RF-09, RF-10
- **Precondición:** Existe al menos una base de datos disponible (local, en D1, o remota vía NCBI). El investigador accedió a la interfaz web.

### Flujo principal (slice básico) — camino feliz

1. El investigador ingresa la **secuencia query** en el formulario, pegándola como texto o subiéndola como archivo FASTA.
2. El investigador elige el **modo de ejecución**: local o remoto (NCBI). La interfaz muestra una única opción, alternativa, para que la decisión sea clara.
3. El investigador selecciona la **base de datos** de una lista: si eligió modo local, aparecen las bases de datos del catálogo del laboratorio (leídas de D1); si eligió modo remoto, las bases de datos estándar de NCBI.
4. El investigador ajusta los **parámetros pre-búsqueda** (E-value máximo, matriz de sustitución, tamaño de palabra, penalización de gaps). La interfaz ofrece valores por defecto sensatos para no obligar al usuario a completarlos.
5. El investigador presiona **Ejecutar búsqueda**.
6. El sistema **valida** que los parámetros estén dentro de rangos lógicos (E-value positivo, matriz compatible con el tipo de secuencia, etc.) y que la secuencia sea reconocible como ADN, ARN o proteína.
7. El sistema **lanza la ejecución en segundo plano** y muestra un indicador de progreso, sin bloquear la interfaz. En modo remoto envía la consulta a NCBI y hace polling; en modo local invoca al binario BLAST+ contra los índices de D1.
8. Cuando termina, el sistema muestra la **lista de alineamientos** (hits) en una tabla, con columnas mínimas: identificador del hit, score, E-value observado, % identidad, % cobertura.
9. El investigador ajusta los **filtros post-búsqueda** (umbrales de identidad, cobertura, E-value observado, taxonomía). La tabla se re-filtra en el momento, sin volver a correr BLAST.
10. El investigador elige el **formato de descarga** (CSV, JSON, FASTA, tabular BLAST o XML) y presiona **Descargar**.
11. El sistema entrega el archivo con los resultados filtrados y guarda una copia de la búsqueda en el historial (D2).

**Postcondición:** El investigador tiene un archivo con los alineamientos filtrados en su equipo. La búsqueda queda registrada en el historial del sistema.

### Slices secundarios nombrados

- **A1 · Secuencia con formato inválido.** El sistema detecta que la secuencia ingresada no tiene formato reconocible (caracteres inválidos, FASTA mal formado, longitud fuera de rango), indica exactamente el problema, y no lanza la búsqueda.
- **A2 · Parámetros pre-búsqueda fuera de rango.** El sistema detecta al menos un parámetro con valor imposible (E-value negativo, tamaño de palabra fuera del rango soportado, matriz incompatible con el tipo de secuencia elegido) y señala qué campo corregir.
- **A3 · Base de datos local no disponible.** El investigador seleccionó modo local y una base de datos que en ese momento no está lista en D1 (por ejemplo, se está actualizando desde P3). El sistema informa el estado y sugiere elegir otra base de datos o cambiar a modo remoto.
- **A4 · Fallo del servicio remoto NCBI.** En modo remoto, NCBI no responde, devuelve error, o supera el timeout. El sistema informa el problema y ofrece reintentar o cambiar a modo local si hay una base de datos equivalente disponible.
- **A5 · Cancelación manual de la búsqueda.** El investigador cancela una búsqueda que ya está en ejecución. El sistema aborta el subproceso local o cancela la solicitud remota, y deja la interfaz lista para una nueva búsqueda.
- **A6 · Ningún resultado supera los filtros post-búsqueda.** El sistema no impide la descarga: entrega un reporte vacío pero con los metadatos de la búsqueda, para que el investigador tenga constancia del intento.

---

## CU-02 · Administrar base de datos BLAST local

- **Actor principal:** Administrador/a
- **Objetivo:** Mantener el catálogo de bases de datos locales disponibles para búsqueda, dando de alta nuevas bases (a partir de archivos FASTA subidos o de fuentes públicas como SwissProt), actualizándolas o dándolas de baja.
- **Realiza:** RF-11, RF-12, RF-13, RF-14
- **Precondición:** El administrador está autenticado con rol de administrador y accedió a la sección de administración de bases de datos.

### Flujo principal (slice básico) — camino feliz

1. El administrador accede a la sección **Administración de bases de datos** y ve el catálogo actual, con: nombre, tipo (nucleótidos / proteínas), tamaño, fecha de alta y estado.
2. El administrador elige **Dar de alta una nueva base de datos**.
3. El sistema le pide: **nombre visible** de la base de datos, **tipo** (nucleótidos o proteínas) y **origen del archivo FASTA** (subir un archivo local, o indicar la URL de una fuente pública como SwissProt).
4. El administrador completa los datos y presiona **Crear base de datos**.
5. El sistema valida que el FASTA sea legible y consistente con el tipo declarado.
6. El sistema lanza en segundo plano la construcción de los índices con `makeblastdb`, muestra un indicador de progreso y no bloquea la interfaz.
7. Al terminar, el sistema agrega la base de datos al catálogo con estado **Disponible**, la persiste en D1, y notifica al administrador que ya puede usarse en el CU-01.

**Postcondición:** La nueva base de datos aparece en el catálogo y queda disponible para que los investigadores la seleccionen en el CU-01.

### Slices secundarios nombrados

- **A1 · FASTA inválido o inconsistente con el tipo declarado.** El sistema detecta que el archivo no es FASTA legible, o que su contenido no coincide con el tipo declarado (por ejemplo se subió FASTA de proteínas indicando "nucleótidos"). Informa el problema y no crea la base de datos.
- **A2 · Actualización de una base de datos existente.** El administrador sube una versión nueva del FASTA para una base de datos ya presente en el catálogo; el sistema reconstruye los índices y actualiza la fecha, sin cambiar el nombre visible ni el resto de sus metadatos. Las búsquedas en curso sobre la versión anterior no se interrumpen.
- **A3 · Baja de una base de datos.** El administrador quita una base de datos del catálogo. El sistema pide confirmación explícita, libera los índices en D1 y deja constancia en el registro. Las búsquedas históricas que la usaron siguen visibles en el historial, marcadas con la nota de que la base de datos ya no existe.
- **A4 · Falla la construcción del índice.** `makeblastdb` termina con error (falta de espacio, FASTA corrupto detectado a mitad, etc.). El sistema informa el error crudo y no agrega la base de datos al catálogo.

---

## Trazabilidad RF → CU

| Requerimiento funcional | Caso de uso que lo realiza |
|---|---|
| RF-01 a RF-10 | CU-01 |
| RF-11 a RF-14 | CU-02 |

La trazabilidad completa **RF → CU → slice → HU** se ve en [`historias-usuario.md`](historias-usuario.md), donde cada HU declara explícitamente de qué slice se deriva.
