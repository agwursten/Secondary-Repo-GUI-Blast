# Diagrama de Contexto — LocalBlast

Este documento contiene la representación DFD del sistema, siguiendo el instructivo de la cátedra: Nivel 0 (contexto — un único proceso 0 con sus entidades externas) y Nivel 1 (descomposición de ese proceso 0 en sus procesos internos, respetando la regla de balanceo de los flujos externos). Los almacenes aparecen recién en Nivel 1, como corresponde.

**Nota sobre el nombre y el rol del sistema.** El proyecto se llama LocalBlast por razones históricas del grupo, pero es importante no confundirlo con el motor de alineamiento: **BLAST+** (la suite oficial de NCBI) es quien efectivamente ejecuta los alineamientos, tanto contra bases de datos locales como contra NCBI en modo remoto (mediante la opción `-remote`). Nuestro sistema es una **GUI web para BLAST+**: recibe la configuración de una búsqueda o de una base de datos por interfaz web, invoca a BLAST+ con las opciones adecuadas y presenta el resultado. Por eso NCBI **no** aparece como entidad externa del diagrama de contexto: nuestra GUI no habla directamente con NCBI, habla con BLAST+, y es BLAST+ el que — cuando corresponde — se comunica con NCBI del otro lado.

---

## Nivel 0 · Diagrama de contexto

El sistema completo se representa como un único proceso (0), con sus tres entidades externas: los dos actores humanos (Investigador/a y Administrador/a) y el único sistema externo con el que dialoga (**BLAST+**, el motor de alineamiento sobre el que se apoya).

```mermaid
flowchart LR
    INV[Investigador/a]

    P((0<br/>LocalBlast<br/>GUI web para BLAST+))

    ADM[Administrador/a]
    BLAST[BLAST+<br/>motor de alineamiento<br/>local y remoto]

    INV -->|secuencia query, programa,<br/>modo, id base de datos,<br/>parámetros y filtros| P
    P -->|tabla de resultados<br/>y archivo descargable| INV

    ADM -->|FASTA + tipo +<br/>orden alta/actualizar/baja| P
    P -->|catálogo y estado<br/>de bases de datos| ADM

    P -->|invocación de blastn/blastp/<br/>makeblastdb con inputs<br/>y flag -remote si aplica| BLAST
    BLAST -->|resultado del alineamiento<br/>o del índice construido| P
```

**Aclaración sobre el modo local vs remoto.** Ambos modos son, desde el punto de vista de nuestra GUI, **una invocación al motor BLAST+**; la diferencia está enteramente del lado de BLAST+:

- En **modo local**, BLAST+ lee los índices de las bases de datos que residen en el mismo servidor.
- En **modo remoto**, BLAST+ recibe la flag `-remote` y él mismo se comunica con los servidores públicos de NCBI para resolver la búsqueda; nuestro sistema no participa de ese diálogo.

Por eso desde el DFD ambos casos comparten los mismos dos flujos externos hacia BLAST+ (invocación y resultado). El comportamiento distinto de BLAST+ según la flag no cambia el diagrama de contexto de nuestro sistema.

---

## Nivel 1 · Descomposición del proceso 0

El proceso 0 se descompone en **tres procesos internos**, más dos almacenes. La regla de balanceo se respeta: los seis flujos externos que cruzan el límite del sistema son los mismos que en Nivel 0, redistribuidos entre los procesos internos.

```mermaid
flowchart TD
    INV[Investigador/a]
    ADM[Administrador/a]
    BLAST[BLAST+<br/>motor de alineamiento]

    P1((1<br/>Ejecutar búsqueda<br/>BLAST))
    P2((2<br/>Filtrar y entregar<br/>resultados))
    P3((3<br/>Administrar bases<br/>de datos))

    D1[(D1 · Catálogo de<br/>bases de datos)]
    D2[(D2 · Búsquedas y<br/>resultados históricos)]

    %% Flujos externos — Investigador
    INV -->|secuencia query, programa,<br/>modo, id base de datos,<br/>parámetros y filtros| P1
    P2 -->|tabla de resultados<br/>y archivo descargable| INV

    %% Flujos externos — Administrador
    ADM -->|FASTA + tipo +<br/>orden alta/actualizar/baja| P3
    P3 -->|catálogo y estado<br/>de bases de datos| ADM

    %% Flujos externos — BLAST+
    P1 -->|invocación blastn/blastp<br/>con inputs y -remote si aplica| BLAST
    BLAST -->|resultado del alineamiento| P1
    P3 -->|invocación makeblastdb<br/>con FASTA y tipo| BLAST
    BLAST -->|confirmación del<br/>índice construido| P3

    %% Flujos internos entre procesos
    P1 -->|resultados crudos<br/>+ criterios post-búsqueda| P2

    %% Flujos con almacenes
    P3 -->|escribe entrada del catálogo| D1
    D1 -->|lista de bases de datos<br/>disponibles con ubicación| P1
    D1 -->|catálogo para el admin| P3

    P2 -->|guarda búsqueda + resultados| D2
    D2 -.->|historial consultable<br/>uso futuro| P2
```

