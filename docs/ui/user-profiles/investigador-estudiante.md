# Perfil de usuario — Investigador/a (Estudiante de grado o posgrado)

> Perfil del actor **Investigador/a** del TP1, en el subgrupo de stakeholders *"Estudiantes de Grado y Posgrado"* identificado en [SRS §2.1](../../requeriments/srs.md#21-stakeholders). Comparte el actor con el perfil [`investigador-senior.md`](investigador-senior.md); por lo tanto, comparte capacidades habilitadas en el sistema (todas las HU01 a HU14 están disponibles para los dos perfiles), pero se diferencia en el objetivo primario con el que entra al sistema, en el nivel de conocimiento técnico y en el tipo de frustraciones que condicionan su uso.

## 1. Perfil de usuario

### Quién es

Estudiante de grado o posgrado que cursa materias con componente de biología molecular, bioinformática o genética, o que está trabajando en una tesis / trabajo final que incluye alguna identificación o comparación de secuencias. Está familiarizado con qué es BLAST a nivel conceptual —sabe que sirve para buscar secuencias similares en una base de datos— pero no necesariamente con el detalle de los parámetros del algoritmo.

Rastreo: SRS §2.1 lo caracteriza como *"Estudiantes de Grado y Posgrado"* y el TP1 no afirma más que esto sobre el estudiante como persona. Cualquier atributo demográfico más fino (edad, carrera específica, años cursados) no se incluye porque el TP1 no lo respalda.

### Objetivo que persigue con el sistema

Correr un alineamiento BLAST sobre una secuencia que le dieron o que obtuvo en el laboratorio, y ver un resultado útil **sin tener que pelearse con la línea de comandos de BLAST+ ni con la configuración del entorno**. El valor que busca es llegar al resultado y, en el mejor caso, descargarlo para pegarlo en un informe.

Rastreo: SRS §2.1 — *"necesitan realizar alineamientos locales rápidos para trabajos prácticos o investigación sin perder tiempo en la configuración de entornos por terminal"*. SRS §1.1 refuerza la barrera de entrada de la CLI (*"recordar la sintaxis de los binarios …, armar comandos con muchos parámetros, gestionar la ubicación de las bases de datos y parsear la salida a mano"*).

### Contexto de uso

- **Lugar.** Un aula / sala de cómputos de la facultad, su propia casa durante el estudio, o eventualmente el laboratorio del grupo. En cualquiera de los tres casos, con conexión a internet. **Supuesto del grupo:** la ubicación concreta no está en el TP1, se infiere de "cursada" y "laboratorio" en SRS §2.1.
- **Dispositivo.** Laptop o PC de escritorio con un navegador moderno. **Supuesto del grupo:** el TP1 no fija dispositivo; se infiere de SRS §1.3 que incluye *"Interfaz web para el rol Investigador"* en el alcance. El sistema no está pensado para uso cómodo en celular.
- **Urgencia.** Media. Trabaja contra una fecha de entrega del TP o del informe, por lo que la rapidez es parte del valor, pero no es un escenario de emergencia. Rastreo: SRS §2.1 habla de *"alineamientos locales rápidos"* como necesidad explícita.
- **Frecuencia de uso.** Baja y por rachas: puede usarlo mucho durante dos semanas antes de una entrega y después no abrirlo por meses. **Supuesto del grupo:** no está en el TP1 pero es coherente con el perfil "cursada".

### Nivel de conocimiento técnico

- **Dominio (biología molecular / bioinformática).** Básico a intermedio. Entiende qué es una secuencia FASTA, qué significa "ADN" vs. "proteína" y la idea general de un alineamiento, pero puede dudar frente a decisiones como "¿uso `blastn` o `blastx` con esta query?" o "¿qué E-value máximo pongo?". Rastreo parcial: SRS §1.1 describe la barrera de la CLI *"para usuarios sin perfil puramente bioinformático o técnico"*, implícitamente ubicándolo en ese segmento.
- **Herramientas.** Maneja un navegador y archivos de su computadora con soltura, pero **no** tiene necesariamente familiaridad con la terminal, ni con instalar BLAST+ en local, ni con escribir scripts para parsear la salida. Rastreo: SRS §1.1, misma cita.
- **Lectura de documentación técnica.** Puede leerla si no le queda otra, pero prefiere evitarla; la documentación de BLAST+ es extensa y escrita para un público técnico. Rastreo: README §1 — *"navegar por documentación extensa, lo que ralentiza el trabajo de usuarios sin perfil puramente bioinformático o técnico"*.

### Limitaciones y frustraciones que condicionan su uso

- **Fricción con la CLI.** La alternativa "terminal + BLAST+" lo frena antes de empezar: tiene que recordar la sintaxis de los binarios y los nombres de las flags, gestionar paths y parsear la salida a mano. Rastreo: SRS §1.1.
- **La web oficial de NCBI es demasiado para la tarea.** Para una consulta rápida le resulta sobrecargada y no le ofrece el filtrado interactivo que necesitaría. Rastreo: README §1 — *"carece de opciones avanzadas de filtrado directo e interactivo … y resulta sobrecargada para consultas simples y rápidas"*.
- **Riesgo de equivocarse en los parámetros.** Al no tener la intuición fina del algoritmo, puede elegir un programa BLAST incompatible con su query (por ejemplo `blastp` sobre una secuencia de ADN) o poner un parámetro fuera de rango sin darse cuenta. Rastreo: existen las HU `HU06_CU003_E1` (parámetros fuera de rango) y `HU07_CU003_E2` (combinación incompatible) precisamente para cubrir esta clase de errores.
- **Riesgo de cargar mal la secuencia.** Puede pegar texto con un carácter extraño, o un FASTA con encabezado y sin cuerpo, y necesita un mensaje claro para corregirlo. Rastreo: `HU02_CU001_E1`.

## 2. Escenario de uso

**Historia de usuario de referencia.** El escenario se construye alrededor de **`HU11_CU005_B` · *Presentar la tabla de alineamientos y guardar la búsqueda en el historial***, porque el objetivo del estudiante termina de cumplirse cuando ve los resultados en pantalla. Los pasos previos que la narración incluye materializan las HUs encadenadas que llevan hasta allí: `HU01_CU001_B` (cargar la secuencia), `HU03_CU002_B` (configurar modo/base/programa/parámetros), `HU05_CU003_B` (validar la configuración), `HU08_CU004_B` (ejecutar). La narración también atraviesa de manera realista un slice de excepción —`HU02_CU001_E1`— porque el perfil es propenso a este tipo de error.

### Narración

Es jueves a la tarde. Un estudiante tiene que entregar un informe de trabajo práctico el lunes y necesita identificar a qué organismo pertenece una secuencia de nucleótidos que le entregó la cátedra. Se mete a LocalBlast desde su laptop en la biblioteca de la facultad y se autentica con el usuario que le dieron al principio del cuatrimestre.

Entra directamente a la pantalla de nueva búsqueda, con el formulario vacío y en la primera sección —**Secuencia query**— pega la secuencia tal como se la pasaron, sin encabezado FASTA, directamente el texto. El sistema le confirma que la secuencia quedó cargada y le indica que infirió alfabeto *"ADN"*. Siente alivio: no tuvo que armar un archivo FASTA ni abrir un editor.

Baja a la sección **Configuración**. Elige *modo remoto* (porque la cátedra no le dio una base local y lo que quiere es buscar contra la nt de NCBI), selecciona la base de datos *nt*, el programa *blastn*, y deja los parámetros pre-búsqueda como están, por defecto. Confía en los defaults porque no quiere ponerse a leer documentación un jueves a la tarde.

Toca **"Validar búsqueda"**. El sistema responde con el visto bueno —*"configuración válida y lista para ejecutar"*— y se habilita el botón **"Ejecutar búsqueda"**. Lo presiona. La interfaz muestra un indicador de progreso. El estudiante aprovecha para abrir el campus virtual en otra pestaña del navegador y revisar la consigna del TP.

Dos minutos después vuelve a la pestaña de LocalBlast: la búsqueda terminó. Ve una tabla con los alineamientos, con las columnas que necesita para identificar el hit más razonable: identificador, score, E-value observado, % de identidad, % de cobertura. El primer hit es claramente de una especie reconocible, con una identidad del 99% y cobertura casi total. Lo copia y se vuelca al informe.

No llega a usar los filtros post-búsqueda ni descargar nada en esa sesión —la respuesta era tan clara que no hizo falta—. Igual, el sistema le confirma por un cartel que la búsqueda quedó guardada automáticamente en su historial. Esto lo tranquiliza: si el lunes al revisar el informe quiere volver a ver el resultado, va a seguir estando ahí.

### Variante de excepción (realista para este perfil)

En una sesión anterior, el estudiante había pegado por accidente una secuencia que incluía un número de posición al principio (p. ej. `1 ATGCGTAC...`). Al confirmar la carga, el sistema le respondió *"carácter inválido '1' en la posición 1"* y no habilitó la configuración (cumpliendo `HU02_CU001_E1`). Borró el número, volvió a pegar la secuencia limpia y pudo continuar. El mensaje claro —en lugar de un error genérico— es lo que le permitió corregir sin pedirle ayuda a nadie.

## 3. Flujo de navegación

Las pantallas que atraviesa el estudiante durante el escenario principal son las siguientes. Cada pantalla indica qué HUs del TP1 la respaldan; **si una pantalla no está respaldada por alguna HU, no se maqueta** (consigna 4.1).

| # | Pantalla | HUs que la respaldan | Qué pasa en esta pantalla |
|---|---|---|---|
| 1 | **Autenticación** | (ninguna HU del TP1 — ver nota) | El estudiante ingresa usuario y contraseña. |
| 2 | **Nueva búsqueda** · sección *Secuencia query* | `HU01_CU001_B`, `HU02_CU001_E1` | Pega la secuencia o sube un archivo FASTA. El sistema infiere el alfabeto y la deja disponible, o rechaza con mensaje claro. |
| 3 | **Nueva búsqueda** · sección *Configuración + validación* | `HU03_CU002_B`, `HU05_CU003_B` (y en escenarios de excepción `HU06_CU003_E1`, `HU07_CU003_E2`) | Elige modo (remoto), base (`nt`), programa (`blastn`), deja parámetros por defecto. Presiona *"Validar búsqueda"* y recibe el OK semántico. |
| 4 | **Ejecución en progreso** | `HU08_CU004_B` (y `HU09_CU004_A1` si cancela, `HU10_CU004_E1` si falla el modo remoto) | Ve el indicador de progreso de BLAST+. Puede navegar a otra pestaña del navegador sin interrumpir. |
| 5 | **Resultados** | `HU11_CU005_B` | Ve la tabla de alineamientos con las columnas mínimas. Confirmación de que la búsqueda quedó persistida en el historial. |

**Nota sobre la pantalla de autenticación.** La autenticación básica está dentro del alcance del TP1 ([SRS §1.3](../../requeriments/srs.md#13-dentro-del-alcance)) pero no se profundizó como HU propia en el TP1 (ningún `HU0X_CU00Y_*` cubre el login). El grupo evaluará en 4.1 si corresponde maquetarla en este TP; en caso contrario, el flujo se maqueta a partir de la pantalla #2 asumiendo sesión ya iniciada.

**Pantallas no incluidas en este flujo.** Las pantallas de *filtros post-búsqueda* (`HU12_CU006_B`) y de *descarga* (`HU13_CU007_B`, `HU14_CU007_A1`) existen en el sistema y están respaldadas por HUs, pero este perfil no las ejerce en el escenario de referencia porque su objetivo —identificar la secuencia— ya quedó cumplido en la pantalla #5. Esas pantallas sí se usan en el escenario del perfil [investigador sénior](investigador-senior.md).

## 4. Resumen de HUs cubiertas por este perfil en el escenario

| HU | Rol en el escenario |
|---|---|
| `HU01_CU001_B` | Carga la secuencia como texto plano (CA-02). |
| `HU02_CU001_E1` | Variante de excepción: rechazo de secuencia con carácter inválido (CA-01). |
| `HU03_CU002_B` | Configuración completa en modo remoto con defaults (CA-01, CA-02). |
| `HU05_CU003_B` | Validación exitosa que habilita *Ejecutar búsqueda* (CA-01). |
| `HU08_CU004_B` | Ejecución asíncrona con indicador de progreso (CA-01, CA-02). |
| `HU11_CU005_B` | Tabla de resultados y persistencia automática en historial (CA-01, CA-02). |
