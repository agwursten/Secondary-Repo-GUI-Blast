# Historias de Usuario — LocalBlast

Cada historia de usuario detalla un **slice** puntual de un caso de uso, con el formato:

- **Origen**: qué CU y qué slice detalla.
- **Rol – meta – motivo**: "Como … quiero … para …".
- **Escenarios de aceptación**: descripción en prosa de las situaciones concretas en las que la historia queda cumplida, trazables a la precondición y postcondición del **slice** correspondiente.

Para el TP1 se detallan las historias del **slice básico** (camino feliz) de cada caso de uso profundizado, más una historia sobre un slice secundario relevante por CU. El resto de los slices secundarios están **nombrados en los casos de uso** y se detallarán como HU cuando algún TP posterior (UX en TP2, diseño en TP4, pruebas en TP5) los necesite — no es obligación abrirlos ya, según la propia guía del TP1.

> **Nota:** el formato Given-When-Then para los criterios de aceptación queda pendiente para una entrega posterior; por ahora los escenarios se redactan en prosa.

---

## HU derivadas de CU-01 · Ejecutar búsqueda BLAST

### HU-01 · Ejecutar una búsqueda BLAST completa desde la interfaz web

**Deriva de:** CU-01, slice básico
**Realiza:** RF-01 a RF-10

> **Como** investigador/a,
> **quiero** cargar una secuencia, elegir si la búsqueda se corre local o remota, ajustar los parámetros del algoritmo y descargar los resultados filtrados desde una misma interfaz web,
> **para** obtener alineamientos sin depender de la línea de comandos ni cargar la web oficial de NCBI para cada consulta.

**Escenarios de aceptación**

- **EA-01.1 · Camino feliz en modo remoto.** El investigador ingresa una secuencia FASTA válida en el formulario, elige modo remoto contra la base de datos "nr" de NCBI, deja los parámetros pre-búsqueda en sus valores por defecto y presiona "Ejecutar búsqueda". La interfaz muestra un indicador de progreso mientras la consulta está en curso y, al terminar, presenta la tabla de alineamientos con al menos las columnas: identificador del hit, score, E-value observado, porcentaje de identidad y porcentaje de cobertura.

- **EA-01.2 · Camino feliz en modo local.** Existe al menos una base de datos local en el catálogo. El investigador ingresa una secuencia válida, elige modo local contra esa base de datos y deja los parámetros por defecto. Al presionar "Ejecutar búsqueda", el sistema ejecuta la consulta contra los índices locales y presenta la tabla de resultados con las mismas columnas mínimas que en el escenario anterior.

- **EA-01.3 · Descarga del reporte en el formato elegido.** La búsqueda finalizó y el investigador está viendo la tabla de resultados con los filtros post-búsqueda aplicados. Selecciona un formato (por ejemplo CSV) y presiona "Descargar". El sistema entrega un archivo en ese formato que contiene únicamente los hits que superan los filtros post-búsqueda activos, y guarda una copia de la búsqueda en el historial del sistema.

---

### HU-01.A1 · Manejo de secuencia con formato inválido

**Deriva de:** CU-01, slice A1
**Realiza:** RF-06

> **Como** investigador/a,
> **quiero** recibir un mensaje claro cuando la secuencia que pego o subo no es reconocible,
> **para** poder corregirla sin tener que adivinar qué le pasa.

**Escenarios de aceptación**

- **EA-01.A1.1 · Secuencia con caracteres no permitidos.** El investigador ingresa como query una cadena que contiene caracteres fuera del alfabeto de ADN, ARN o proteína, y presiona "Ejecutar búsqueda". El sistema no lanza la ejecución y muestra un mensaje que indica cuál es el carácter inválido y en qué posición aparece.

- **EA-01.A1.2 · FASTA con encabezado pero sin secuencia.** El investigador sube un archivo FASTA con línea de encabezado (`>ID`) pero cuerpo vacío, y presiona "Ejecutar búsqueda". El sistema no lanza la ejecución y muestra el mensaje "El FASTA contiene un encabezado pero ninguna secuencia asociada".

---

## HU derivadas de CU-02 · Administrar base de datos BLAST local

### HU-02a · Dar de alta una base de datos BLAST subiendo un FASTA

**Deriva de:** CU-02, slice básico
**Realiza:** RF-11, RF-12, RF-14

> **Como** administrador/a del sistema,
> **quiero** subir un archivo FASTA y darlo de alta como una nueva base de datos local,
> **para** que los investigadores del laboratorio puedan usarla en sus búsquedas locales.

**Escenarios de aceptación**

- **EA-02a.1 · Alta exitosa a partir de un FASTA propio del laboratorio.** El administrador está autenticado con rol de administrador, dispone de un archivo FASTA válido de proteínas del laboratorio y accedió a la sección "Administración de bases de datos". Completa el formulario con nombre visible, tipo "proteínas" y el archivo FASTA, y presiona "Crear base de datos". El sistema ejecuta la construcción de índices en segundo plano y, al terminar, la nueva base de datos aparece en el catálogo con estado "Disponible" y queda listada como opción para el investigador en el CU-01.

- **EA-02a.2 · Alta desde una fuente pública indicando URL (SwissProt).** El administrador está autenticado y quiere dar de alta la base de datos SwissProt. En el formulario elige la opción "URL pública", pega la URL del FASTA de SwissProt y presiona "Crear base de datos". El sistema descarga el FASTA desde la URL, construye los índices y agrega la base de datos al catálogo con estado "Disponible".

---

### HU-02.A1 · Rechazo de FASTA inconsistente con el tipo declarado

**Deriva de:** CU-02, slice A1
**Realiza:** RF-13

> **Como** administrador/a,
> **quiero** que el sistema me alerte si el FASTA que subí no corresponde con el tipo de base de datos que declaré,
> **para** no dejar en el catálogo bases de datos mal etiquetadas que después arruinen las búsquedas.

**Escenarios de aceptación**

- **EA-02.A1.1 · FASTA de proteínas subido declarando tipo "nucleótidos".** El administrador declaró tipo "nucleótidos" en el formulario y subió un archivo FASTA cuyas secuencias contienen aminoácidos no válidos como bases nitrogenadas. Al presionar "Crear base de datos", el sistema no agrega la base de datos al catálogo y muestra el mensaje "El contenido del FASTA no coincide con el tipo declarado (nucleótidos)", explicando cuál es el carácter que rompe la coincidencia.

- **EA-02.A1.2 · Archivo que no es FASTA.** El administrador subió un archivo cuyo contenido no respeta la estructura FASTA (ninguna línea comienza con `>`). Al presionar "Crear base de datos", el sistema no agrega la base de datos al catálogo y muestra el mensaje "El archivo no es un FASTA válido".

---

## Tabla de trazabilidad RF → CU → slice → HU

| RF | CU | Slice | HU |
|---|---|---|---|
| RF-01, RF-02, RF-03, RF-04, RF-05, RF-06, RF-07, RF-08, RF-09, RF-10 | CU-01 | básico | HU-01 |
| RF-06 | CU-01 | A1 | HU-01.A1 |
| — | CU-01 | A2, A3, A4, A5, A6 | *(nombrados, sin detallar aún)* |
| RF-11, RF-12, RF-14 | CU-02 | básico | HU-02a |
| RF-13 | CU-02 | A1 | HU-02.A1 |
| — | CU-02 | A2, A3, A4 | *(nombrados, sin detallar aún)* |

Los slices nombrados sin HU detallada no son un olvido: la propia guía del TP1 aclara que "no todo slice justifica ese nivel de inversión" y que se detallan solo cuando un TP posterior los necesita.
