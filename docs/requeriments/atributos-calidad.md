# Atributos de Calidad y Escenarios — LocalBlast

Este documento contiene los **requerimientos no funcionales** del sistema, expresados como atributos de calidad y sus correspondientes **escenarios de calidad** (fuente–estímulo–artefacto–entorno–respuesta–medida), siguiendo el modelo **ISO/IEC 25010**.

La selección de los cinco atributos que se profundizan no fue arbitraria: se aplicó el método de dos etapas visto en la teoría — **filtrado** primero (descartar los que no aplican al dominio) y **priorización por comparación pareada** después (matriz `^`/`<` donde cada atributo se enfrenta a los demás y se cuenta cuántas veces "gana"). El filtrado se mantuvo deliberadamente **liviano** — solo se descartaron los atributos manifiestamente inaplicables — para que fuera la matriz, y no el criterio a priori del grupo, la que hiciera el trabajo real de discriminación. Ambas etapas están documentadas para que cualquier lector pueda auditar las decisiones.

---

## Índice

1. [Filtrado inicial de atributos](#1-filtrado-inicial-de-atributos)
2. [Priorización por comparación pareada](#2-priorización-por-comparación-pareada)
3. [Los cinco atributos elegidos](#3-los-cinco-atributos-elegidos)
4. [Escenarios de calidad](#4-escenarios-de-calidad)
5. [Trazabilidad hacia los procesos y RFs](#5-trazabilidad-hacia-los-procesos-y-rfs)

---

## 1. Filtrado inicial de atributos

Partimos del universo amplio de atributos que la teoría de la materia identifica como candidatos: Performance, Escalabilidad, Disponibilidad, Recuperación, Confiabilidad, Robustez, Integridad, Administrabilidad, Seguridad, Interoperabilidad, Capacidad, Mantenibilidad, Extensibilidad, Flexibilidad, Reusabilidad, Portabilidad, Testeabilidad, Usabilidad. Sobre ese universo hicimos dos operaciones **antes** de la matriz de priorización: (a) descarte de atributos manifiestamente inaplicables al dominio, y (b) fusión explícita de atributos que se solapan en el nivel de detalle del TP.

### 1.1 Atributos descartados

Solo tres atributos se descartan de plano; para todos los demás, la matriz será la que decida su relevancia relativa:

| Atributo descartado | Motivo |
|---|---|
| **Portabilidad** | El sistema se ejecuta como aplicación web sobre un servidor del laboratorio; no hay requisito de correr en múltiples sistemas operativos ni de empaquetarse para distintos entornos. Ningún RF del SRS lo pide. |
| **Reusabilidad** | LocalBlast es un producto puntual, no una biblioteca de componentes reutilizables por otros sistemas. La reusabilidad interna de módulos es una preocupación de diseño (TP4), no un atributo de calidad observable. |
| **Administrabilidad** | El rol Administrador y el proceso P3 están explícitamente **fuera del alcance profundizado** ([SRS 1.4](srs.md#14-fuera-del-alcance)); sin ese proceso, no hay superficie sobre la que redactar escenarios de administrabilidad. |

### 1.2 Fusiones explícitas

Cuatro atributos se fusionan dentro de otros por solapamiento fuerte a este nivel de detalle. La fusión se hace **antes** de la matriz para no duplicar preocupaciones en las comparaciones pareadas:

| Fusionado en | Se absorbe |
|---|---|
| **Confiabilidad** | **Robustez** — en ISO 25010, la tolerancia a fallos (que es lo que informalmente llamamos "robustez") es sub-atributo de Fiabilidad. Los escenarios de tolerancia a fallos se redactan bajo Confiabilidad. |
| **Escalabilidad** | **Capacidad** — ambos se refieren al comportamiento del sistema frente al crecimiento de la carga (usuarios, volumen). En un TP con alcance de un laboratorio, no amerita separarlos. |
| **Mantenibilidad** | **Extensibilidad** — en ISO 25010, la modificabilidad y la modularidad (base de la extensibilidad) son sub-atributos de Mantenibilidad. |
| **Mantenibilidad** | **Flexibilidad** — la flexibilidad se realiza a través de una arquitectura mantenible; sin una decisión de diseño concreta que la separe (por ejemplo, un motor de reglas configurable), se cuenta como parte de Mantenibilidad. |

### 1.3 Atributos que entran a la matriz de priorización

Tras los descartes y las fusiones, quedan **once atributos** que entran a la matriz. Es un número similar al del ejemplo de la cátedra (12) y suficientemente amplio para que la matriz sea el instrumento efectivo de discriminación, no un trámite:

1. Performance
2. Escalabilidad (absorbe Capacidad)
3. Disponibilidad
4. Recuperación
5. Confiabilidad (absorbe Robustez)
6. Integridad
7. Seguridad
8. Interoperabilidad
9. Mantenibilidad (absorbe Extensibilidad y Flexibilidad)
10. Testeabilidad
11. Usabilidad

Nota deliberada sobre dos atributos "de riesgo":

- **Seguridad** entra a la matriz pese a que el propio SRS declara la autenticación fuera de alcance ([SRS 1.4](srs.md#14-fuera-del-alcance)). No la descartamos a priori para dejar que la matriz **audite** esa decisión: si Seguridad es efectivamente irrelevante en el alcance del TP, debería terminar con muy pocas victorias.
- **Disponibilidad** entra por la misma razón: no hay SLA definido, pero preferimos que la matriz lo confirme antes que descartarla por intuición.

---

## 2. Priorización por comparación pareada

Aplicamos el método de la cátedra: cada atributo se compara contra todos los demás y en cada celda se anota `^` si el atributo de la **fila** es más importante para LocalBlast que el de la **columna**, o `<` si es menos importante. Al final, contamos cuántas veces "ganó" cada atributo (cantidad de `^` en su fila) y ese conteo define el orden.

Notación:

- `^` — el atributo de la fila es más relevante que el de la columna.
- `<` — el atributo de la fila es menos relevante que el de la columna.
- `—` — celda diagonal (un atributo no se compara consigo mismo).

### 2.1 Matriz de comparación pareada

|                       | Perf | Esc | Disp | Rec | Conf | Int | Seg | Interop | Mant | Test | Usa | **Orden** |
|-----------------------|:----:|:---:|:----:|:---:|:----:|:---:|:---:|:-------:|:----:|:----:|:---:|:---------:|
| **Performance**       |  —   |  ^  |  ^   |  ^  |  <   |  <  |  ^  |    <    |  ^   |  ^   |  <  |   **6**   |
| **Escalabilidad**     |  <   |  —  |  <   |  <  |  <   |  <  |  ^  |    <    |  <   |  <   |  <  |   **1**   |
| **Disponibilidad**    |  <   |  ^  |  —   |  ^  |  <   |  <  |  ^  |    <    |  <   |  ^   |  <  |   **4**   |
| **Recuperación**      |  <   |  ^  |  <   |  —  |  <   |  <  |  ^  |    <    |  <   |  <   |  <  |   **2**   |
| **Confiabilidad**     |  ^   |  ^  |  ^   |  ^  |  —   |  <  |  ^  |    <    |  ^   |  ^   |  <  |   **7**   |
| **Integridad**        |  ^   |  ^  |  ^   |  ^  |  ^   |  —  |  ^  |    <    |  ^   |  ^   |  <  |   **8**   |
| **Seguridad**         |  <   |  <  |  <   |  <  |  <   |  <  |  —  |    <    |  <   |  <   |  <  |   **0**   |
| **Interoperabilidad** |  ^   |  ^  |  ^   |  ^  |  ^   |  ^  |  ^  |    —    |  ^   |  ^   |  ^  |  **10**   |
| **Mantenibilidad**    |  <   |  ^  |  ^   |  ^  |  <   |  <  |  ^  |    <    |  —   |  ^   |  <  |   **5**   |
| **Testeabilidad**     |  <   |  ^  |  <   |  ^  |  <   |  <  |  ^  |    <    |  <   |  —   |  <  |   **3**   |
| **Usabilidad**        |  ^   |  ^  |  ^   |  ^  |  ^   |  ^  |  ^  |    <    |  ^   |  ^   |  —  |   **9**   |

Chequeo de consistencia: la matriz es **antisimétrica** (si `(i,j) = ^` entonces `(j,i) = <`) y la suma de victorias totaliza `C(11,2) = 55` (verificable: `6+1+4+2+7+8+0+10+5+3+9 = 55`).

### 2.2 Justificación de las comparaciones no obvias

Muchas comparaciones son directas, pero algunas ameritan justificación explícita — son las que el docente puede pedir defender en la presentación:

- **Interoperabilidad > todo lo demás (10 de 10).** Sin invocación correcta a BLAST+ el sistema **no funciona en absoluto** — no hay resultados que mostrar, ni interfaz que usar, ni datos que preservar íntegros. Es la dependencia externa dura sobre la que se apoya todo el valor de LocalBlast (ver `srs.md` sec. 8 y `contexto-inicial.md`). Por eso gana todas las comparaciones, incluso contra Usabilidad.

- **Usabilidad > Confiabilidad e Integridad.** Es una decisión discutida. La razón de ser del proyecto (según la [sección 1.1 del SRS](srs.md#11-problema)) es que ni la CLI de BLAST+ ni la web NCBI son suficientemente usables para el perfil objetivo. Si LocalBlast fuera perfectamente confiable pero igual de duro de usar que la CLI, no aportaría valor sobre las alternativas existentes. Confiabilidad e Integridad son baseline; Usabilidad es el diferenciador.

- **Integridad > Confiabilidad.** Discutible porque en ISO 25010 la integridad de datos suele considerarse parte de Fiabilidad. La separamos porque los escenarios que nos preocupan (historial D2 con búsquedas parcialmente persistidas, race conditions en escrituras concurrentes, cancelaciones dejando estado inconsistente) son específicos de la integridad transaccional. Un sistema puede recuperarse de un crash y aun así dejar datos inconsistentes.

- **Performance > Disponibilidad, Recuperación y Escalabilidad.** En un laboratorio, tolerar que el sistema esté caído unos minutos es aceptable; que sea lento en cada búsqueda no lo es. El punto de comparación está en la CLI de BLAST+ como alternativa: la CLI está siempre disponible pero es lenta de operar por su usabilidad. LocalBlast tiene que ser rápido de usar.

- **Confiabilidad > Recuperación.** En ISO 25010 la recuperabilidad es sub-atributo de Fiabilidad; a este nivel de detalle, Confiabilidad la absorbe conceptualmente. La ganamos por diferencia clara.

- **Mantenibilidad > Testeabilidad.** En ISO 25010 la testeabilidad es sub-atributo de Mantenibilidad; aunque en el contexto de un TP con presentaciones periódicas la testeabilidad tiene valor por sí misma, la Mantenibilidad la abarca. Es coherente con la decisión de fusión que hicimos en 1.2.

- **Disponibilidad > Testeabilidad, pero Confiabilidad > Disponibilidad.** La disponibilidad es lo que el usuario final observa (sistema up o down); la testeabilidad es una preocupación del equipo. Pero por debajo de ambas está la confiabilidad como capacidad de mantenerse operativo.

- **Seguridad = 0 victorias.** Es el resultado que valida el descarte propuesto en el filtrado inicial (1.3): Seguridad no gana ninguna comparación en este alcance específico. Este es exactamente el tipo de resultado que buscábamos al meter Seguridad en la matriz — que la propia matriz confirmara la intuición sobre "fuera de alcance".

- **Escalabilidad = 1 victoria (solo contra Seguridad).** Confirma que el dimensionamiento para un laboratorio no impone requisitos de escalabilidad significativos; lo que importa (varios usuarios concurrentes) se cubre como escenario de sobrecarga dentro de Performance y Confiabilidad.

### 2.3 Ranking final

Ordenando por cantidad de victorias, de mayor a menor:

| Ranking | Atributo | Victorias |
|:---:|---|:---:|
| 🥇 1 | **Interoperabilidad** | 10 |
| 🥈 2 | **Usabilidad** | 9 |
| 🥉 3 | **Integridad** | 8 |
| 4 | **Confiabilidad** | 7 |
| 5 | **Performance** | 6 |
| 6 | Mantenibilidad | 5 |
| 7 | Disponibilidad | 4 |
| 8 | Testeabilidad | 3 |
| 9 | Recuperación | 2 |
| 10 | Escalabilidad | 1 |
| 11 | Seguridad | 0 |

### 2.4 Selección del umbral

Siguiendo el método del PDF de la cátedra (que en su ejemplo usa un umbral para dejar los cinco atributos más relevantes), fijamos el **umbral en 6 victorias**. Los atributos con 6 o más victorias son los que consideramos críticos para el diseño de LocalBlast. Los que quedan por debajo — Mantenibilidad, Disponibilidad, Testeabilidad, Recuperación, Escalabilidad y Seguridad — siguen siendo preocupaciones legítimas del equipo, pero no motivan escenarios de calidad propios en este TP.

El umbral discrimina **seis atributos "afuera" y cinco "adentro"**: la matriz hace efectivamente el trabajo de selección, no un mero refinamiento del filtrado inicial.

---

## 3. Los cinco atributos elegidos

De la priorización surgen los cinco atributos sobre los que redactamos escenarios detallados:

| # | Atributo | Categoría ISO 25010 | Sub-característica ISO 25010 |
|:---:|---|---|---|
| 1 | **Interoperabilidad** | Compatibilidad | Interoperabilidad |
| 2 | **Usabilidad** | Usabilidad | Operabilidad, Aprendizaje, Protección contra errores |
| 3 | **Integridad** | Fiabilidad | Integridad transaccional (variante de dominio) |
| 4 | **Confiabilidad** | Fiabilidad | Tolerancia a fallos |
| 5 | **Performance** | Eficiencia de desempeño | Comportamiento temporal |

Para cada uno se redactan **tres escenarios** cubriendo distintas condiciones de entorno: **normal**, **sobrecarga** y **degradado**, siguiendo el molde de seis campos que muestra el ejemplo resuelto de la cátedra.

---

## 4. Escenarios de calidad

### 4.1 Interoperabilidad — Compatibilidad con BLAST+

Es el atributo prioritario: todo el sistema depende de invocar correctamente a BLAST+ y de parsear sus resultados. Los escenarios cubren la operación normal, la coexistencia de modos local y remoto bajo carga, y el manejo de incompatibilidades de versión o indisponibilidad de NCBI.

**Escenario 1 — entorno normal**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Lanza una búsqueda `blastn` en modo local con parámetros válidos contra una base de datos del catálogo D1 |
| Entorno | Operación normal, BLAST+ 2.14 o posterior instalado, catálogo D1 con al menos una BD válida |
| Artefacto | Módulo de invocación a BLAST+ (P1) y parser de resultados |
| Respuesta | El sistema construye la invocación con la sintaxis correcta, ejecuta el binario, recibe el resultado y lo parsea a la estructura interna de alineamientos |
| Medida de respuesta | 100% de las búsquedas contra versiones soportadas de BLAST+ devuelven un resultado parseable sin intervención manual |

**Escenario 2 — entorno de sobrecarga (coexistencia de modos)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Múltiples investigadores/as |
| Estímulo | Lanzan simultáneamente búsquedas en modo local y remoto (hasta 10 en simultáneo, mezcla de ambos) |
| Entorno | Sobrecarga — pico de uso del laboratorio |
| Artefacto | Módulos de invocación a BLAST+ para local y para remoto (dos rutas de código sobre el mismo binario) |
| Respuesta | El sistema serializa las invocaciones sin mezclar parámetros entre búsquedas y respetando la política de frecuencia hacia NCBI (delegada a BLAST+ con la flag `-remote`) |
| Medida de respuesta | 0% de búsquedas con parámetros contaminados de otra búsqueda concurrente; 100% de las remotas respetan las políticas de uso responsable de NCBI (verificable en los logs de BLAST+) |

**Escenario 3 — entorno degradado (incompatibilidad de versión o NCBI caído)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a (que dispara la búsqueda) + entorno externo (BLAST+ o NCBI) |
| Estímulo | Lanza una búsqueda cuando (a) el binario BLAST+ instalado devuelve un formato de salida no esperado por el parser (por ejemplo, un campo nuevo en una versión posterior), o (b) NCBI no responde en modo remoto |
| Entorno | Degradado — incompatibilidad de versión / servicio externo indisponible |
| Artefacto | Parser de resultados / Módulo de modo remoto |
| Respuesta | El sistema detecta el desvío o el timeout, no crashea, notifica al usuario con un mensaje específico (`"Versión de BLAST+ no soportada"` / `"NCBI no responde, reintente más tarde"`) y no persiste una búsqueda incompleta en D2 |
| Medida de respuesta | 100% de las incompatibilidades y timeouts se comunican al usuario con un mensaje que nombra la causa; 0% de registros parciales quedan en D2 |

---

### 4.2 Usabilidad — Operabilidad y protección contra errores

Es el atributo diferenciador de LocalBlast: la razón por la que el sistema existe es que la CLI y la web NCBI son duras de operar para el perfil objetivo.

**Escenario 1 — entorno normal**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a nuevo en LocalBlast (habituado a la CLI de BLAST+ o a la web NCBI) |
| Estímulo | Ingresa por primera vez y quiere correr una búsqueda `blastn` con valores por defecto |
| Entorno | Operación normal, primera sesión del usuario, sin capacitación previa ni documentación abierta |
| Artefacto | Interfaz gráfica (formulario de carga de secuencia y de configuración, CU001 + CU002) |
| Respuesta | El usuario logra completar una búsqueda end-to-end (cargar secuencia → configurar → ejecutar → ver resultados) sin consultar documentación externa |
| Medida de respuesta | 90% de los usuarios nuevos completan una búsqueda con valores por defecto en menos de 5 minutos desde la primera pantalla, medido con una prueba de usabilidad con al menos 5 participantes representativos del perfil |

**Escenario 2 — entorno de sobrecarga (muchos resultados + filtros encadenados)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Ejecuta una búsqueda que devuelve más de 500 hits y aplica tres filtros post-búsqueda encadenados (identidad ≥ 90%, cobertura ≥ 80%, taxón específico) |
| Entorno | Sobrecarga cognitiva y visual — tabla larga, filtros interactivos aplicados en secuencia |
| Artefacto | Tabla de resultados con filtros post-búsqueda (P2, CU006) |
| Respuesta | El sistema aplica los filtros incrementalmente, sin recargar la página, mostrando la cuenta de hits que sobreviven a cada uno |
| Medida de respuesta | Cada filtro se aplica en menos de 1 segundo sobre 500 hits; la cuenta de hits visibles se actualiza sin que el usuario tenga que hacer acciones adicionales (ni "aplicar" ni "recargar") |

**Escenario 3 — entorno degradado (usuario comete un error semántico frecuente)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a con poca experiencia en BLAST |
| Estímulo | Elige un programa BLAST incompatible con su secuencia (por ejemplo, `blastn` con una query de proteína) |
| Entorno | Degradado — usuario cometiendo un error semántico frecuente en el dominio |
| Artefacto | Validación semántica pre-ejecución (RF-12, CU003) y mensajes al usuario |
| Respuesta | El sistema bloquea el lanzamiento, explica el motivo con lenguaje del dominio (`"El programa blastn es para nucleótidos; tu query parece ser de proteína — probá con blastp o blastx"`) y sugiere alternativas viables |
| Medida de respuesta | 100% de las combinaciones incompatibles son bloqueadas con un mensaje que nombra explícitamente la alternativa correcta; en pruebas con usuarios sin capacitación, el 90% resuelve el error sin ayuda externa en menos de 30 segundos |

---

### 4.3 Integridad — Consistencia del historial D2 y de las búsquedas

Los escenarios se centran en el almacén D2 (búsquedas y resultados históricos) y en garantizar que ninguna combinación de operaciones concurrentes o interrupciones deje datos parciales o mezclados.

**Escenario 1 — entorno normal**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Ejecuta una búsqueda que termina exitosamente |
| Entorno | Operación normal |
| Artefacto | Módulo de persistencia en historial D2 (parte de CU005, RF-10) |
| Respuesta | El sistema almacena la búsqueda completa (parámetros pre-búsqueda, base de datos, timestamp, resultados crudos) en D2 de forma atómica |
| Medida de respuesta | 100% de las búsquedas exitosas quedan en D2 con todos sus campos poblados; auditoría posterior no encuentra registros parciales |

**Escenario 2 — entorno de sobrecarga (escrituras concurrentes)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Varios investigadores/as |
| Estímulo | Cinco búsquedas terminan casi simultáneamente y se persisten en D2 en el mismo segundo |
| Entorno | Sobrecarga — escrituras concurrentes en el mismo almacén |
| Artefacto | Módulo de persistencia en D2 con acceso concurrente (CU005) |
| Respuesta | El sistema serializa las escrituras sin colisiones ni pérdidas; cada búsqueda queda con su identificador único y sus resultados correctamente asociados a sus parámetros |
| Medida de respuesta | 0% de mezclado de resultados entre búsquedas; 0% de búsquedas exitosas perdidas por race condition, verificado bajo una prueba de concurrencia con al menos 5 escrituras/segundo |

**Escenario 3 — entorno degradado (cancelación o falla a mitad de la ejecución)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a (cancelación explícita, RF-08) o BLAST+ (crash / timeout) |
| Estímulo | Una búsqueda se interrumpe antes de terminar |
| Entorno | Degradado — ejecución abortada a mitad de camino |
| Artefacto | Módulo de ejecución (CU004) y módulo de persistencia (CU005) |
| Respuesta | El sistema **no** persiste la búsqueda en D2 (o, si registra su existencia, la marca explícitamente como `"cancelada"` sin resultados asociados); no deja archivos temporales huérfanos y libera los recursos del proceso BLAST+ |
| Medida de respuesta | 100% de las búsquedas canceladas o abortadas no dejan registros en D2 con estado inconsistente; 0% de archivos temporales huérfanos en disco, verificado por barrido posterior a la prueba |

---

### 4.4 Confiabilidad — Tolerancia a fallos

Cubre el comportamiento del pipeline P1 completo ante variaciones de la carga y ante fallos de la dependencia externa (BLAST+). Absorbe conceptualmente lo que en el análisis inicial figuraba como Robustez.

**Escenario 1 — entorno normal**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Ejecuta una búsqueda con parámetros dentro de rangos habituales |
| Entorno | Operación normal, BLAST+ instalado, catálogo D1 poblado |
| Artefacto | Pipeline P1 completo (validación sintáctica → configuración → validación semántica → invocación → parseo de resultados → persistencia) |
| Respuesta | La búsqueda se completa exitosamente y los resultados se muestran al usuario |
| Medida de respuesta | Tasa de éxito ≥ 99% de las búsquedas lanzadas con parámetros válidos en condiciones normales |

**Escenario 2 — entorno de sobrecarga (secuencia query muy grande)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Carga una secuencia query grande (por ejemplo, un cromosoma bacteriano completo, ~5 MB de nucleótidos) y ejecuta `blastn` contra una base de datos grande |
| Entorno | Sobrecarga — carga de trabajo cerca de los límites del servidor |
| Artefacto | Módulo de ejecución asíncrona con indicador de progreso (RF-08, CU004) |
| Respuesta | El sistema muestra progreso, mantiene la UI responsiva, no timeoutea prematuramente y, o bien devuelve resultados completos, o bien notifica al usuario un timeout controlado con opción de ajustar parámetros |
| Medida de respuesta | 0% de fallas silenciosas; 100% de las búsquedas largas terminan con resultados válidos o con una notificación explícita de timeout que nombra el motivo y no queda persistida en D2 |

**Escenario 3 — entorno degradado (BLAST+ falla durante la ejecución)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | BLAST+ (proceso externo) |
| Estímulo | Devuelve un `exit code` distinto de 0 a mitad de la ejecución (por ejemplo, por falta de memoria o índice de BD corrupto) |
| Entorno | Degradado — dependencia externa fallando |
| Artefacto | Módulo de invocación a BLAST+ y manejo de excepciones (CU004) |
| Respuesta | El sistema captura el error, no propaga el crash a la GUI, muestra al usuario el mensaje de BLAST+ (o una traducción amigable) y ofrece las opciones de reintentar o volver a la pantalla de configuración |
| Medida de respuesta | 100% de los `exit code` ≠ 0 de BLAST+ se capturan y se comunican al usuario; 0% de casos en que la GUI quede colgada esperando resultados que nunca van a llegar |

---

### 4.5 Performance — Comportamiento temporal

El tiempo que consume BLAST+ propiamente dicho depende del tamaño de la BD y no está bajo control de LocalBlast; los escenarios se enfocan en el **overhead** que agrega el sistema y en la **reactividad de la UI** durante búsquedas concurrentes.

**Escenario 1 — entorno normal**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Carga una secuencia query pequeña (< 1 KB, típico de un gen o una proteína individual) y hace clic en `"Ejecutar"` en modo local |
| Entorno | Operación normal, sin otras búsquedas concurrentes |
| Artefacto | Pipeline P1 completo (validación de query + validación semántica + invocación a BLAST+ local) |
| Respuesta | El sistema valida la entrada, lanza la búsqueda y presenta los resultados. El tiempo total percibido incluye la ejecución de BLAST+ (dependiente del tamaño de la BD, mostrado como progreso) |
| Medida de respuesta | El overhead atribuible a LocalBlast (validaciones + parseo de resultados + render de la tabla) es menor a 2 segundos; el resto del tiempo es el que consume BLAST+ y se refleja en el indicador de progreso |

**Escenario 2 — entorno de sobrecarga (UI reactiva con búsqueda en curso)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Lanzó una búsqueda que tarda más de 30 segundos y, mientras espera, navega la interfaz (por ejemplo, prepara la siguiente búsqueda en otra pestaña de la app) |
| Entorno | Sobrecarga — la interfaz debe seguir respondiendo mientras una búsqueda corre en background |
| Artefacto | Ejecución asíncrona (RF-08) + UI reactiva |
| Respuesta | La UI responde a los clics del usuario sin bloquearse; la búsqueda en curso sigue mostrando su progreso sin interferir con la interacción |
| Medida de respuesta | Tiempo de respuesta de la UI ≤ 200 ms en el percentil 95 durante una búsqueda concurrente en background |

**Escenario 3 — entorno degradado (10 usuarios concurrentes lanzando búsquedas)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Varios investigadores/as (uso pico del laboratorio) |
| Estímulo | 10 usuarios lanzan búsquedas simultáneamente contra el mismo servidor de LocalBlast |
| Entorno | Degradado — carga cercana al máximo esperado para el contexto de un laboratorio |
| Artefacto | Servidor de LocalBlast + cola de búsquedas |
| Respuesta | El sistema encola las búsquedas y confirma la recepción a cada usuario en un tiempo acotado, aunque la ejecución efectiva se difiera |
| Medida de respuesta | 0% de solicitudes rechazadas o perdidas con hasta 10 búsquedas concurrentes; tiempo de confirmación de encolado ≤ 3 segundos en el percentil 95 |

---

## 5. Trazabilidad hacia los procesos y RFs

La tabla muestra, para cada atributo, qué **procesos** y **requerimientos funcionales** del SRS son los principales artefactos sobre los que se apoyan sus escenarios de calidad. No es una relación exhaustiva de todos los RFs tocados, sino los más representativos por escenario.

| Atributo | Procesos afectados | RFs principales |
|---|---|---|
| Interoperabilidad | P1 (invocación a BLAST+, local y remoto) | RF-03, RF-04, RF-05, RF-08 |
| Usabilidad | P1 (carga y configuración), P2 (filtrado interactivo) | RF-01, RF-06, RF-11 |
| Integridad | P1 (persistencia en D2 al final de CU005) | RF-10 |
| Confiabilidad | P1 (ejecución asíncrona con cancelación y validaciones) | RF-02, RF-07, RF-08, RF-12 |
| Performance | P1 (overhead del pipeline), P2 (filtros post-búsqueda) | RF-08, RF-11 |

---

*Los cinco atributos elegidos y sus quince escenarios (5 × 3 entornos) forman la especificación no funcional del SRS para el TP1. En TPs posteriores, estos escenarios funcionan como criterios de aceptación de las decisiones de arquitectura (TP3), de diseño (TP4) y como base para las pruebas no funcionales (TP5).*