**Chequeo de balanceo:** los seis flujos externos aparecen en Nivel 1 con los mismos extremos externos que en Nivel 0. Los que van hacia BLAST+ se dividen entre P1 (para búsqueda) y P3 (para construir índices), pero desde afuera del sistema siguen siendo los dos mismos flujos.

---

## Descripción de los procesos y almacenes

### Procesos

- **P1 · Ejecutar búsqueda BLAST.** Recibe del investigador el archivo FASTA con la secuencia query, la elección del programa BLAST (`blastn`, `blastp`, `blastx`, `tblastn`, `tblastx`), el modo (local o remoto), la base de datos elegida y los parámetros pre-búsqueda que afectan al algoritmo (E-value, matriz de sustitución, tamaño de palabra, penalizaciones de gap, etc.). Verifica la compatibilidad entre el programa BLAST elegido, el tipo de la secuencia query y el tipo de la base de datos, valida el resto de la entrada e **invoca a BLAST+** con la combinación correcta de opciones — incluida la flag `-remote` cuando el modo es remoto. Recibe de vuelta el conjunto crudo de alineamientos.

- **P2 · Filtrar y entregar resultados.** Recibe los resultados crudos y los criterios de filtrado post-búsqueda que el usuario definió (por ejemplo umbrales de % identidad, cobertura, E-value, taxones), aplica esos filtros, arma la vista de resultados que se muestra en la interfaz y prepara el archivo descargable en el formato pedido (CSV, JSON, FASTA, tabular BLAST, XML). Al cerrar la búsqueda, escribe una copia del resultado en el historial D2.

- **P3 · Administrar bases de datos.** Es el proceso del rol Administrador. Recibe el archivo FASTA subido por el admin y el tipo declarado (nucleótidos o proteínas), junto con las órdenes de alta, actualización o baja de una base de datos local. **Invoca a BLAST+** con `makeblastdb` para construir los índices, y mantiene actualizado en D1 el catálogo de bases de datos disponibles (nombre visible, tipo, ubicación del índice, fecha) que P1 va a ofrecer al investigador. Devuelve al administrador el estado del proceso (base de datos creada, actualizada, con errores, etc.).

### Almacenes

- **D1 · Catálogo de bases de datos.** Contiene los **metadatos** de cada base de datos local disponible: nombre visible, tipo (nucleótidos / proteínas), ruta al conjunto de archivos de índice que produjo `makeblastdb`, fecha de alta, tamaño. Los archivos físicos de índice (`.nhr`, `.nin`, `.nsq`, etc.) los escribe y los lee **BLAST+**; nuestro sistema los registra en D1 pero no los interpreta.

- **D2 · Búsquedas y resultados históricos.** Guarda la traza de cada búsqueda ejecutada (parámetros, base de datos usada, timestamp) junto con su resultado, para que el usuario pueda volver a consultar o descargar sin repetir la ejecución. En esta primera versión del sistema solo se **escribe** en D2 (flujo lleno); la lectura (flujo punteado) queda documentada como uso futuro — no está en el alcance profundizado del cuatrimestre.

---

## Nota sobre el alcance profundizado

De los tres procesos identificados, el grupo lleva a profundidad **P1 (Ejecutar búsqueda BLAST)** y **P3 (Administrar bases de datos)** — ver la justificación en la sección "Selección de procesos a profundizar" del [SRS](../requirements/srs.md#5-selección-de-procesos-a-profundizar).
