# Diseño detallado — LocalBlast

**HU08_CU004_B · Ejecutar la búsqueda validada y ver sus resultados**

Este documento baja la arquitectura de LocalBlast ([`architecture.md`](../architecture/architecture.md)) al nivel de clases para una historia de usuario. Parte de la HU y de sus criterios de aceptación, la analiza en sus tres dimensiones (funcionalidad, estructura y calidad) y deriva, en ese orden, el diagrama de robustez, los diagramas de secuencia y el modelo de clases. Cada diagrama sale del anterior: lo que no figura en la robustez no se invoca en las secuencias, y lo que no figura en las secuencias no aparece en el modelo de clases.

---

## Índice

1. [Introducción](#1-introducción)
2. [Relación con la arquitectura](#2-relación-con-la-arquitectura)
3. [Diseño de la HU](#3-diseño-de-la-hu)
---

## 1. Introducción

### 1.1 Propósito

Definir qué clases, operaciones y colaboraciones implementan la ejecución de una búsqueda BLAST en LocalBlast, desde que el investigador presiona **Ejecutar búsqueda** hasta que ve la tabla de alineamientos y la búsqueda queda guardada en el historial. El documento es la guía para implementar y probar esa funcionalidad.

### 1.2 Historia de usuario elegida

**`HU08_CU004_B` · Ejecutar la búsqueda validada y ver sus resultados**: el camino feliz (pasos 1 a 4) del caso de uso `CU004`. Realiza RF-08, RF-09 y RF-10.

**Qué queda afuera de este diseño:**

- La **cancelación** (`HU09_CU004_A1`) y el **fallo del modo remoto** con su mensaje diferenciado (`HU10_CU004_E1`), que tienen sus propias historias.
- La **identificación del investigador** (autenticación y sesión). No tiene historia de usuario propia y no forma parte de lo que esta HU pide.
- La **validación** de la búsqueda. Es la precondición de la HU (la deja hecha `HU05_CU003_B`), así que aquí la búsqueda llega ya validada.

### 1.3 Motivo de la elección

La HU cumple las tres condiciones para sostener un diseño en tres dimensiones:

| Condición | Evidencia en la arquitectura |
|---|---|
| Está asociada a un escenario de calidad | `EC-01` (concurrencia de invocaciones) y `EC-02` (cambio menor de versión de BLAST+) llegan al componente **Adaptador BLAST+**, que la HU atraviesa (tabla 11.1 de la arquitectura) |
| Atraviesa la estructura | Su recorrido (tabla 11.2) pasa por la Aplicación Web, por las tres capas del Backend y por el sistema externo BLAST+ |
| Hay decisiones de arquitectura que la afectan | `DA-03` (Adaptador BLAST+ dedicado) y `DA-04` (un subproceso por búsqueda) citan al Adaptador; `DA-02` (capas) rige todo el recorrido por el Backend |

Más allá de esas condiciones, es **la historia que justifica la existencia del producto**. LocalBlast es una interfaz para BLAST+, y esta es la única HU en la que BLAST+ se invoca de verdad. Las historias anteriores preparan la búsqueda y las posteriores trabajan sobre resultados que ya existen. Es también la que verifica el driver de la arquitectura (interoperabilidad) y la que tiene más riesgo técnico: ejecutar sin bloquear la interfaz, atender varias búsquedas a la vez sin mezclar resultados e interpretar una salida que no controlamos.

### 1.4 Siglas

| Sigla | Significado |
|---|---|
| C4 | Modelo de documentación de arquitectura en cuatro niveles: contexto, contenedores, componentes y código |
| CA | Criterio de aceptación de una historia de usuario |
| CLI | Interfaz de línea de comandos (*command-line interface*) |
| CU | Caso de uso |
| D2 | Almacén del DFD con las búsquedas ejecutadas y sus resultados crudos (historial) |
| DA | Decisión de arquitectura |
| DFD | Diagrama de flujo de datos |
| EC | Escenario de calidad |
| GRASP | Patrones generales para asignar responsabilidades (*General Responsibility Assignment Software Patterns*) |
| HTTP / HTTPS | Protocolo de la web / HTTP sobre una conexión cifrada |
| HU | Historia de usuario |
| MVC | Modelo-Vista-Controlador |
| NCBI | *National Center for Biotechnology Information*, proveedor del BLAST remoto |
| RF | Requerimiento funcional |
| SQL | Lenguaje para consultar y modificar bases de datos relacionales |
| XML | Formato de datos con etiquetas; es la salida de BLAST+ que usa este diseño (`-outfmt 5`) |

---

## 2. Relación con la arquitectura

### 2.1 Tabla de coherencia

| Dimensión | Contenido |
|---|---|
| **Funcionalidad** | `HU08_CU004_B`, slice básico `CU004_B` del caso de uso `CU004 · Ejecutar la búsqueda y ver sus resultados` (pasos 1 a 4). Caminos: el principal (ejecutar, guardar en el historial y mostrar la tabla) y uno de error (BLAST+ no termina bien: no se muestra tabla ni se guarda nada, como exige la garantía mínima de `CU004`). |
| **Estructura** | Contenedor **Aplicación Web** (patrón MVC, `DA-07`): Pantallas, Controlador de búsqueda, Modelo de búsqueda, Modelo de resultados y Cliente del Backend. Contenedor **Backend** (patrón Capas, `DA-02`): **Controladores** (presentación), **Ejecución y persistencia** (dominio), **Acceso a datos** y **Adaptador BLAST+** (datos). Sistema externo **BLAST+**. Estilo base cliente-servidor (`DA-01`). **Componente principal: Ejecución y persistencia.** |
| **Calidad** | `EC-01` · hasta cinco búsquedas concurrentes sin cruce de resultados. Tácticas: *introducir concurrencia* y *encapsular*. Decisión: `DA-04` (un subproceso de BLAST+ por búsqueda). `EC-02` · cambio menor de versión de BLAST+ sin romper la lectura de la salida. Tácticas: *adaptar la interfaz* y *encapsular*. Decisión: `DA-03` (Adaptador BLAST+ dedicado en la capa de datos). |
| **Dominio** | Entidades del modelo de dominio que intervienen: `Busqueda` y `Alineamiento` como clases; `SecuenciaQuery`, `ProgramaBlast`, `ParametrosPreBusqueda`, `ModoEjecucion` y `BaseDeDatos` como datos de la búsqueda. No intervienen `Usuario`, `Investigador`, `Administrador`, `FiltroPostBusqueda`, `Reporte` ni `FormatoDescarga` (ver [3.2](#32-entidades-del-modelo-de-dominio-que-intervienen)). |
| **Verificación** | `EC-01`: se verificará con una prueba de cinco búsquedas lanzadas a la vez sobre un adaptador simulado con demoras distintas; cada una recibe exactamente sus propios alineamientos (cero cruces). `EC-02`: se verificará con una prueba de la lectura de una salida XML con campos desconocidos; los campos obligatorios llegan intactos y queda registrada una advertencia. Las pruebas concretas se diseñan en la etapa de pruebas, una vez aprobado este diseño. |

### 2.2 Recorrido de la HU sobre los componentes

```mermaid
flowchart LR
    subgraph web["Aplicación Web · MVC"]
        pan["Pantallas"]
        cb["Controlador<br/>de búsqueda"]
        mod["Modelos de búsqueda<br/>y de resultados"]
        cli["Cliente del<br/>Backend"]
    end
    subgraph be["Backend · Capas"]
        subgraph pres["Presentación"]
            ctrl["Controladores"]
        end
        subgraph dom["Dominio"]
            eje["Ejecución y<br/>persistencia ★"]
        end
        subgraph dat["Datos"]
            acc["Acceso a datos"]
            ada["Adaptador BLAST+"]
        end
    end
    blast["BLAST+<br/>(sistema externo)"]

    pan --> cb --> cli
    cb --> mod
    cli -->|JSON / HTTPS| ctrl
    ctrl --> eje
    eje --> ada
    eje --> acc
    ada -->|CLI / subproceso| blast
```

★ componente principal de la HU.

La verificación completa de coherencia con la arquitectura está en la [sección 8.2](#82-verificación-de-coherencia), porque necesita los diagramas de las secciones 3 y 4.

---

## 3. Diseño de la HU

### 3.1 Enunciado y criterios de aceptación

> **Como** investigador/a,
> **quiero** que el sistema invoque a BLAST+ en segundo plano sobre mi búsqueda validada, con indicador de progreso y opción de cancelar, y que al terminar me muestre los alineamientos en una tabla y guarde automáticamente la búsqueda en el historial,
> **para** poder seguir trabajando en la aplicación mientras la búsqueda corre, ver los resultados apenas estén listos y no perder la búsqueda aunque no llegue a refinarla ni descargarla en esta sesión.

- **CA-01. Ejecución asíncrona con indicador de progreso.** **Given** una búsqueda ya configurada y validada (postcondición de `CU003`), **When** el investigador presiona "Ejecutar búsqueda" y el sistema invoca a BLAST+ en segundo plano, **Then** la interfaz muestra un indicador de progreso visible y permanece navegable: el investigador puede desplazarse dentro de la aplicación sin que la ejecución se interrumpa.
- **CA-02. Presentación de la tabla al finalizar.** **Given** una búsqueda en ejecución que BLAST+ termina exitosamente, **When** el sistema recibe el conjunto crudo de alineamientos, **Then** presenta los resultados en una tabla con al menos las columnas: identificador del hit, score, E-value observado, porcentaje de identidad y porcentaje de cobertura.
- **CA-03. Persistencia automática en el historial.** **Given** una búsqueda que BLAST+ terminó exitosamente, **When** el sistema recibe su conjunto crudo de alineamientos, **Then** registra en el historial (D2), antes de presentar la tabla, una entrada con los parámetros pre-búsqueda, la base de datos usada, el timestamp y el conjunto **completo** de resultados crudos que devolvió BLAST+ (antes de cualquier filtro post-búsqueda), sin que el investigador tenga que ejercer `CU005` ni `CU006` para que la persistencia ocurra.

> **Precisión de CA-03.** La redacción original registraba la búsqueda "cuando el sistema termina de mostrar" la tabla. Eso chocaba con la garantía mínima de `CU004` ("si la tabla se muestra, la entrada en D2 también queda escrita"): si se muestra primero y se guarda después, una falla entre los dos pasos deja una tabla visible sin entrada en el historial. Se invirtió el orden (primero se guarda, después se muestra) en [`historias-usuario.md`](../requeriments/historias-usuario.md) y en el flujo de `CU004` de [`casos-de-uso.md`](../requeriments/casos-de-uso.md).

**La búsqueda no se guarda antes de ejecutarse.** La secuencia y la configuración validadas las conserva la Aplicación Web (en su Modelo de búsqueda) y viajan completas en la solicitud de ejecución. La única escritura en la base es la del historial, cuando BLAST+ ya terminó (RF-10).

### 3.2 Entidades del modelo de dominio que intervienen

Se marcaron los sustantivos del enunciado y de los criterios ("búsqueda validada", "BLAST+", "alineamientos", "tabla", "historial", "parámetros pre-búsqueda", "base de datos usada", "timestamp", "resultados crudos", "identificador del hit", "score", "E-value", "porcentaje de identidad", "porcentaje de cobertura") y se buscaron en el [modelo de dominio](../requeriments/modelo-dominio.md). En verde, las entidades que intervienen:

```mermaid
classDiagram
    class Usuario
    class Investigador
    class Administrador
    class Busqueda
    class SecuenciaQuery
    class ProgramaBlast
    class ParametrosPreBusqueda
    class ModoEjecucion
    class BaseDeDatos
    class Alineamiento
    class FiltroPostBusqueda
    class Reporte
    class FormatoDescarga
    Usuario <|-- Investigador
    Usuario <|-- Administrador
    Investigador "1" --> "*" SecuenciaQuery : carga
    Investigador "1" --> "*" Busqueda : lanza
    Busqueda "*" --> "1" SecuenciaQuery : usa
    Busqueda "*" --> "1" ProgramaBlast : se ejecuta con
    Busqueda "1" *-- "1" ParametrosPreBusqueda : configurada con
    Busqueda "*" --> "1" ModoEjecucion : se ejecuta en
    Busqueda "*" --> "1" BaseDeDatos : consulta
    Busqueda "1" *-- "*" Alineamiento : produce
    Busqueda "1" --> "*" FiltroPostBusqueda : refinada por
    Busqueda "1" --> "*" Reporte : origina
    ProgramaBlast "1" --> "*" ParametrosPreBusqueda : propone valores por defecto
    BaseDeDatos "*" --> "1" ModoEjecucion : disponible en
    Reporte "*" --> "*" Alineamiento : incluye los visibles
    Reporte "*" --> "*" FiltroPostBusqueda : registra los aplicados
    Reporte "*" --> "1" FormatoDescarga : exportado en
    Administrador "1" --> "*" BaseDeDatos : administra
    style Busqueda fill:#dcfce7,stroke:#15803d
    style SecuenciaQuery fill:#dcfce7,stroke:#15803d
    style ProgramaBlast fill:#dcfce7,stroke:#15803d
    style ParametrosPreBusqueda fill:#dcfce7,stroke:#15803d
    style ModoEjecucion fill:#dcfce7,stroke:#15803d
    style BaseDeDatos fill:#dcfce7,stroke:#15803d
    style Alineamiento fill:#dcfce7,stroke:#15803d
```

| Entidad del modelo | ¿Interviene? | Qué usa la HU de ella | La HU la... |
|---|---|---|---|
| `Busqueda` | Sí, como clase | Su configuración, para invocar a BLAST+; los alineamientos que produce; el momento en que se ejecutó | Crea (a partir de la configuración validada) |
| `Alineamiento` | Sí, como clase | Identificador del hit, score, E-value, % identidad y % cobertura: las cinco columnas de la tabla | Crea |
| `SecuenciaQuery` | Sí, como dato de `Busqueda` | El texto FASTA que recibe BLAST+ y su longitud (para la cobertura) | Consulta |
| `ProgramaBlast` | Sí, como dato de `Busqueda` | Qué binario se invoca (`blastn`, `blastp`, …) | Consulta |
| `ParametrosPreBusqueda` | Sí, como dato de `Busqueda` | E-value máximo, tamaño de palabra, matriz y penalizaciones de gap | Consulta |
| `ModoEjecucion` | Sí, como dato de `Busqueda` | Si la invocación lleva la flag `-remote` | Consulta |
| `BaseDeDatos` | Sí, como dato de `Busqueda` | Su ubicación (ruta del índice local o nombre de la base de NCBI) | Consulta |
| `Usuario`, `Investigador` | No | La identificación del investigador queda afuera de esta HU (1.2) | — |
| `Administrador` | No | Fuera del alcance; el catálogo de bases ya está cargado | — |
| `FiltroPostBusqueda` | No | CA-03 exige guardar el conjunto **crudo**; filtrar es `HU11_CU005_B` | — |
| `Reporte`, `FormatoDescarga` | No | Descargar es `HU12_CU006_B` | — |

**Por qué cinco entidades intervienen solo como datos.** `SecuenciaQuery`, `ProgramaBlast`, `ParametrosPreBusqueda`, `ModoEjecucion` y `BaseDeDatos` tienen reglas propias (alfabeto, rangos, compatibilidad entre programa, query y base), pero esas reglas pertenecen a las HU de carga, configuración y validación (`HU01` a `HU07`). Esta HU solo lee sus valores para pasárselos a BLAST+ y guardarlos en el historial. Alcanza con que `Busqueda` los exponga como atributos; convertirlas en clases acá agregaría clases sin comportamiento.

**Cambios al modelo de dominio.** Al armar esta tabla se detectó que el modelo no tenía el concepto **ProgramaBlast** y que tenía multiplicidades que contradecían a `CU001` (una misma secuencia se usa en varias búsquedas). El modelo se corrigió; los cambios están en el *Registro de cambios* de [`modelo-dominio.md`](../requeriments/modelo-dominio.md#registro-de-cambios).

### 3.3 Análisis tridimensional

| Elemento | Funcionalidad (qué hace) | Estructura (con qué se hace) | Calidad (qué propiedad cumple) |
|---|---|---|---|
| **CA-01** | Lanzar la búsqueda sin bloquear la interfaz y mostrar un indicador de progreso hasta que llegue la respuesta | `PantallaBusqueda` (delega y muestra); `ControladorBusqueda` (marca la búsqueda en ejecución en `ModeloBusqueda` y pide la ejecución a `ClienteBackend` de forma asíncrona); `ControladorEjecucion` | La interfaz sigue navegable mientras BLAST+ corre, porque nadie en el cliente se queda bloqueado esperando la respuesta |
| **CA-02** | Al terminar BLAST+, mostrar la tabla con hit, score, E-value, % identidad y % cobertura | `AdaptadorBlast` (invoca y lee la salida); `Busqueda` y `Alineamiento`, que calcula sus porcentajes; en el cliente, `ControladorBusqueda` carga las filas en `ModeloResultados` y `PantallaBusqueda` las dibuja | `EC-02`: si la salida trae campos nuevos, la tabla igual sale con los campos obligatorios intactos |
| **CA-03** | Guardar en el historial la búsqueda con parámetros, base, timestamp y todos los alineamientos crudos | `RepositorioHistorial` | Nunca se muestra una tabla sin su entrada en el historial: primero se guarda y después se devuelve la tabla |
| **`EC-01`** · Concurrencia | Hasta cinco investigadores ejecutan a la vez | Cada solicitud se atiende en su propio hilo del servidor; `AdaptadorBlast` lanza un subproceso propio por búsqueda | **Cero cruces de resultados**: los resultados vuelven por la misma llamada que los pidió, sin estado compartido entre búsquedas |
| **`EC-02`** · Cambio de versión de BLAST+ | BLAST+ devuelve campos que el sistema no conoce | `AdaptadorBlast`, que es el único que conoce el formato de la salida | El 100 % de las salidas "casi conocidas" conserva los campos obligatorios y deja una advertencia en el log |

Los escenarios de **tolerancia a fallos** (rate limit y timeout de NCBI) describen el error del modo remoto, que es `HU10_CU004_E1`. Los de **confidencialidad** dependen de la identificación del investigador, que queda afuera de esta HU. Los de **operabilidad** alcanzan a la configuración (`HU05`) y al filtrado (`HU11`).

### 3.4 Diagrama de robustez

Leyenda: borde punteado = actor o sistema externo; cilindro gris = almacén de datos; rectángulo redondeado azul = *boundary*; círculo naranja = *controller*; rectángulo con barras verde = *entity*; flecha punteada = observación de solo lectura de la Vista sobre los Modelos (MVC). Los recuadros grises agrupan los elementos de cada contenedor.

```mermaid
%%{init: {"flowchart": {"nodeSpacing": 70, "rankSpacing": 60}}}%%
flowchart LR
    inv["Investigador/a<br/>(actor)"]

    subgraph web["Aplicación Web (MVC)"]
        ui(["«boundary»<br/>PantallaBusqueda"])
        cb(("«controller»<br/>ControladorBusqueda"))
        mb[["«entity»<br/>ModeloBusqueda"]]
        mr[["«entity»<br/>ModeloResultados"]]
        cl(("«controller»<br/>ClienteBackend"))
    end

    subgraph be["Backend (Capas)"]
        ce(("«controller»<br/>ControladorEjecucion"))
        ab(["«boundary»<br/>AdaptadorBlast"])
        rh(("«controller»<br/>«interface»<br/>RepositorioHistorial"))
        subgraph agg["agregado Busqueda"]
            bu[["«entity»<br/>Busqueda"]]
            al[["«entity»<br/>Alineamiento"]]
        end
    end
    db[("Base de datos<br/>historial D2")]
    blast["BLAST+<br/>(sistema externo)"]

    inv --> ui
    ui --> cb
    cb --> mb
    cb --> mr
    cb --> cl
    cl -->|JSON / HTTPS| ce
    ce --> bu
    ce --> ab
    ab ----> blast
    ce --> rh
    rh -->|guarda| bu
    rh ----> db
    ui -.->|observa| mb
    ui -.->|observa| mr

    classDef actor fill:#f3f4f6,stroke:#4b5563,color:#111827,stroke-dasharray: 4 3
    classDef boundary fill:#dbeafe,stroke:#1d4ed8,color:#0f172a
    classDef controller fill:#ffedd5,stroke:#c2410c,color:#0f172a
    classDef entity fill:#dcfce7,stroke:#15803d,color:#0f172a
    classDef store fill:#e5e7eb,stroke:#374151,color:#111827
    class inv,blast actor
    class ui,ab boundary
    class cb,cl,ce,rh controller
    class mb,mr,bu,al entity
    class db store
    style web fill:#f9fafb,stroke:#9ca3af
    style be fill:#f9fafb,stroke:#9ca3af
    style agg fill:#ffffff,stroke:#15803d,stroke-dasharray: 5 5
```

**Cómo se clasificó cada elemento.**

- **Fronteras.** Hay dos, porque el sistema habla con dos cosas que no son él: el investigador, a través de `PantallaBusqueda`, y BLAST+, a través de `AdaptadorBlast`.
- **Controladores de la Aplicación Web.** `ControladorBusqueda` interpreta la acción del investigador y actualiza los Modelos (rol Controlador del MVC). `ClienteBackend` es el único que sabe hablar con el Backend por HTTP. La comunicación entre la Aplicación Web y el Backend **no** es una frontera: los dos contenedores son parte de LocalBlast, así que es una coordinación entre controladores.
- **Controladores del Backend.** `ControladorEjecucion` coordina la ejecución y `RepositorioHistorial` es la **interfaz con la base de datos**: define qué se puede hacer con el historial (`guardar`) pero no cómo ni dónde. Detrás tiene implementaciones intercambiables (ver el modelo de clases).
- **Entidades del Backend.** `Busqueda` y `Alineamiento`, que salen de la tabla 3.2. Forman un agregado: un alineamiento no existe sin su búsqueda, y desde afuera se accede siempre a través de `Busqueda`.
- **Entidades de la Aplicación Web.** `ModeloBusqueda` y `ModeloResultados` son el rol Modelo del MVC: la representación, en el cliente, de la `Busqueda` que se va a ejecutar (su configuración validada y su estado) y de sus `Alineamiento` ya calculados (las filas de la tabla). No son entidades nuevas del dominio, sino la copia en el cliente de dos que ya están en el modelo.
- **Base de datos.** Es el almacén donde queda el historial (D2), en el contenedor *Base de datos*. No es una de las tres categorías de la robustez: se dibuja para mostrar dónde terminan los datos, igual que BLAST+. Solo la toca `RepositorioHistorial`.

**Reglas de conexión verificadas.**

- El actor solo toca la pantalla, y la pantalla solo le delega acciones a `ControladorBusqueda`. **La Vista nunca se conecta con el Backend:** el único camino hacia el servidor es `ControladorBusqueda → ClienteBackend → ControladorEjecucion`.
- Ninguna frontera modifica una entidad. Las flechas punteadas de `PantallaBusqueda` a los Modelos son la **observación de solo lectura** que fija la arquitectura para el MVC de la Aplicación Web (`DA-07`, variante con notificación por suscripción): la Vista se redibuja cuando cambia un Modelo, pero nunca lo modifica ni decide nada con él. Toda modificación pasa por `ControladorBusqueda`. Es la razón de ser de la regla "boundary no toca entity" (que la pantalla no decida ni cambie datos), y aquí se respeta.
- `AdaptadorBlast` recibe datos simples y devuelve los hits como datos, no como `Alineamiento`.
- BLAST+ se alcanza solo a través de su frontera, y la base de datos solo a través del repositorio.

#### 3.4.1 Dónde vive cada regla del negocio

| # | Regla | Dónde vive | Por qué |
|---|---|---|---|
| R1 | % identidad = identidades ÷ longitud del alineamiento × 100; % cobertura = tramo de la query cubierto ÷ longitud de la query × 100 | Entidad `Alineamiento` | Experto: el alineamiento tiene todos los datos para calcularlos. La longitud de la query se la pasa `Busqueda` al crearlo |
| R2 | Al historial va el conjunto **completo** de alineamientos crudos, sin filtrar | Entidad `Busqueda` | Crea un `Alineamiento` por cada hit que devolvió BLAST+ y no descarta ninguno. Es el conjunto que después guarda el repositorio |
| R3 | La tabla se devuelve solo después de que la búsqueda quedó en el historial | `ControladorEjecucion` (orden de los pasos) | Es una regla de coordinación entre dos colaboradores (el repositorio y quien pidió la ejecución), y por eso el orden lo fija el controlador |
| R4 | Si BLAST+ no termina bien, no se muestra tabla ni se guarda nada (garantía mínima de `CU004`) | `AdaptadorBlast` (avisa con `ErrorBlast`) y `ControladorEjecucion` (el error corta el flujo antes de registrar y de guardar) | El Adaptador es quien sabe que BLAST+ falló (código de salida); el controlador no necesita ningún `if`, porque el error interrumpe la secuencia |
| R5 | Los campos de la salida de BLAST+ que no se conocen se ignoran y se advierten, sin tocar los conocidos (`EC-02`) | `AdaptadorBlast` | Táctica *adaptar la interfaz*: el formato de BLAST+ se conoce en un solo lugar (`DA-03`) |
| R6 | La ejecución pasa por los estados *en ejecución*, *finalizada* o *con error*, y la pantalla muestra progreso, tabla o mensaje según el estado | `ModeloBusqueda` (guarda el estado) y `ControladorBusqueda` (lo cambia) | Es estado de la interacción en el cliente, no del dominio. La Vista solo lo lee para decidir qué dibujar |

Las reglas del dominio (R1 a R5) viven en el Backend. La pantalla no aplica ninguna: solo muestra lo que los Modelos tienen.

#### 3.4.2 Elementos del diagrama y componentes de la arquitectura

| Elemento | Tipo | Contenedor | Componente | Capa / rol |
|---|---|---|---|---|
| `PantallaBusqueda` | boundary | Aplicación Web | Pantallas | Vista (MVC) |
| `ControladorBusqueda` | controller | Aplicación Web | Controlador de búsqueda | Controlador (MVC) |
| `ModeloBusqueda` | entity | Aplicación Web | Modelo de búsqueda | Modelo (MVC) |
| `ModeloResultados` | entity | Aplicación Web | Modelo de resultados | Modelo (MVC) |
| `ClienteBackend` | controller | Aplicación Web | Cliente del Backend | Apoyo (fuera de la tríada MVC) |
| `ControladorEjecucion` | controller | Backend | **Ejecución y persistencia** | Dominio |
| `Busqueda`, `Alineamiento` | entity | Backend | Ejecución y persistencia | Dominio |
| `RepositorioHistorial` | controller (interfaz) | Backend | Acceso a datos | Datos |
| `AdaptadorBlast` | boundary | Backend | Adaptador BLAST+ | Datos |
| BLAST+ | sistema externo | — | — | — |
| Base de datos (historial D2) | almacén de datos | Base de datos (PostgreSQL) | — | — |

**Nota sobre el componente Controladores del Backend.** El mensaje de `ClienteBackend` a `ControladorEjecucion` llega por HTTP a una ruta del Backend (componente **Controladores**) que solo convierte la solicitud JSON en la llamada a `ejecutar_busqueda` y el resultado en la respuesta JSON. Es código del framework web sin lógica propia, y por eso no se modela como clase. Así el recorrido respeta la cadena del patrón Capas: Controladores → Ejecución y persistencia → Acceso a datos / Adaptador BLAST+.

### 3.5 Diagramas de secuencia

Hay dos diagramas: el camino principal y el camino de error. Ambos usan los participantes del diagrama de robustez. **Cada flecha sólida es una llamada a una operación de la clase que la recibe**: el texto de la flecha es el nombre de esa operación, que aparece tal cual en el modelo de clases. Las flechas punteadas son respuestas. La única excepción es la flecha hacia BLAST+, que no es una clase nuestra sino un programa externo: su texto es la línea de comandos con que se lo invoca. El participante del Adaptador es la implementación `AdaptadorBlastCli`, porque `leer_salida` y `registrar_advertencia` son operaciones de esa clase; el controlador la conoce solo a través de la interfaz `AdaptadorBlast`.

**Cómo se redibuja la Vista.** Cuando `ControladorBusqueda` cambia un Modelo, la Vista se entera por suscripción (en React, el cambio de estado provoca que el componente se vuelva a dibujar) y lee el Modelo. En los diagramas eso aparece como una nota seguida de la lectura que hace `PantallaBusqueda`. El Modelo nunca llama a la Vista: no la conoce.

#### Secuencia 1 · Camino principal

```mermaid
sequenceDiagram
    autonumber
    actor Inv as Investigador/a
    participant UI as PantallaBusqueda
    participant CB as ControladorBusqueda
    participant MB as ModeloBusqueda
    participant MR as ModeloResultados
    participant CL as ClienteBackend
    participant CE as ControladorEjecucion
    participant B as Busqueda
    participant AB as AdaptadorBlastCli<br/>(implementa AdaptadorBlast)
    participant BL as BLAST+
    participant AL as Alineamiento
    participant RH as RepositorioHistorial<br/>(interfaz)

    Inv->>UI: presionar_ejecutar()
    UI->>CB: ejecutar()
    CB->>MB: configuracion()
    MB-->>CB: configuracion validada
    CB->>MB: marcar_en_ejecucion()
    Note over UI,MB: la Vista observa el cambio y se redibuja
    UI->>UI: mostrar_progreso()
    CB-)CL: ejecutar_busqueda(configuracion)
    Note over CB,CL: llamada asíncrona: la interfaz<br/>sigue navegable mientras espera (CA-01)
    CL->>CE: ejecutar_busqueda(configuracion)
    CE->>B: Busqueda(configuracion, fecha)
    CE->>AB: ejecutar(programa, secuencia, base_datos, remota, parametros)
    AB->>BL: programa -query … -db … -outfmt 5 [-remote] (subproceso propio, EC-01)
    BL-->>AB: salida XML
    AB->>AB: leer_salida(salida_xml)
    opt la salida trae campos desconocidos (EC-02)
        AB->>AB: registrar_advertencia(campos)
    end
    AB-->>CE: hits
    CE->>B: registrar_resultados(hits)
    loop por cada hit
        B->>AL: Alineamiento(hit, longitud_query)
    end
    CE->>RH: guardar(busqueda)
    Note over RH: parámetros, base, fecha y todos<br/>los alineamientos crudos (CA-03)
    CE->>B: tabla_resultados()
    loop por cada alineamiento
        B->>AL: porcentaje_identidad()
        B->>AL: porcentaje_cobertura()
    end
    B-->>CE: filas
    CE-->>CL: filas
    CL-->>CB: filas
    CB->>MR: cargar(filas)
    CB->>MB: marcar_finalizada()
    Note over UI,MR: la Vista observa el cambio y se redibuja
    UI->>MR: filas()
    MR-->>UI: filas
    UI->>UI: mostrar_resultados(filas)
    UI-->>Inv: tabla con hit, score, E-value, % identidad y % cobertura
```

Las tácticas de calidad se ven como operaciones concretas:

- **Introducir concurrencia (`EC-01`).** Cada solicitud de ejecución se atiende en su propio hilo del servidor, y en ese hilo `ejecutar` lanza un **subproceso propio** de BLAST+ y espera su salida (`DA-04`). Los hits vuelven por la misma llamada al mismo `ejecutar_busqueda` que los pidió. No hay ningún lugar compartido donde los resultados de dos búsquedas puedan mezclarse.
- **Adaptar la interfaz y encapsular (`EC-02`).** El controlador y las entidades nunca ven el XML de BLAST+. `leer_salida` toma los campos que conoce por su nombre y, si hay otros, el fragmento `opt` muestra cómo se advierten sin romper nada (`DA-03`).

#### Secuencia 2 · Camino de error: BLAST+ no termina bien

```mermaid
sequenceDiagram
    autonumber
    actor Inv as Investigador/a
    participant UI as PantallaBusqueda
    participant CB as ControladorBusqueda
    participant MB as ModeloBusqueda
    participant CL as ClienteBackend
    participant CE as ControladorEjecucion
    participant B as Busqueda
    participant AB as AdaptadorBlastCli<br/>(implementa AdaptadorBlast)
    participant BL as BLAST+
    participant RH as RepositorioHistorial<br/>(interfaz)

    Inv->>UI: presionar_ejecutar()
    UI->>CB: ejecutar()
    CB->>MB: configuracion()
    MB-->>CB: configuracion validada
    CB->>MB: marcar_en_ejecucion()
    UI->>UI: mostrar_progreso()
    CB-)CL: ejecutar_busqueda(configuracion)
    CL->>CE: ejecutar_busqueda(configuracion)
    CE->>B: Busqueda(configuracion, fecha)
    CE->>AB: ejecutar(programa, secuencia, base_datos, remota, parametros)
    AB->>BL: programa -query … -db … -outfmt 5 [-remote]
    BL-->>AB: código de salida distinto de 0 y mensaje de error
    AB-->>CE: ErrorBlast(mensaje)
    Note over CE,RH: el error corta el flujo: no se registran<br/>resultados ni se llama a guardar (R4)
    CE-->>CL: ErrorBlast(mensaje)
    CL-->>CB: ErrorBlast(mensaje)
    CB->>MB: registrar_error(mensaje)
    Note over UI,MB: la Vista observa el cambio y se redibuja
    UI->>MB: mensaje_error()
    MB-->>UI: mensaje
    UI->>UI: mostrar_error(mensaje)
    UI-->>Inv: mensaje de BLAST+, sin tabla
```

Este camino cubre la garantía mínima de `CU004`: si la ejecución no termina bien, no se muestra ninguna tabla y no se escribe nada en el historial. `RepositorioHistorial` figura en el diagrama justamente para mostrar que no recibe ninguna llamada, y `ModeloResultados` no aparece porque no se carga nada. El tratamiento específico del error remoto (distinguir un timeout de un rechazo de NCBI) es de `HU10_CU004_E1`.

#### 3.5.1 Asignación de responsabilidades

| Responsabilidad | Quién | Criterio GRASP |
|---|---|---|
| Recibir el clic y mostrar progreso, tabla o error según lo que tengan los Modelos | `PantallaBusqueda` | Bajo acoplamiento: solo conoce a `ControladorBusqueda` (para delegar) y a los Modelos (para leer); no decide nada |
| Interpretar la acción "ejecutar" en el cliente: tomar la configuración, cambiar el estado, pedir la ejecución y cargar el resultado o el error | `ControladorBusqueda` | Controlador (del lado cliente) |
| Conservar la configuración validada y el estado de la ejecución | `ModeloBusqueda` | Experto en información |
| Conservar las filas recibidas para la tabla (y luego filtrarlas, en `HU11`) | `ModeloResultados` | Experto en información |
| Hablar con el Backend por HTTP | `ClienteBackend` | Bajo acoplamiento y alta cohesión: es lo único del cliente que conoce la forma de la interfaz REST |
| Coordinar la ejecución en el servidor: crear la búsqueda, invocar a BLAST+, registrar, guardar y devolver la tabla | `ControladorEjecucion` | Controlador: orquesta sin hacer el trabajo del dominio |
| Crear la `Busqueda` | `ControladorEjecucion` | Creador: es quien recibe la configuración con la que se inicializa |
| Crear los `Alineamiento` a partir de los hits | `Busqueda` | Creador: la búsqueda contiene a sus alineamientos y tiene el dato que les falta (la longitud de la query) |
| Calcular % identidad y % cobertura | `Alineamiento` | Experto en información |
| Armar las filas de la tabla | `Busqueda` | Experto: conoce todos sus alineamientos |
| Invocar a BLAST+ y leer su salida, advirtiendo los campos desconocidos | `AdaptadorBlast` | Bajo acoplamiento (es lo único que conoce a BLAST+) y alta cohesión |
| Guardar la búsqueda en el historial | `RepositorioHistorial` | Alta cohesión, bajo acoplamiento y Polimorfismo (ver D9) |

---

