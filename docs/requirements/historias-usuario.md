# Historias de Usuario — LocalBlast

Cada historia de usuario detalla un **slice** puntual de un caso de uso, con el formato:

- **Origen**: qué CU y qué slice detalla.
- **Rol – meta – motivo**: "Como … quiero … para …".
- **Criterios de aceptación** en formato Given-When-Then, trazables a la precondición y postcondición **del slice**, no del CU completo.

Para el TP1 se detallan las historias del **slice básico** (camino feliz) de cada caso de uso profundizado, más una historia sobre un slice secundario relevante por CU. El resto de los slices secundarios están **nombrados en los casos de uso** y se detallarán como HU cuando algún TP posterior (UX en TP2, diseño en TP4, pruebas en TP5) los necesite — no es obligación abrirlos ya, según la propia guía del TP1.

---

## HU derivadas de CU-01 · Ejecutar búsqueda BLAST

### HU-01 · Ejecutar una búsqueda BLAST completa desde la interfaz web

**Deriva de:** CU-01, slice básico
**Realiza:** RF-01 a RF-10

> **Como** investigador/a,
> **quiero** cargar una secuencia, elegir si la búsqueda se corre local o remota, ajustar los parámetros del algoritmo y descargar los resultados filtrados desde una misma interfaz web,
> **para** obtener alineamientos sin depender de la línea de comandos ni cargar la web oficial de NCBI para cada consulta.

**Criterios de aceptación**

- **CA-01.1 · Camino feliz en modo remoto**
  - **Given** que ingresé una secuencia FASTA válida, elegí modo remoto contra la base "nr" de NCBI, y dejé los parámetros pre-búsqueda en sus valores por defecto,
  - **When** presiono "Ejecutar búsqueda",
  - **Then** la interfaz muestra un indicador de progreso mientras la consulta está en curso y, al terminar, presenta la tabla de alineamientos con al menos las columnas: identificador del hit, score, E-value observado, % identidad y % cobertura.

- **CA-01.2 · Camino feliz en modo local**
  - **Given** que hay al menos una base de datos local disponible en el catálogo, ingresé una secuencia válida, elegí modo local con esa base y dejé los parámetros por defecto,
  - **When** presiono "Ejecutar búsqueda",
  - **Then** el sistema ejecuta la búsqueda contra los índices locales y presenta la tabla de resultados con las mismas columnas mínimas que en modo remoto.

- **CA-01.3 · Descarga del reporte en el formato elegido**
  - **Given** que la búsqueda finalizó y estoy viendo la tabla de resultados con los filtros post-búsqueda aplicados,
  - **When** selecciono un formato (por ejemplo CSV) y presiono "Descargar",
  - **Then** el sistema entrega un archivo en ese formato que contiene únicamente los hits que superan los filtros post-búsqueda activos, y guarda una copia de la búsqueda en el historial del sistema.

---

### HU-01.A1 · Manejo de secuencia con formato inválido

**Deriva de:** CU-01, slice A1
**Realiza:** RF-06

> **Como** investigador/a,
> **quiero** recibir un mensaje claro cuando la secuencia que pego o subo no es reconocible,
> **para** poder corregirla sin tener que adivinar qué le pasa.

**Criterios de aceptación**

- **CA-01.A1.1 · Secuencia con caracteres no permitidos**
  - **Given** que ingresé como query una cadena que contiene caracteres fuera del alfabeto de ADN, ARN o proteína,
  - **When** presiono "Ejecutar búsqueda",
  - **Then** el sistema no lanza la ejecución y muestra un mensaje que indica cuál es el carácter inválido y en qué posición aparece.

- **CA-01.A1.2 · FASTA con encabezado pero sin secuencia**
  - **Given** que subí un archivo FASTA con línea de encabezado (`>ID`) pero cuerpo vacío,
  - **When** presiono "Ejecutar búsqueda",
  - **Then** el sistema no lanza la ejecución y muestra el mensaje "El FASTA contiene un encabezado pero ninguna secuencia asociada".

---

## HU derivadas de CU-02 · Administrar base de datos BLAST local

### HU-02a · Dar de alta una base de datos BLAST subiendo un FASTA

**Deriva de:** CU-02, slice básico
**Realiza:** RF-11, RF-12, RF-14

> **Como** administrador/a del sistema,
> **quiero** subir un archivo FASTA y darlo de alta como una nueva base local,
> **para** que los investigadores del laboratorio puedan usarla en sus búsquedas locales.

**Criterios de aceptación**

- **CA-02a.1 · Alta exitosa de una base local a partir de un FASTA propio del laboratorio**
  - **Given** que estoy autenticado con rol de administrador, dispongo de un archivo FASTA válido de proteínas del laboratorio, y accedí a la sección "Administración de bases de datos",
  - **When** completo el formulario con nombre visible, tipo "proteínas" y el archivo FASTA, y presiono "Crear base",
  - **Then** el sistema ejecuta la construcción de índices en segundo plano, y al terminar la base aparece en el catálogo con estado "Disponible" y queda listada como opción para el investigador en el CU-01.

- **CA-02a.2 · Alta desde una fuente pública indicando URL (SwissProt)**
  - **Given** que estoy autenticado como administrador y quiero dar de alta la base SwissProt,
  - **When** en el formulario elijo la opción "URL pública", pego la URL del FASTA de SwissProt y presiono "Crear base",
  - **Then** el sistema descarga el FASTA desde la URL, construye los índices y agrega la base al catálogo con estado "Disponible".

---

### HU-02.A1 · Rechazo de FASTA inconsistente con el tipo declarado

**Deriva de:** CU-02, slice A1
**Realiza:** RF-13

> **Como** administrador/a,
> **quiero** que el sistema me alerte si el FASTA que subí no corresponde con el tipo de base que declaré,
> **para** no dejar en el catálogo bases mal etiquetadas que después arruinen las búsquedas.

**Criterios de aceptación**

- **CA-02.A1.1 · FASTA de proteínas subido declarando tipo "nucleótidos"**
  - **Given** que declaré tipo "nucleótidos" en el formulario y subí un archivo FASTA cuyas secuencias contienen aminoácidos no válidos como bases,
  - **When** presiono "Crear base",
  - **Then** el sistema no agrega la base al catálogo y muestra el mensaje "El contenido del FASTA no coincide con el tipo declarado (nucleótidos)", explicando cuál es el carácter que rompe la coincidencia.

- **CA-02.A1.2 · Archivo que no es FASTA**
  - **Given** que subí un archivo cuyo contenido no respeta la estructura FASTA (ninguna línea comienza con `>`),
  - **When** presiono "Crear base",
  - **Then** el sistema no agrega la base al catálogo y muestra el mensaje "El archivo no es un FASTA válido".

---

## Tabla de trazabilidad RF → CU → slice → HU

| RF | CU | Slice | HU |
|---|---|---|---|
| RF-01, RF-02, RF-03, RF-04, RF-05, RF-06, RF-07, RF-08, RF-09, RF-10 | CU-01 | básico | HU-01 |
| RF-06 | CU-01 | A1 | HU-01.A1 |
| CU-01 | A2, A3, A4, A5, A6 | *(nombrados, sin detallar aún)* | |
| RF-11, RF-12, RF-14 | CU-02 | básico | HU-02a |
| RF-13 | CU-02 | A1 | HU-02.A1 |
| CU-02 | A2, A3, A4 | *(nombrados, sin detallar aún)* | |

Los slices nombrados sin HU detallada no son un olvido: la propia guía del TP1 aclara que "no todo slice justifica ese nivel de inversión" y que se detallan solo cuando un TP posterior los necesita.
