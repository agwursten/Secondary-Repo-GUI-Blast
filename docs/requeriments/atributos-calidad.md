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

- **Seguridad** entra a la matriz como atributo genuino. Cubre autenticación básica del investigador (login/sesión — ver [SRS 1.3](srs.md#13-dentro-del-alcance)), confidencialidad del historial personal (cada investigador ve únicamente sus propias búsquedas en D2), cifrado en tránsito (HTTPS sobre datos que pueden ser propiedad intelectual del laboratorio) y advertencia al usuario cuando envía secuencias sensibles a NCBI en modo remoto. Lo que sí queda fuera del alcance es la gestión avanzada de usuarios (registro autoservicio, recuperación de contraseña por email, roles múltiples), no la seguridad en sí.
- **Disponibilidad** entra pese a que no hay SLA definido, para dejar que la matriz confirme o desmienta su baja prioridad de forma auditable, en vez de descartarla por intuición.

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
| **Performance**       |  —   |  ^  |  ^   |  ^  |  <   |  <  |  <  |    <    |  ^   |  ^   |  <  |   **5**   |
| **Escalabilidad**     |  <   |  —  |  <   |  <  |  <   |  <  |  <  |    <    |  <   |  <   |  <  |   **0**   |
| **Disponibilidad**    |  <   |  ^  |  —   |  ^  |  <   |  <  |  <  |    <    |  <   |  ^   |  <  |   **3**   |
| **Recuperación**      |  <   |  ^  |  <   |  —  |  <   |  <  |  <  |    <    |  <   |  <   |  <  |   **1**   |
| **Confiabilidad**     |  ^   |  ^  |  ^   |  ^  |  —   |  <  |  ^  |    <    |  ^   |  ^   |  <  |   **7**   |
| **Integridad**        |  ^   |  ^  |  ^   |  ^  |  ^   |  —  |  ^  |    <    |  ^   |  ^   |  <  |   **8**   |
| **Seguridad**         |  ^   |  ^  |  ^   |  ^  |  <   |  <  |  —  |    <    |  ^   |  ^   |  <  |   **6**   |
| **Interoperabilidad** |  ^   |  ^  |  ^   |  ^  |  ^   |  ^  |  ^  |    —    |  ^   |  ^   |  ^  |  **10**   |
| **Mantenibilidad**    |  <   |  ^  |  ^   |  ^  |  <   |  <  |  <  |    <    |  —   |  ^   |  <  |   **4**   |
| **Testeabilidad**     |  <   |  ^  |  <   |  ^  |  <   |  <  |  <  |    <    |  <   |  —   |  <  |   **2**   |
| **Usabilidad**        |  ^   |  ^  |  ^   |  ^  |  ^   |  ^  |  ^  |    <    |  ^   |  ^   |  —  |   **9**   |

Chequeo de consistencia: la matriz es **antisimétrica** (si `(i,j) = ^` entonces `(j,i) = <`) y la suma de victorias totaliza `C(11,2) = 55` (verificable: `5+0+3+1+7+8+6+10+4+2+9 = 55`).

### 2.2 Justificación de las comparaciones no obvias

Muchas comparaciones son directas, pero algunas ameritan justificación explícita — son las que el docente puede pedir defender en la presentación:

- **Interoperabilidad > todo lo demás (10 de 10).** Sin invocación correcta a BLAST+ el sistema **no funciona en absoluto** — no hay resultados que mostrar, ni interfaz que usar, ni datos que preservar íntegros ni proteger con autenticación. Es la dependencia externa dura sobre la que se apoya todo el valor de LocalBlast (ver `srs.md` sec. 8 y `contexto-inicial.md`). Por eso gana todas las comparaciones, incluso contra Usabilidad.

- **Usabilidad > Confiabilidad, Integridad y Seguridad.** Es una decisión discutida. La razón de ser del proyecto (según la [sección 1.1 del SRS](srs.md#11-problema)) es que ni la CLI de BLAST+ ni la web NCBI son suficientemente usables para el perfil objetivo. Si LocalBlast fuera perfectamente confiable, íntegro y seguro pero igual de duro de usar que la CLI, no aportaría valor sobre las alternativas existentes. Estos tres son baseline; Usabilidad es el diferenciador.

- **Integridad > Confiabilidad > Seguridad.** El orden entre los tres atributos "de fiabilidad extendida" quedó así porque: (a) la Integridad transaccional del historial es específica y crítica — un historial con datos mezclados o parciales es peor que un sistema temporalmente caído; (b) la Confiabilidad es una preocupación transversal del pipeline P1 (validaciones, tolerancia a fallos de BLAST+, ejecución asíncrona) que impacta a todos los usuarios por igual; (c) la Seguridad es genuinamente importante — cada investigador tiene datos que otros no deben ver — pero no rompe la operación del sistema al fallar de forma degradada (un problema de sesión no corrompe una búsqueda). El orden refleja "qué es peor si falla", no "qué es menos importante en absoluto".

- **Seguridad > Performance.** Éste fue el cambio más discutido. Para un investigador que tiene búsquedas de un proyecto no publicado (o secuencias del laboratorio con potencial de patentamiento), que otro usuario del sistema pueda ver su historial es un problema mayor que que el sistema tarde un poco más en responder. Además, la Seguridad es baseline: si falla la confidencialidad, el usuario deja de usar el sistema; si es un poco más lento, se queja pero sigue usándolo.

- **Performance > Mantenibilidad, Testeabilidad, Escalabilidad, Recuperación, Disponibilidad.** La performance percibida por el usuario (UI reactiva, overhead bajo) importa más que preocupaciones internas del equipo (mantenibilidad, testeabilidad) o que atributos sin driver claro en el dominio (escalabilidad de laboratorio, recuperación sin datos críticos, disponibilidad sin SLA).

- **Confiabilidad > Seguridad, pero Seguridad > Mantenibilidad y Testeabilidad.** La confiabilidad afecta todo el sistema; la seguridad afecta la relación de cada usuario con sus datos. Ambas son user-facing, pero la confiabilidad es más amplia. A su vez, Seguridad supera a Mantenibilidad y Testeabilidad porque estas dos son preocupaciones del equipo, no del usuario final.

- **Escalabilidad = 0 victorias.** Confirma que el dimensionamiento para un laboratorio no impone requisitos de escalabilidad significativos; lo que importa (varios usuarios concurrentes) se cubre como escenario de sobrecarga dentro de otros atributos.

### 2.3 Ranking final

Ordenando por cantidad de victorias, de mayor a menor:

| Ranking | Atributo | Victorias |
|:---:|---|:---:|
| 🥇 1 | **Interoperabilidad** | 10 |
| 🥈 2 | **Usabilidad** | 9 |
| 🥉 3 | **Integridad** | 8 |
| 4 | **Confiabilidad** | 7 |
| 5 | **Seguridad** | 6 |
| 6 | Performance | 5 |
| 7 | Mantenibilidad | 4 |
| 8 | Disponibilidad | 3 |
| 9 | Testeabilidad | 2 |
| 10 | Recuperación | 1 |
| 11 | Escalabilidad | 0 |

### 2.4 Selección del umbral

Siguiendo el método del PDF de la cátedra (que en su ejemplo usa un umbral para dejar los cinco atributos más relevantes), fijamos el **umbral en 6 victorias**. Los atributos con 6 o más victorias son los que consideramos críticos para el diseño de LocalBlast. Los que quedan por debajo — Performance, Mantenibilidad, Disponibilidad, Testeabilidad, Recuperación y Escalabilidad — siguen siendo preocupaciones legítimas del equipo, pero no motivan escenarios de calidad propios en este TP.

El umbral discrimina **seis atributos "afuera" y cinco "adentro"**: la matriz hace efectivamente el trabajo de selección, no un mero refinamiento del filtrado inicial.

Vale destacar el caso de **Performance**, que quedó apenas por debajo del umbral (5 victorias contra las 6 de Seguridad). Aspectos de rendimiento no se pierden del análisis: reaparecen como escenarios de sobrecarga dentro de otros atributos (la reactividad de la UI durante búsquedas concurrentes se cubre bajo Confiabilidad; el tiempo de aplicación de filtros post-búsqueda se cubre bajo Usabilidad). Es decir, Performance se manifiesta transversalmente en varios escenarios sin necesidad de una sección propia.

---

## 3. Los cinco atributos elegidos

De la priorización surgen los cinco atributos sobre los que redactamos escenarios detallados:

| # | Atributo | Categoría ISO 25010 | Sub-característica ISO 25010 |
|:---:|---|---|---|
| 1 | **Interoperabilidad** | Compatibilidad | Interoperabilidad |
| 2 | **Usabilidad** | Usabilidad | Operabilidad, Aprendizaje, Protección contra errores |
| 3 | **Integridad** | Fiabilidad | Integridad transaccional (variante de dominio) |
| 4 | **Confiabilidad** | Fiabilidad | Tolerancia a fallos |
| 5 | **Seguridad** | Seguridad | Autenticidad, Confidencialidad, Integridad de datos protegidos |

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

Es el atributo diferenciador de LocalBlast: la razón por la que el sistema existe es que la CLI y la web NCBI son duras de operar para el perfil objetivo. Los escenarios incorporan también aspectos de tiempo de respuesta percibido, ya que Performance quedó absorbida transversalmente en la especificación.

**Escenario 1 — entorno normal**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a nuevo en LocalBlast (habituado a la CLI de BLAST+ o a la web NCBI) |
| Estímulo | Ingresa por primera vez, se autentica y quiere correr una búsqueda `blastn` con valores por defecto |
| Entorno | Operación normal, primera sesión del usuario, sin capacitación previa ni documentación abierta |
| Artefacto | Interfaz gráfica (login + formulario de carga de secuencia y de configuración, CU001 + CU002) |
| Respuesta | El usuario logra completar una búsqueda end-to-end (login → cargar secuencia → configurar → ejecutar → ver resultados) sin consultar documentación externa |
| Medida de respuesta | 90% de los usuarios nuevos completan una búsqueda con valores por defecto en menos de 5 minutos desde la pantalla de login, medido con una prueba de usabilidad con al menos 5 participantes representativos del perfil |

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
| Respuesta | El sistema almacena la búsqueda completa (parámetros pre-búsqueda, base de datos, timestamp, resultados crudos, identificador del usuario que la lanzó) en D2 de forma atómica |
| Medida de respuesta | 100% de las búsquedas exitosas quedan en D2 con todos sus campos poblados; auditoría posterior no encuentra registros parciales |

**Escenario 2 — entorno de sobrecarga (escrituras concurrentes)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Varios investigadores/as |
| Estímulo | Cinco búsquedas terminan casi simultáneamente y se persisten en D2 en el mismo segundo |
| Entorno | Sobrecarga — escrituras concurrentes en el mismo almacén |
| Artefacto | Módulo de persistencia en D2 con acceso concurrente (CU005) |
| Respuesta | El sistema serializa las escrituras sin colisiones ni pérdidas; cada búsqueda queda con su identificador único, sus resultados correctamente asociados a sus parámetros, y con el identificador de su usuario propietario preservado |
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

Cubre el comportamiento del pipeline P1 completo ante variaciones de la carga y ante fallos de la dependencia externa (BLAST+). Absorbe conceptualmente lo que en el análisis inicial figuraba como Robustez. Los escenarios de sobrecarga incorporan aspectos de reactividad de la UI (originalmente pensados bajo Performance), ya que ese atributo quedó apenas por debajo del umbral.

**Escenario 1 — entorno normal**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Ejecuta una búsqueda con parámetros dentro de rangos habituales |
| Entorno | Operación normal, BLAST+ instalado, catálogo D1 poblado |
| Artefacto | Pipeline P1 completo (validación sintáctica → configuración → validación semántica → invocación → parseo de resultados → persistencia) |
| Respuesta | La búsqueda se completa exitosamente y los resultados se muestran al usuario |
| Medida de respuesta | Tasa de éxito ≥ 99% de las búsquedas lanzadas con parámetros válidos en condiciones normales |

**Escenario 2 — entorno de sobrecarga (secuencia query muy grande + UI reactiva)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Carga una secuencia query grande (por ejemplo, un cromosoma bacteriano completo, ~5 MB de nucleótidos) y ejecuta `blastn` contra una base de datos grande; mientras espera, navega la interfaz |
| Entorno | Sobrecarga — carga de trabajo cerca de los límites del servidor, UI concurrente con búsqueda en curso |
| Artefacto | Módulo de ejecución asíncrona con indicador de progreso (RF-08, CU004) + UI reactiva |
| Respuesta | El sistema muestra progreso, mantiene la UI responsiva mientras la búsqueda corre en background, no timeoutea prematuramente y, o bien devuelve resultados completos, o bien notifica al usuario un timeout controlado con opción de ajustar parámetros |
| Medida de respuesta | 0% de fallas silenciosas; 100% de las búsquedas largas terminan con resultados válidos o con una notificación explícita de timeout; tiempo de respuesta de la UI ≤ 200 ms en el percentil 95 durante la búsqueda en background |

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

### 4.5 Seguridad — Autenticidad, confidencialidad e integridad de datos protegidos

Cubre cuatro preocupaciones del dominio: (a) **autenticación** del investigador para que solo usuarios válidos entren al sistema; (b) **confidencialidad del historial personal** — cada investigador ve únicamente sus propias búsquedas en D2, dado que las secuencias query pueden ser propiedad intelectual del laboratorio o parte de proyectos aún no publicados; (c) **cifrado en tránsito** entre el navegador y el servidor de LocalBlast; (d) **advertencia informada** cuando el usuario está por enviar una secuencia sensible al motor remoto (BLAST+ en modo `-remote` la envía a NCBI). La seguridad se apoya en la autenticación básica declarada dentro del alcance ([SRS 1.3](srs.md#13-dentro-del-alcance)).

**Escenario 1 — entorno normal (autenticación y sesión)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Ingresa sus credenciales (usuario y contraseña) e inicia sesión para trabajar en el sistema |
| Entorno | Operación normal, primer acceso del día, credenciales previamente creadas por fuera del sistema |
| Artefacto | Módulo de autenticación / gestión de sesiones |
| Respuesta | El sistema valida las credenciales contra el almacén de usuarios, inicia una sesión con timeout configurado y expone al usuario únicamente su propio historial en D2; todas las comunicaciones cliente–servidor viajan cifradas (HTTPS) |
| Medida de respuesta | 100% de las sesiones exitosas solo dan acceso a los datos del usuario autenticado; 0% de accesos aceptados con credenciales inválidas; la sesión expira automáticamente tras 30 minutos de inactividad sin excepción; 100% del tráfico entre cliente y servidor viaja por TLS/HTTPS |

**Escenario 2 — entorno de sobrecarga (múltiples usuarios simultáneos con datos aislados)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Múltiples investigadores/as |
| Estímulo | 10 investigadores autenticados simultáneamente ejecutan búsquedas, consultan su historial y descargan resultados |
| Entorno | Sobrecarga — uso pico del laboratorio, cada usuario debe ver solo sus propios datos |
| Artefacto | Control de acceso a D2 (aislamiento del historial por usuario) y gestión concurrente de sesiones |
| Respuesta | El sistema separa correctamente las búsquedas de cada usuario; ningún investigador puede ver, descargar ni modificar el historial de otro; las sesiones concurrentes no interfieren entre sí (por ejemplo, un logout de A no afecta la sesión de B) |
| Medida de respuesta | 0% de casos en que un usuario acceda a búsquedas de otro; 100% de las consultas a D2 filtran automáticamente por el identificador del usuario autenticado, verificable por auditoría de las queries del backend |

**Escenario 3 — entorno degradado (intento de bypass o envío de secuencia sensible a NCBI)**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | (a) Cliente HTTP no autenticado intentando acceder directamente a un endpoint de la API, o (b) investigador/a autenticado/a que va a enviar una secuencia potencialmente sensible en modo remoto |
| Estímulo | (a) Se hace una request a `/api/history` o `/api/search` sin cookie de sesión válida, o (b) el investigador selecciona modo remoto para una búsqueda cuya secuencia query es un manuscrito no publicado |
| Entorno | Degradado — intento de bypass de autenticación, o transferencia de datos sensibles a un tercero (NCBI) |
| Artefacto | (a) Middleware de autenticación aplicado a todos los endpoints protegidos; (b) advertencia de privacidad en la pantalla de configuración cuando el modo es remoto |
| Respuesta | (a) El sistema rechaza la request con código 401 (no autenticado) o 403 (sin permiso), sin filtrar información del historial en el cuerpo del error; (b) el sistema muestra al usuario una advertencia clara antes de lanzar la búsqueda: `"En modo remoto tu secuencia se envía a los servidores de NCBI. Si es información confidencial o no publicada, considerá usar modo local"` y requiere confirmación explícita |
| Medida de respuesta | 100% de los endpoints protegidos rechazan requests sin sesión válida y no incluyen datos sensibles en la respuesta de error; 100% de las búsquedas remotas requieren un clic de confirmación posterior a la advertencia de privacidad, verificable en logs |

---

## 5. Trazabilidad hacia los procesos y RFs

La tabla muestra, para cada atributo, qué **procesos** y **requerimientos funcionales** del SRS son los principales artefactos sobre los que se apoyan sus escenarios de calidad. Seguridad no realiza un RF específico porque los aspectos funcionales relacionados (login, filtrado de historial por usuario) quedaron en el alcance sin RF profundizado en este SRS; los escenarios de calidad de Seguridad sirven, además, como especificación de las capacidades que ese diseño de autenticación deberá cumplir cuando se implemente.

| Atributo | Procesos afectados | RFs principales | Nota |
|---|---|---|---|
| Interoperabilidad | P1 (invocación a BLAST+, local y remoto) | RF-03, RF-04, RF-05, RF-08 | — |
| Usabilidad | P1 (carga y configuración), P2 (filtrado interactivo) | RF-01, RF-06, RF-11 | — |
| Integridad | P1 (persistencia en D2 al final de CU005) | RF-10 | — |
| Confiabilidad | P1 (ejecución asíncrona con cancelación y validaciones) | RF-02, RF-07, RF-08, RF-12 | Incorpora aspectos de reactividad de UI que originalmente pensamos bajo Performance |
| Seguridad | Transversal (todos los procesos) | — | No hay RFs específicos de autenticación en este SRS; los escenarios funcionan como especificación no funcional del comportamiento esperado |

---

*Los cinco atributos elegidos y sus quince escenarios (5 × 3 entornos) forman la especificación no funcional del SRS para el TP1. En TPs posteriores, estos escenarios funcionan como criterios de aceptación de las decisiones de arquitectura (TP3), de diseño (TP4) y como base para las pruebas no funcionales (TP5).*
