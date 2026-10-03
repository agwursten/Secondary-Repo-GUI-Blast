# Perfil de usuario — Investigador/a sénior o Docente de bioinformática / biología molecular

> Perfil del actor **Investigador/a** del TP1, en el subgrupo de stakeholders *"Investigadores y Docentes de Bioinformática / Biología Molecular"* identificado en [SRS §2.1](../../requeriments/srs.md#21-stakeholders). Comparte el actor del sistema con el perfil [`investigador-estudiante.md`](investigador-estudiante.md) —ambos subgrupos usan las mismas capacidades habilitadas, HU01 a HU14—, pero el objetivo con el que entra al sistema, el nivel de conocimiento técnico y los puntos de dolor son distintos.

## 1. Perfil de usuario

### Quién es

Investigador/a o docente de un grupo de bioinformática o biología molecular. Trabaja con secuencias como parte habitual de su labor profesional: puede estar analizando resultados de un experimento, preparando material para una clase, o colaborando con un grupo que mantiene bases de datos propias del laboratorio (SwissProt espejado localmente, genomas de interés del grupo, etc.).

Rastreo: SRS §2.1 lo caracteriza como *"Investigadores y Docentes de Bioinformática / Biología Molecular"*. El TP1 no afirma más atributos personales sobre este perfil; cualquier detalle demográfico fino no está respaldado y por lo tanto no se incluye.

### Objetivo que persigue con el sistema

Correr alineamientos BLAST **sobre bases de datos del laboratorio o estándar**, **explorar los resultados interactivamente** con filtros que la web oficial de NCBI no ofrece (umbrales de identidad, cobertura, E-value observado, taxonomía) y **llevarse el subconjunto filtrado** en un formato que después puede procesar fuera del sistema (CSV para una planilla, FASTA para alimentar otro pipeline, XML / tabular BLAST para scripts existentes).

Rastreo: SRS §2.1 — *"buscan una herramienta ágil e intuitiva para explorar resultados con filtros visuales personalizados que no están disponibles de forma nativa en la web tradicional"*; SRS §1.2 — *"Los resultados se descargan en CSV, JSON, FASTA, tabular BLAST o XML"*; SRS §1.3 incluye en el alcance *"Aplicación interactiva de filtros post-búsqueda sobre la tabla de resultados"* y *"Descarga de resultados en múltiples formatos"*.

### Contexto de uso

- **Lugar.** La oficina / box del grupo de investigación, o el laboratorio donde está la computadora conectada a las bases locales. En algunos casos también desde su casa, cuando el servidor del laboratorio es accesible por red. **Supuesto del grupo:** el TP1 no fija ubicación concreta, se infiere de "laboratorio" y de la existencia de un catálogo local de bases administradas por el grupo (SRS §9).
- **Dispositivo.** Laptop o PC de escritorio con un navegador moderno. Suele tener a mano una terminal, un editor y una planilla; es común que use LocalBlast en una pestaña y abra el CSV descargado en otra ventana. **Supuesto del grupo:** el TP1 fija "Interfaz web" ([SRS §1.3](../../requeriments/srs.md#13-dentro-del-alcance)) pero no describe el flujo multiventana; se infiere del uso que la propuesta de valor del sistema promete.
- **Urgencia.** Variable, pero típicamente **menor que la del estudiante**: el trabajo es exploratorio, no está contra una fecha de entrega semanal. **Supuesto del grupo:** no está en el TP1 explícitamente; se infiere del contraste con la descripción del subgrupo "estudiantes" en SRS §2.1 (*"alineamientos rápidos"*) frente a la del subgrupo sénior (*"explorar resultados con filtros visuales personalizados"*, una tarea más deliberativa).
- **Frecuencia de uso.** Alta y sostenida: puede ser una herramienta de uso cotidiano o cuasi-cotidiano durante proyectos activos. **Supuesto del grupo**.

### Nivel de conocimiento técnico

- **Dominio (biología molecular / bioinformática).** Alto. Entiende perfectamente la diferencia entre `blastn`, `blastp`, `blastx`, `tblastn` y `tblastx`, sabe elegir una matriz de sustitución, interpreta E-values de memoria y tiene criterios formados sobre qué umbrales de identidad / cobertura son razonables para su pregunta biológica. Rastreo: SRS §2.1 explícito — *"Bioinformática / Biología Molecular"*.
- **Herramientas.** Usa (o usó) BLAST+ por línea de comandos y conoce las opciones de la CLI, pero **la fricción de armar comandos y parsear salida a mano le hace preferir una GUI**, siempre que la GUI no le saque control sobre los parámetros. Rastreo: README §1 lo coloca entre los stakeholders del canvas de descubrimiento, lo cual implica que es un stakeholder al que la CLI y la web actuales no le alcanzan.
- **Lectura de documentación técnica.** La maneja bien, pero no quiere tener que recurrir a ella para cada búsqueda; valora que el sistema le haga lo repetitivo —cargar la secuencia, armar el formulario, parsear la salida— sin obligarlo a repasar flags.

### Limitaciones y frustraciones que condicionan su uso

- **La web oficial de NCBI no deja filtrar interactivamente los resultados.** Para rehacer un filtro distinto hoy tiene que descargar la salida y procesarla por fuera, o volver a correr la búsqueda. Rastreo: SRS §1.1 — *"no ofrece filtros interactivos post-búsqueda (identidad, cobertura, taxonomía) sobre la lista de resultados"*; README §1 — *"carece de opciones avanzadas de filtrado directo e interactivo (como filtros instantáneos por % de identidad o cobertura posterior a la búsqueda)"*.
- **La web oficial de NCBI no corre contra bases del laboratorio.** Cuando el grupo tiene sus propios índices BLAST curados —de un genoma de interés, de una colección propia— la web pública no sirve, y tiene que irse a la terminal con los binarios locales. Rastreo: SRS §1.1 — *"no permite ejecutar contra bases de datos propias del laboratorio"*; SRS §1.3 habilita explícitamente este modo mixto (local + remoto desde la misma interfaz).
- **BLAST+ y NCBI fallan seguido en la práctica.** Timeouts del modo remoto, rate limits, errores inesperados; necesita que cuando algo falla la interfaz le diga **exactamente qué** falló —el mensaje literal de BLAST+ / NCBI, no una traducción propia— para distinguir un problema de red temporal de uno más grave. Rastreo: `HU10_CU004_E1` describe este tipo de uso: *"quiero … que el sistema me muestre el error tal como lo devolvió BLAST+ (o NCBI a través de BLAST+)"*; también escenarios de calidad del TP2 Parte A sobre tolerancia a fallos.
- **Base local en estado inconsistente.** Si la base del laboratorio que planeaba usar está actualizándose o tiene índices corruptos, no quiere que el sistema le sustituya en silencio por otra ni que se le pase a modo remoto solo; quiere saberlo y decidir. Rastreo: `HU04_CU002_A1` cubre este caso: *"no quedarme trabado ni terminar corriendo contra una base equivocada porque el sistema me la sustituyó por su cuenta"*.
- **No volver a correr BLAST solo para probar un umbral nuevo.** Necesita poder aflojar un umbral de identidad del 80% al 60% y agregar cobertura del 70% sin volver a invocar al motor. Rastreo: `HU12_CU006_B` CA-02.

## 2. Escenario de uso

**Historia de usuario de referencia.** El escenario se construye alrededor de **`HU13_CU007_B` · *Descargar los alineamientos actualmente visibles en un formato***, porque el objetivo real del investigador sénior se cierra cuando se lleva el subconjunto filtrado a su siguiente paso de análisis. Los pasos previos materializan las HUs encadenadas: `HU01_CU001_B` (carga), `HU03_CU002_B` (configuración en modo local), `HU05_CU003_B` (validación), `HU08_CU004_B` (ejecución), `HU11_CU005_B` (tabla y persistencia) y `HU12_CU006_B` (filtros post-búsqueda). La narración también atraviesa, de forma coherente con el perfil, el camino alternativo `HU04_CU002_A1` (base local no disponible), que es la clase de situación que este usuario sí se encuentra.

### Narración

Un investigador sénior está trabajando en un proyecto sobre una familia de proteínas de interés. Tiene una secuencia candidata nueva, obtenida de un experimento del grupo, y quiere ver con qué proteínas de la base del laboratorio alinea con razonable identidad y cobertura, para después usar ese subconjunto en un árbol filogenético que arma por fuera del sistema.

Abre LocalBlast desde su escritorio del laboratorio y entra con su usuario del grupo. En la pantalla de nueva búsqueda sube el archivo FASTA de la secuencia candidata, que viene con encabezado y cuerpo bien formados. El sistema le confirma la carga y le indica que infirió alfabeto *"proteína"*.

Pasa a la configuración. Elige **modo local**, selecciona del catálogo la base propia del grupo —*lab_proteins_v3*—, elige programa **blastp** y ajusta un par de parámetros pre-búsqueda a los valores con los que trabaja habitualmente (una matriz distinta a la por defecto y un E-value máximo más restrictivo). Toca **"Validar búsqueda"**: el sistema le da el visto bueno, se habilita **"Ejecutar búsqueda"** y la presiona.

La búsqueda termina en un minuto. La tabla aparece con los alineamientos y el sistema le confirma por un cartel discreto que ya se guardó en el historial. En este momento es donde empieza el trabajo real para él: no le sirve toda la tabla, le sirve el subconjunto relevante. Abre el panel de filtros post-búsqueda y pone *identidad ≥ 80%* y *cobertura ≥ 60%*. La tabla se re-filtra inmediatamente, sin volver a correr BLAST, y queda mostrando los hits que importan.

Mira un rato la tabla filtrada, decide que el umbral de cobertura es muy restrictivo y lo afloja a *≥ 50%*. La tabla se re-filtra otra vez contra el conjunto crudo original (no contra el subconjunto filtrado anterior), aparecen algunos hits adicionales interesantes. Satisfecho con el filtro, elige formato **CSV** y presiona **"Descargar"**. El archivo que recibe contiene los hits visibles —los que superan los filtros vigentes— con las columnas mínimas y una sección de metadatos con los parámetros pre-búsqueda, la base utilizada, el timestamp y los filtros aplicados. Abre el CSV en una planilla y empieza a limpiarlo para el próximo paso.

Vuelve a LocalBlast una semana después, revisa el historial y confirma algo que le importa: la entrada en el historial sigue conteniendo el conjunto crudo completo, no la lista filtrada, así que puede probar un umbral distinto más adelante sin tener que relanzar BLAST+.

### Variante de camino alternativo (realista para este perfil)

En una sesión anterior, al elegir la base local el investigador seleccionó *lab_genomes_v2* para una búsqueda contra genomas del grupo. El sistema le respondió *"La base de datos 'lab_genomes_v2' está siendo actualizada y no puede usarse en este momento"* y le devolvió al paso de selección con la lista refrescada, **sin** proponerle automáticamente cambiar a modo remoto (cumpliendo `HU04_CU002_A1` CA-01). Esto le dejó claro que la base no estaba disponible, no que había desaparecido del sistema; él decidió esperar a que el administrador terminara la actualización y volvió al día siguiente.

## 3. Flujo de navegación

Las pantallas que atraviesa el investigador sénior durante el escenario principal, con las HUs que respaldan cada una. Las HUs son las mismas pantallas base que para el perfil estudiante, pero este perfil **sí ejerce** las pantallas de filtrado y descarga, que el estudiante no visitó en su escenario.

| # | Pantalla | HUs que la respaldan | Qué pasa en esta pantalla |
|---|---|---|---|
| 1 | **Autenticación** | (ninguna HU del TP1 — ver nota) | Ingresa usuario y contraseña del laboratorio. |
| 2 | **Nueva búsqueda** · sección *Secuencia query* | `HU01_CU001_B` | Sube un archivo FASTA con un único registro de proteína. |
| 3 | **Nueva búsqueda** · sección *Configuración + validación* | `HU03_CU002_B`, `HU04_CU002_A1` (variante), `HU05_CU003_B` | Elige modo local, base del laboratorio, programa `blastp`, ajusta parámetros a sus valores habituales y valida la configuración. |
| 4 | **Ejecución en progreso** | `HU08_CU004_B` | Ve el indicador de progreso de la invocación local a BLAST+. |
| 5 | **Resultados** con *filtros post-búsqueda* y *descarga* | `HU11_CU005_B`, `HU12_CU006_B`, `HU13_CU007_B` (y, cuando los filtros dejan la tabla vacía, `HU14_CU007_A1`) | Ve la tabla, aplica y ajusta filtros interactivamente, descarga el subconjunto visible como CSV. Confirmación de persistencia automática en el historial. |

**Nota sobre la pantalla de autenticación.** La misma observación que el perfil estudiante: la autenticación básica está en el alcance ([SRS §1.3](../../requeriments/srs.md#13-dentro-del-alcance)) pero no tiene HU propia en el TP1. El grupo evaluará en 4.1 si se maqueta.

**Nota sobre pantalla #5.** Las HU `HU11_CU005_B`, `HU12_CU006_B` y `HU13_CU007_B` conviven en la misma vista: la HU11 habla de presentar la tabla *"en la misma vista apenas termina la ejecución"*, y las HUs de filtro y descarga operan sobre esa misma tabla (los filtros no re-ejecutan BLAST y la descarga toma lo visible). Por eso se maqueta como una pantalla única con zonas específicas para cada HU, no como tres pantallas separadas. Esto es coherente también con el escenario de calidad de **Operabilidad** del TP2 Parte A, que exige fluidez al refinar resultados sin cambiar de contexto.

## 4. Resumen de HUs cubiertas por este perfil en el escenario

| HU | Rol en el escenario |
|---|---|
| `HU01_CU001_B` | Carga la secuencia desde archivo FASTA de proteína (CA-01). |
| `HU03_CU002_B` | Configuración completa en modo local con base del laboratorio (CA-03) y ajuste manual de parámetros (CA-02). |
| `HU04_CU002_A1` | Variante alternativa: base local en actualización (CA-01). |
| `HU05_CU003_B` | Validación exitosa que habilita *Ejecutar búsqueda* (CA-01). |
| `HU08_CU004_B` | Ejecución asíncrona con indicador de progreso (CA-01, CA-02). |
| `HU11_CU005_B` | Tabla de resultados y persistencia automática en historial (CA-01, CA-02). |
| `HU12_CU006_B` | Aplicación y ajuste sucesivo de filtros post-búsqueda sin re-ejecutar BLAST (CA-01, CA-02); historial no modificado por los filtros (CA-03). |
| `HU13_CU007_B` | Descarga en CSV del subconjunto filtrado con metadatos (CA-02); historial no se altera por la descarga (CA-03). |
