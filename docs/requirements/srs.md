# SRS — LocalBlast

**Especificación de Requerimientos de Software (SRS) — Ingeniería de Software 2026, FIUNER.**
Este documento es la línea base del proyecto **LocalBlast** al cierre del TP1. Se estructura en secciones y se apoya en documentos hermanos para el detalle de diagramas, casos de uso e historias de usuario.

---

## Índice

1. [Visión y alcance](#1-visión-y-alcance)
2. [Stakeholders y usuarios](#2-stakeholders-y-usuarios)
3. [Diagrama de contexto (DFD)](#3-diagrama-de-contexto-dfd)
4. [Modelo de dominio](#4-modelo-de-dominio)
5. [Selección de procesos a profundizar](#5-selección-de-procesos-a-profundizar)
6. [Requerimientos funcionales](#6-requerimientos-funcionales)
7. [Casos de uso e historias de usuario](#7-casos-de-uso-e-historias-de-usuario)
8. [Atributos de calidad (ISO 25010)](#8-atributos-de-calidad-iso-25010)
9. [Suposiciones y dependencias](#9-suposiciones-y-dependencias)
10. [Glosario](#10-glosario)

---

## 1. Visión y alcance

### 1.1 Problema

La ejecución de alineamientos con BLAST presenta hoy dos alternativas incompletas para el usuario típico de un laboratorio o cursada:

- **Línea de comandos (BLAST+):** exige recordar la sintaxis de los binarios (`blastn`, `blastp`, `makeblastdb`, etc.), armar comandos con muchos parámetros, gestionar la ubicación de las bases y parsear la salida a mano. Es la opción más flexible pero tiene barrera de entrada alta.
- **Interfaz web oficial de NCBI:** es accesible pero pesada, no permite ejecutar contra bases de datos propias del laboratorio, y no ofrece filtros interactivos post-búsqueda (identidad, cobertura, taxonomía) sobre la lista de resultados.

Ninguna de las dos permite hoy, con una sola herramienta: correr BLAST **local o remoto** desde la misma interfaz, con **bases de datos propias** del laboratorio administradas por un rol dedicado, aplicar **filtros pre-búsqueda** (parámetros del algoritmo) y **post-búsqueda** (refinamiento sobre resultados) de forma intuitiva, y **descargar los resultados** en el formato que más convenga.

### 1.2 Propuesta de valor

LocalBlast es una **interfaz web para BLAST+** que resuelve las tres carencias:

- El **investigador** decide con un botón si el alineamiento se corre localmente (contra bases del laboratorio) o remotamente (contra NCBI, usando la opción `-remote` del BLAST+).
- El **administrador** puede subir archivos FASTA propios o importar bases públicas (SwissProt, por ejemplo) para dejarlas disponibles como bases locales.
- Los **filtros pre-búsqueda** se cargan en un formulario con valores por defecto sensatos; los **filtros post-búsqueda** se aplican en la tabla de resultados sin volver a correr BLAST.
- Los **resultados** se descargan en CSV, JSON, FASTA, tabular BLAST o XML.

### 1.3 Dentro del alcance (TP1 → TP5)

- Interfaz web para investigador y administrador.
- Ejecución de búsquedas BLAST local (`blastn`, `blastp`, `blastx`, `tblastn`, `tblastx`) y remota (`-remote`).
- Formulario de parámetros pre-búsqueda con valores por defecto.
- Aplicación interactiva de filtros post-búsqueda sobre la tabla de resultados.
- Descarga de resultados en múltiples formatos.
- Alta, actualización y baja de bases de datos locales por parte del administrador, tanto a partir de archivo FASTA subido como de URL pública.
- Autenticación básica con dos roles (Investigador y Administrador).

### 1.4 Fuera del alcance

- Modificación del algoritmo BLAST subyacente. LocalBlast **usa** el motor BLAST+; no lo reimplementa.
- Herramientas de alineamiento múltiple (ClustalW, Muscle) o modelado 3D de estructuras.
- Búsquedas en lote con múltiples queries simultáneas en una sola ejecución (queda como posible ampliación en el Trabajo Integrador).
- Anotación funcional o enriquecimiento biológico de los hits más allá de lo que devuelve BLAST.

---

## 2. Stakeholders y usuarios

| Actor / Stakeholder | Rol | Usa el sistema | Interés en el proyecto |
|---|---|---|---|
| **Investigador/a** | Estudiante de grado/posgrado, tesista, becario/a, docente-investigador/a | Sí (usuario final principal) | Reducir el tiempo de las búsquedas BLAST recurrentes y evitar la fricción de la terminal o de la web de NCBI. |
| **Administrador/a de bases de datos** | Bioinformático/a del laboratorio, técnico/a de IT del grupo de investigación | Sí | Poder mantener bases de datos propias (secuencias del laboratorio) y espejos de bases públicas sin depender del acceso externo. |
| **Docente de la cursada** | Docente de bioinformática o materias afines | Sí (a través del rol Investigador) | Usar la herramienta en clases y trabajos prácticos, reemplazando parcialmente a la web de NCBI. |
| **NCBI** | Proveedor del servicio remoto de BLAST | No es usuario del sistema; es un sistema externo consumido por LocalBlast | Establece los límites de uso de la API remota (rate limits) que el sistema respeta. |
| **Cátedra de Ingeniería de Software (FIUNER)** | Evaluador del proyecto | No | Verificar la aplicación correcta de los conceptos del cuatrimestre. |

Los dos primeros son los actores del modelo de casos de uso (los que aparecen en el diagrama de contexto). El resto son stakeholders sin interacción directa con el sistema.

---

## 3. Diagrama de contexto (DFD)

Los diagramas de contexto (Nivel 0) y su descomposición (Nivel 1), junto con la descripción de procesos, almacenes y flujos, están en:

👉 [`docs/architecture/contexto-inicial.md`](../architecture/contexto-inicial.md)

---

## 4. Modelo de dominio

El modelo de dominio conceptual — entidades esenciales del problema y sus relaciones, sin atributos ni detalles de implementación — está en:

👉 [`docs/requirements/modelo-dominio.md`](modelo-dominio.md)

---

## 5. Selección de procesos a profundizar

De los tres procesos identificados en el DFD Nivel 1 (P1, P2, P3), el grupo elige llevar a profundidad **P1 (Ejecutar búsqueda BLAST)** y **P3 (Administrar bases de datos)**. P2 (Filtrar y entregar resultados) queda documentado a nivel de alcance en el DFD pero no se profundiza como caso de uso propio.

### 5.1 Qué se profundiza y por qué

- **P1 · Ejecutar búsqueda BLAST — profundizado.** Es el proceso *core* del sistema: sin él no hay valor entregable. Concentra la complejidad interesante (dos rutas de ejecución alternativas, validación de parámetros pre-búsqueda, ejecución asíncrona, integración con NCBI y con el binario local). Se detalla como CU-01.

- **P3 · Administrar bases de datos — profundizado.** Es el proceso que habilita el modo local, que es lo que diferencia a LocalBlast de "otra interfaz web sobre NCBI". Sin P3 el laboratorio no puede tener bases propias, y el sistema pierde la mitad de su propuesta de valor. Se detalla como CU-02.

### 5.2 Qué queda fuera del profundizado y por qué

- **P2 · Filtrar y entregar resultados — no profundizado.** Se ejecuta enteramente sobre datos ya en memoria (filtros a la tabla y serialización a un formato) y su lógica es previsible: comparaciones numéricas y export a formatos estándar. No aporta descubrimiento significativo al TP1 ni riesgo de arquitectura para el TP3. Va a ser cubierto en detalle recién en el TP4 (diseño detallado) y TP5 (pruebas), donde su naturaleza combinatoria — muchos filtros, muchos formatos — recién se vuelve relevante.

Elegir dos procesos y no los tres cumple con la recomendación explícita de la cátedra: **"elegir uno bien resuelto vale más que varios a medio desarrollar"**. Se eligieron dos porque están fuertemente relacionados en la propuesta de valor del proyecto (búsqueda local + gestión de bases locales son la misma feature vista desde dos roles distintos), y separar uno sin el otro no capturaría bien el dominio.

---

## 6. Requerimientos funcionales

Los RF-01 a RF-10 corresponden a **P1 (Ejecutar búsqueda BLAST)** y son realizados por el CU-01.
Los RF-11 a RF-14 corresponden a **P3 (Administrar bases de datos)** y son realizados por el CU-02.

### Proceso P1 — Ejecución de búsqueda BLAST

| ID | Requerimiento |
|---|---|
| **RF-01** | El sistema debe permitir al usuario ingresar la secuencia query como texto pegado en el formulario o como archivo FASTA subido. |
| **RF-02** | El sistema debe permitir al usuario elegir entre dos modos de ejecución mutuamente excluyentes: **local** (contra una base del catálogo del laboratorio) o **remoto** (contra NCBI vía la opción `-remote` de BLAST+). |
| **RF-03** | El sistema debe permitir al usuario seleccionar una base de datos disponible para el modo elegido: en modo local, las que figuran en el catálogo administrado por P3; en modo remoto, las bases estándar de NCBI. |
| **RF-04** | El sistema debe permitir al usuario configurar los parámetros pre-búsqueda que afectan al algoritmo: **E-value máximo**, **matriz de sustitución** (para BLAST de proteínas), **tamaño de palabra** y **penalización de gaps** (apertura y extensión). El sistema debe ofrecer valores por defecto sensatos según el programa BLAST correspondiente. |
| **RF-05** | El sistema debe determinar automáticamente el programa BLAST a ejecutar (`blastn`, `blastp`, `blastx`, `tblastn`, `tblastx`) a partir del tipo de la secuencia query y del tipo de la base seleccionada. |
| **RF-06** | El sistema debe validar, antes de ejecutar la búsqueda, que la secuencia query respete el alfabeto declarado o inferido (ADN, ARN o proteína) y que los parámetros pre-búsqueda estén dentro de rangos válidos. |
| **RF-07** | El sistema debe ejecutar la búsqueda de forma asíncrona, mostrando un indicador de progreso, sin bloquear la interfaz de usuario, y debe permitir cancelar una búsqueda en curso. |
| **RF-08** | El sistema debe mostrar los resultados en una tabla con, como mínimo: identificador del hit, score, E-value observado, porcentaje de identidad y porcentaje de cobertura. |
| **RF-09** | El sistema debe permitir aplicar filtros post-búsqueda sobre la tabla de resultados — al menos: umbrales de porcentaje de identidad, porcentaje de cobertura, E-value observado y filtro por taxonomía cuando la información esté disponible — sin volver a ejecutar la búsqueda. |
| **RF-10** | El sistema debe permitir al usuario descargar los resultados filtrados en al menos los formatos: CSV, JSON, FASTA, tabular BLAST (`-outfmt 6`) y XML. |

### Proceso P3 — Administración de bases de datos

| ID | Requerimiento |
|---|---|
| **RF-11** | El sistema debe permitir al administrador dar de alta una nueva base de datos local, indicando: nombre visible, tipo (nucleótidos o proteínas) y origen del archivo FASTA — subiendo un archivo local o indicando la URL de una fuente pública. |
| **RF-12** | El sistema debe construir los índices BLAST (`makeblastdb`) de la nueva base en segundo plano, mostrando un indicador de progreso y sin bloquear la interfaz. |
| **RF-13** | El sistema debe validar que el archivo FASTA sea legible y que su contenido sea consistente con el tipo declarado, y debe rechazar la creación de la base con un mensaje explicativo si la validación falla. |
| **RF-14** | El sistema debe permitir al administrador actualizar o dar de baja una base de datos existente del catálogo, sin afectar las búsquedas en curso ni el historial de búsquedas ya realizadas. |

---

## 7. Casos de uso e historias de usuario

Los casos de uso en formato Cockburn (flujo principal detallado y slices secundarios nombrados) están en:

👉 [`docs/requirements/casos-de-uso.md`](casos-de-uso.md)

Las historias de usuario ya detalladas para el TP1 (slice básico + un slice secundario por CU, con criterios Given-When-Then) están en:

👉 [`docs/requirements/historias-usuario.md`](historias-usuario.md)

**Resumen de la cadena de trazabilidad:**

- **CU-01** realiza RF-01 a RF-10. Slice básico → **HU-01**. Slice A1 → **HU-01.A1**. Slices A2–A6 nombrados.
- **CU-02** realiza RF-11 a RF-14. Slice básico → **HU-02a**. Slice A1 → **HU-02.A1**. Slices A2–A4 nombrados.

---

## 8. Atributos de calidad (ISO 25010)

Cada atributo de calidad se especifica con al menos dos **escenarios** en el formato **fuente – estímulo – artefacto – entorno – respuesta – medida**, cubriendo más de una condición de entorno.

### 8.1 Usabilidad

**Escenario U-1 · Usuario nuevo lanza su primera búsqueda BLAST remota**

| Aspecto | Contenido |
|---|---|
| Fuente | Investigador/a sin experiencia previa con la herramienta. |
| Estímulo | Quiere ejecutar una búsqueda BLAST remota contra NCBI a partir de una secuencia pegada en el formulario. |
| Artefacto | Interfaz web del sistema. |
| Entorno | Primera sesión del usuario, sin capacitación previa. |
| Respuesta | El usuario completa el formulario, ejecuta la búsqueda y descarga el resultado. |
| Medida | El usuario lo logra en **menos de 3 minutos** desde que abre la aplicación, sin consultar documentación externa. |

**Escenario U-2 · Interpretación de un error de validación de parámetros**

| Aspecto | Contenido |
|---|---|
| Fuente | Investigador/a que ingresó un parámetro pre-búsqueda fuera de rango. |
| Estímulo | Presiona "Ejecutar búsqueda" con un E-value negativo. |
| Artefacto | Formulario de parámetros de la interfaz. |
| Entorno | Uso normal, con conexión estable. |
| Respuesta | El sistema resalta el campo con problema y muestra un mensaje que indica **cuál es el rango válido** para ese parámetro. |
| Medida | El usuario corrige el valor y ejecuta la búsqueda en **menos de 30 segundos** desde el error. |

### 8.2 Rendimiento (Eficiencia de Desempeño)

**Escenario R-1 · Búsqueda local de tamaño estándar contra base propia del laboratorio**

| Aspecto | Contenido |
|---|---|
| Fuente | Investigador/a. |
| Estímulo | Lanza una búsqueda `blastp` de una secuencia de ~500 aminoácidos contra una base local de ≤10.000 secuencias. |
| Artefacto | Motor BLAST+ local invocado por el sistema. |
| Entorno | Servidor del laboratorio en operación normal (CPU con carga baja, base ya indexada). |
| Respuesta | El sistema entrega los resultados en la interfaz. |
| Medida | Tiempo total desde "Ejecutar" hasta que la tabla aparece completa: **menor a 10 segundos** en el percentil 95 de las ejecuciones. |

**Escenario R-2 · Aplicación de filtros post-búsqueda sobre resultados ya cargados**

| Aspecto | Contenido |
|---|---|
| Fuente | Investigador/a. |
| Estímulo | Cambia un umbral de filtro (por ejemplo % identidad mínimo de 70 a 80) sobre una tabla ya renderizada con 1.000 hits. |
| Artefacto | Módulo de filtros post-búsqueda de la interfaz. |
| Entorno | Uso normal en el navegador del usuario. |
| Respuesta | La tabla se actualiza para mostrar solo los hits que superan el nuevo umbral. |
| Medida | La actualización se completa en **menos de 500 ms**, sin llamada al backend. |

### 8.3 Seguridad

**Escenario S-1 · Investigador intenta administrar bases de datos**

| Aspecto | Contenido |
|---|---|
| Fuente | Usuario con rol Investigador (no Administrador). |
| Estímulo | Intenta acceder a la URL de la sección "Administración de bases de datos". |
| Artefacto | Módulo de autorización del sistema. |
| Entorno | Uso normal, sesión iniciada correctamente como Investigador. |
| Respuesta | El sistema deniega el acceso y redirige a una página de "no autorizado". No se listan las bases ni se filtra la operación por otro camino. |
| Medida | En el **100%** de los intentos, incluso reintentos posteriores a un cambio de rol simulado desde el cliente, el acceso queda denegado. |

**Escenario S-2 · Subida de un archivo malicioso como si fuera FASTA**

| Aspecto | Contenido |
|---|---|
| Fuente | Administrador (o atacante con credenciales de administrador comprometidas). |
| Estímulo | Sube un archivo binario grande con extensión `.fasta`. |
| Artefacto | Módulo de subida y validación de bases de datos (P3). |
| Entorno | Uso adverso — se asume que las credenciales pueden filtrarse; no se confía en el rol solo. |
| Respuesta | El sistema rechaza el archivo antes de invocar `makeblastdb`, sin dejar residuos en el sistema de archivos y sin exponer el contenido en la respuesta HTTP. |
| Medida | El archivo se descarta en **menos de 2 segundos** independientemente de su tamaño, con un log del intento. |

### 8.4 Confiabilidad

**Escenario C-1 · NCBI no responde durante la búsqueda**

| Aspecto | Contenido |
|---|---|
| Fuente | Servicio remoto NCBI. |
| Estímulo | No responde a la solicitud dentro del timeout esperado. |
| Artefacto | Componente de integración con NCBI (dentro de P1). |
| Entorno | Modo remoto, conexión a Internet operativa desde el servidor del laboratorio. |
| Respuesta | El sistema informa al investigador que NCBI no respondió, no deja la búsqueda "colgada" y ofrece reintentar o cambiar a modo local. La interfaz vuelve a estado operativo. |
| Medida | El usuario recibe el mensaje de fallo en **menos de 60 segundos** desde el timeout, y la interfaz queda usable inmediatamente para lanzar una nueva búsqueda. |

**Escenario C-2 · Cancelación limpia de una búsqueda local en curso**

| Aspecto | Contenido |
|---|---|
| Fuente | Investigador/a. |
| Estímulo | Presiona "Cancelar" con una búsqueda local en curso. |
| Artefacto | Componente de ejecución asíncrona de BLAST local (dentro de P1). |
| Entorno | Servidor operativo, uso normal. |
| Respuesta | El sistema aborta el subproceso `blastn`/`blastp` correspondiente, libera memoria y archivos temporales asociados, y deja la interfaz lista para una nueva búsqueda. Ningún archivo residual queda en el sistema. |
| Medida | En el **100%** de las cancelaciones, el subproceso queda terminado en menos de 5 segundos y no aparecen archivos temporales asociados a esa ejecución. |

### 8.5 Mantenibilidad

**Escenario M-1 · Agregar un nuevo formato de descarga**

| Aspecto | Contenido |
|---|---|
| Fuente | Grupo de desarrollo (futuros TP4/TP5). |
| Estímulo | Requerimiento nuevo: sumar un formato adicional a la descarga (por ejemplo, HTML enriquecido). |
| Artefacto | Módulo de exportación de resultados (P2). |
| Entorno | Desarrollo, con tests existentes verdes. |
| Respuesta | El nuevo formato queda disponible en el selector de descarga sin modificar el resto del pipeline de resultados. |
| Medida | El cambio se implementa modificando **exactamente un módulo** de exportación y agregando un test, sin tocar la lógica de búsqueda ni de filtros. |

**Escenario M-2 · Cambio de la matriz de sustitución por defecto**

| Aspecto | Contenido |
|---|---|
| Fuente | Docente / administrador del laboratorio. |
| Estímulo | Decide cambiar el default de la matriz de sustitución para `blastp` de BLOSUM62 a BLOSUM80. |
| Artefacto | Configuración de parámetros por defecto del sistema. |
| Entorno | Producción del laboratorio. |
| Respuesta | El nuevo default queda vigente para todas las nuevas búsquedas, sin necesidad de redeploy. |
| Medida | El cambio se aplica editando **un solo archivo de configuración** y reiniciando el servicio; ningún código fuente se modifica. |

---

## 9. Suposiciones y dependencias

- El binario **BLAST+** (versión 2.14 o posterior) está disponible en el servidor donde corre el sistema. Es una dependencia externa: LocalBlast **usa** BLAST+, no lo empaqueta.
- La API remota de NCBI (`https://blast.ncbi.nlm.nih.gov/Blast.cgi`) está disponible desde la red del servidor cuando el usuario elige modo remoto. Las políticas de uso responsable de NCBI se respetan (frecuencia de polling, límite de queries por unidad de tiempo).
- El servidor tiene espacio en disco suficiente para alojar las bases locales del laboratorio y los archivos temporales de las búsquedas.
- Los usuarios acceden por HTTPS desde navegadores modernos.

---

## 10. Glosario

| Término | Significado |
|---|---|
| **BLAST** | *Basic Local Alignment Search Tool*: familia de algoritmos para buscar regiones de similitud local entre secuencias biológicas. |
| **BLAST+** | Suite oficial de línea de comandos de NCBI que implementa BLAST (`blastn`, `blastp`, `makeblastdb`, etc.). Es la herramienta que LocalBlast envuelve. |
| **Query** | Secuencia biológica que el investigador quiere alinear contra una base. |
| **Base de datos BLAST** | Conjunto de secuencias biológicas indexadas para búsqueda BLAST. Físicamente: los archivos `.nhr/.nin/.nsq` (nucleótidos) o `.phr/.pin/.psq` (proteínas) generados por `makeblastdb`. |
| **Hit / Alineamiento** | Cada una de las coincidencias que BLAST devuelve entre la query y una secuencia de la base. |
| **E-value** | Cantidad esperada de hits del mismo score o mejor que se obtendrían por azar. Cuanto más bajo, más significativa la coincidencia. |
| **Matriz de sustitución** | Tabla que puntúa cada posible sustitución entre residuos, usada por BLAST de proteínas (BLOSUM62, PAM30, etc.). |
| **FASTA** | Formato de texto para representar secuencias biológicas, con un encabezado `>ID descripción` seguido de la secuencia. |
| **SwissProt** | Base de datos curada de proteínas, parte de UniProtKB. Un ejemplo típico de base pública que un laboratorio querría espejar localmente. |
| **`makeblastdb`** | Utilitario de BLAST+ que construye los índices de una base a partir de un archivo FASTA. |
| **Filtro pre-búsqueda** | Valor de un parámetro del algoritmo BLAST que se fija antes de ejecutar y que afecta al resultado (E-value máximo, matriz, tamaño de palabra, etc.). |
| **Filtro post-búsqueda** | Criterio que se aplica sobre resultados ya calculados para restringir qué se muestra o descarga, sin volver a correr BLAST (umbral de % identidad, cobertura, taxón). |
