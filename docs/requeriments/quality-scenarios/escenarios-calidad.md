# Escenarios de Atributo de Calidad — LocalBlast

Este documento contiene la selección, priorización y especificación de los atributos de calidad críticos para **LocalBlast**, junto con sus escenarios de calidad (seis componentes cada uno). Es parte del TP2 — Parte A y se apoya en los artefactos del TP1 (SRS, casos de uso e historias de usuario) para dar contexto a cada escenario.

**Taxonomía utilizada.** Las subcaracterísticas se toman del modelo de calidad del producto de la **ISO/IEC 25010:2023** (ver Anexo A de la guía del TP2). Para cada atributo elegido se declara explícitamente la característica y subcaracterística correspondientes.

---

## Índice

1. [Metodología](#1-metodología)
2. [Filtrado inicial de atributos](#2-filtrado-inicial-de-atributos)
3. [Matriz de priorización](#3-matriz-de-priorización)
4. [Resultados y atributos seleccionados](#4-resultados-y-atributos-seleccionados)
5. [Escenarios de calidad](#5-escenarios-de-calidad)
   - 5.1 [Interoperabilidad](#51-interoperabilidad-compatibilidad)
   - 5.2 [Operabilidad](#52-operabilidad-capacidad-de-interacción)
   - 5.3 [Tolerancia a fallos](#53-tolerancia-a-fallos-fiabilidad)
   - 5.4 [Protección frente a errores del usuario](#54-protección-frente-a-errores-del-usuario-capacidad-de-interacción)
   - 5.5 [Comportamiento temporal](#55-comportamiento-temporal-eficiencia-de-desempeño)

---

## 1. Metodología

Aplicamos el método de priorización por matriz comparativa visto en clase, con los siguientes pasos:

1. **Filtrado inicial.** Partimos del catálogo completo de subcaracterísticas de la ISO/IEC 25010:2023 y descartamos las que no aportan valor significativo al tipo de sistema que estamos desarrollando (una GUI web para BLAST+, de ámbito de un laboratorio, con pocos usuarios concurrentes y alcance acotado al TP1). Quedamos con **diez atributos candidatos**.
2. **Comparación por pares.** Construimos una matriz triangular 10×10 donde comparamos cada atributo con cada uno de los otros, respondiendo la pregunta: *¿cuál es más crítico para LocalBlast?*. Usamos la notación `^` / `<` descrita en la sección 3.
3. **Conteo y umbral.** Para cada atributo contamos cuántas veces resultó ganador en las comparaciones. Fijamos un umbral de **5 victorias** y nos quedamos con los **cinco atributos** por encima de ese umbral.
4. **Especificación de escenarios.** Para cada atributo elegido redactamos **tres escenarios** (entorno normal, de sobrecarga y degradado) con los seis componentes de la plantilla ISO: fuente del estímulo, estímulo, artefacto, entorno, respuesta y medida de la respuesta.

Priorizamos escenarios en entornos de sobrecarga y degradados por sobre el camino normal, siguiendo la indicación de la guía del TP2 (sección 3.1).

---

## 2. Filtrado inicial de atributos

### 2.1 Atributos descartados

La ISO/IEC 25010:2023 define ocho características con sus subcaracterísticas (unas 30 en total). Para LocalBlast descartamos las siguientes antes de la matriz comparativa, porque **no aportan valor significativo al alcance definido del proyecto**:

| Subcaracterística | Motivo del descarte |
|---|---|
| **Completitud / Corrección / Pertinencia funcional** (Adecuación funcional) | Son requerimientos de "correctitud funcional" que ya quedan cubiertos por los RF y los CU del TP1. No se tratan como atributos no funcionales a especificar aparte. |
| **Utilización de recursos** (Eficiencia de desempeño) | El cuello de botella real de performance es BLAST+ (externo), no nuestro código. No tenemos una restricción fuerte de CPU/RAM/disco impuesta por el laboratorio. |
| **Capacidad** (Eficiencia de desempeño) | El laboratorio tiene pocos usuarios concurrentes (≤5-10). Los límites máximos no son el driver de arquitectura. |
| **Ausencia de fallos** (Fiabilidad) | Queda cubierta implícitamente por tolerancia a fallos y por la validación semántica (que están en la lista corta). |
| **No repudio** (Seguridad) | Típico de dominios financiero/legal. No hay requerimiento del laboratorio de poder probar que un investigador lanzó cierta búsqueda. |
| **Responsabilidad / accountability** (Seguridad) | Mismo motivo que no repudio. El historial sirve al usuario, no como mecanismo de auditoría formal. |
| **Resistencia** (Seguridad) | Pensada para sistemas bajo ataque sostenido. LocalBlast es un sistema interno de laboratorio sin exposición pública relevante. |
| **Reconocibilidad de la adecuación** (Capacidad de interacción) | Más propio de productos de catálogo público, no de una herramienta de laboratorio con usuarios conocidos. |
| **Capacidad de aprendizaje** (Capacidad de interacción) | Importante, pero queda subsumida por *Operabilidad* en nuestro caso (los usuarios ya conocen BLAST; lo que hay que aprender es la UI). |
| **Compromiso del usuario** (Capacidad de interacción) | Pensada para productos de consumo. Los investigadores no vuelven a LocalBlast por "engagement" sino para hacer su trabajo. |
| **Inclusividad / Asistencia al usuario / Autodescriptividad** (Capacidad de interacción) | Importantes en general; no son los drivers principales para una herramienta interna de laboratorio con usuarios con perfil técnico. |
| **Coexistencia** (Compatibilidad) | LocalBlast corre en un servidor dedicado del laboratorio. No convive con otros sistemas que compitan por sus recursos. |
| **Modularidad / Reusabilidad / Analizabilidad / Modificabilidad / Testabilidad** (Mantenibilidad) | Importantes para el equipo, pero no son requerimientos exigidos por el usuario final ni condicionan la arquitectura del producto en el alcance del TP1. Se cubren por buenas prácticas internas. |
| **Adaptabilidad / Instalabilidad / Reemplazabilidad** (Flexibilidad) | El entorno de despliegue está definido (servidor del laboratorio, BLAST+ instalado). No hay requerimiento de portabilidad entre entornos ni de reemplazo. |

### 2.2 Atributos candidatos para la matriz de priorización

Quedan diez atributos para comparar entre sí:

| # | Abrev. | Subcaracterística | Característica (ISO 25010:2023) |
|---|---|---|---|
| 1 | **CT** | Comportamiento temporal | Eficiencia de desempeño |
| 2 | **CA** | Capacidad[^1] | Eficiencia de desempeño |
| 3 | **DI** | Disponibilidad | Fiabilidad |
| 4 | **TF** | Tolerancia a fallos | Fiabilidad |
| 5 | **CR** | Capacidad de recuperación | Fiabilidad |
| 6 | **CO** | Confidencialidad | Seguridad |
| 7 | **AU** | Autenticidad | Seguridad |
| 8 | **OP** | Operabilidad | Capacidad de interacción |
| 9 | **PE** | Protección frente a errores del usuario | Capacidad de interacción |
| 10 | **IN** | Interoperabilidad | Compatibilidad |

[^1]: Dejamos *Capacidad* dentro de la matriz (en lugar de descartarla directamente como el resto de "Eficiencia de desempeño") porque queríamos que la propia comparación por pares confirmara, o refutara, nuestra intuición inicial de que no es crítica para este alcance. El resultado del conteo lo validó: terminó en el último lugar.

---

## 3. Matriz de priorización

**Convención.** En cada celda `(fila, columna)` se compara el atributo de la fila contra el atributo de la columna:

- `^` indica que **el atributo de la columna es más crítico** para LocalBlast.
- `<` indica que **el atributo de la fila es más crítico** para LocalBlast.
- La diagonal queda vacía (no se compara un atributo consigo mismo).
- Solo se completa el **triángulo superior** (la matriz es antisimétrica).

El puntaje final de cada atributo es la cantidad de comparaciones en que resultó ganador: se cuentan los `<` de su fila más los `^` de su columna (en las filas que están por encima de la diagonal).

### 3.1 Grilla comparativa 10×10

| | CT | CA | DI | TF | CR | CO | AU | OP | PE | IN | **Puntaje** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **CT** | — | `<` | `<` | `^` | `<` | `<` | `<` | `^` | `^` | `^` | **5** |
| **CA** |   | — | `^` | `^` | `^` | `^` | `^` | `^` | `^` | `^` | **0** |
| **DI** |   |   | — | `^` | `<` | `<` | `<` | `^` | `^` | `^` | **4** |
| **TF** |   |   |   | — | `<` | `<` | `<` | `^` | `<` | `^` | **7** |
| **CR** |   |   |   |   | — | `<` | `<` | `^` | `^` | `^` | **3** |
| **CO** |   |   |   |   |   | — | `<` | `^` | `^` | `^` | **2** |
| **AU** |   |   |   |   |   |   | — | `^` | `^` | `^` | **1** |
| **OP** |   |   |   |   |   |   |   | — | `<` | `^` | **8** |
| **PE** |   |   |   |   |   |   |   |   | — | `^` | **6** |
| **IN** |   |   |   |   |   |   |   |   |   | — | **9** |

**Verificación.** Suma total de puntajes = 5 + 0 + 4 + 7 + 3 + 2 + 1 + 8 + 6 + 9 = **45**, que coincide con la cantidad total de comparaciones C(10,2) = 10·9/2 = 45. ✓

### 3.2 Justificación de las comparaciones clave

Se registra la justificación de las comparaciones que determinaron el top 5. El resto siguen la misma lógica (importancia relativa en el alcance del proyecto).

- **CT vs IN (gana IN).** Sin invocar correctamente a BLAST+ no hay producto, por más rápida que sea la UI. La interoperabilidad es *condición necesaria*; el buen tiempo de respuesta sobre un sistema que no funciona no vale.
- **OP vs IN (gana IN).** Mismo argumento: una interfaz excelente sobre un motor que no responde no tiene valor.
- **CT vs OP (gana OP).** La propuesta de valor completa de LocalBlast es "bajar la barrera de entrada frente a la línea de comandos de BLAST+". Si la UI es rápida pero el investigador no la entiende, vuelve a la terminal.
- **CT vs TF (gana TF).** Un timeout de NCBI que no se maneja arruina una búsqueda que puede haber tardado minutos. La velocidad de la UI es importante, pero la tolerancia a fallos protege el trabajo del usuario.
- **CT vs PE (gana PE).** La validación semántica previa a ejecutar BLAST+ (RF-02, RF-05, RF-07) existe precisamente porque una búsqueda mal configurada desperdicia tiempo de cómputo caro, local o remoto. Prevenir el error vale más que correr rápido.
- **TF vs PE (gana TF).** Ambos son defensivos, pero los fallos externos (BLAST+/NCBI) son más frecuentes e impredecibles que las malas configuraciones del usuario, que ya quedan filtradas por la validación semántica.
- **OP vs TF (gana OP).** Si BLAST+ falla el investigador reintenta; si la UI es incomprensible, abandona el producto. OP es más foundational para el *valor entregado*.
- **IN vs todo el resto (gana IN).** Siempre. LocalBlast es, por definición, una GUI para BLAST+: la interoperabilidad con BLAST+ es la razón de ser del sistema.

---

## 4. Resultados y atributos seleccionados

### 4.1 Ranking

Umbral elegido: **5 victorias**. Quedan los cinco atributos que superan ese umbral.

| Posición | Atributo | Subcaracterística | Puntaje | ¿Seleccionado? |
|:---:|---|---|:---:|:---:|
| 1 | IN | Interoperabilidad | 9 | ✅ |
| 2 | OP | Operabilidad | 8 | ✅ |
| 3 | TF | Tolerancia a fallos | 7 | ✅ |
| 4 | PE | Protección frente a errores del usuario | 6 | ✅ |
| 5 | CT | Comportamiento temporal | 5 | ✅ |
| 6 | DI | Disponibilidad | 4 | ❌ |
| 7 | CR | Capacidad de recuperación | 3 | ❌ |
| 8 | CO | Confidencialidad | 2 | ❌ |
| 9 | AU | Autenticidad | 1 | ❌ |
| 10 | CA | Capacidad | 0 | ❌ |

### 4.2 Síntesis de por qué estos cinco y no los otros

Los cinco atributos seleccionados forman un conjunto coherente con la naturaleza del proyecto:

- **Interoperabilidad** y **Tolerancia a fallos** cubren la relación con el actor externo más crítico (BLAST+ y, a través suyo, NCBI). Sin estas dos, el núcleo del sistema no es confiable.
- **Operabilidad** y **Protección frente a errores del usuario** cubren la relación con el actor humano principal (Investigador/a). Son la propuesta de valor del producto frente a la alternativa de usar BLAST+ por línea de comandos.
- **Comportamiento temporal** cubre lo que podríamos llamar "el nervio de la UI": la ejecución asíncrona (RF-08), el filtrado interactivo sin re-ejecutar BLAST (RF-11) y la respuesta general de la interfaz.

Los que quedaron afuera no son despreciables, pero son de **menor prioridad relativa**: la disponibilidad y la recuperación importan, pero el laboratorio no exige 24/7 y el peor caso tolera reintentos; confidencialidad y autenticidad están cubiertas por la autenticación básica declarada en el alcance (SRS §1.3) y no requieren un atributo de calidad sofisticado adicional; y capacidad simplemente no es un driver con los volúmenes esperados (≤5-10 investigadores concurrentes).

---

## 5. Escenarios de calidad

Para cada uno de los cinco atributos seleccionados se definen **tres escenarios** cubriendo distintas condiciones de entorno (normal, sobrecarga, degradado), con los seis componentes de la plantilla ISO.

---

### 5.1 Interoperabilidad (Compatibilidad)

**Justificación de criticidad del atributo.** LocalBlast *es*, por definición, una GUI para BLAST+. Toda ejecución (RF-03, RF-04, RF-05, RF-08) termina siendo una invocación a BLAST+ con los argumentos adecuados y un parseo de su salida. La interoperabilidad con este sistema externo es condición de existencia del producto, y es el único atributo que se mantuvo invicto en la matriz comparativa (9/9 victorias).

**Escenario 1 — entorno normal**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Lanza una búsqueda remota con `blastp` sobre la base de datos `nr` |
| Entorno | Normal — NCBI responde en tiempo esperado, versión de BLAST+ soportada |
| Artefacto | Módulo de ejecución asíncrona (`CU004`) + invocación a BLAST+ con flag `-remote` |
| Respuesta | El sistema arma la línea de comandos de BLAST+ con los parámetros validados en `CU003`, invoca al binario como subproceso, recibe la salida estándar al terminar, la parsea y dispara `CU005` para presentar y persistir los resultados |
| Medida de la respuesta | 100% de los campos requeridos por RF-09 (identificador del hit, score, E-value, % identidad, % cobertura) se parsean correctamente y se muestran en la tabla |

*Criticidad:* es el camino feliz del producto; sin cumplirse en condiciones normales no hay sistema. Se incluye como baseline.

**Escenario 2 — entorno de sobrecarga**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Varios investigadores del mismo laboratorio |
| Estímulo | Lanzan hasta 5 búsquedas concurrentes (mezcla de locales y remotas) desde la misma instancia del sistema |
| Entorno | Sobrecarga — 5 invocaciones concurrentes a BLAST+ sobre el mismo servidor |
| Artefacto | Módulo de ejecución asíncrona (`CU004`) y gestión de subprocesos de BLAST+ |
| Respuesta | El sistema invoca cada búsqueda como un subproceso independiente de BLAST+, con su propio contexto de ejecución; mantiene la asociación entre cada subproceso y la búsqueda del investigador que lo originó, y entrega los resultados a la sesión correcta |
| Medida de la respuesta | 0 cruces de resultados entre búsquedas concurrentes (verificable comparando el hash de resultado esperado por búsqueda con el persistido en D2) con hasta 5 búsquedas simultáneas |

*Criticidad:* un cruce de resultados entre investigadores sería un error silencioso catastrófico — el investigador vería alineamientos ajenos sin saberlo. Es un escenario de concurrencia típico en un laboratorio al final del día.

**Escenario 3 — entorno degradado**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | BLAST+ (sistema externo) |
| Estímulo | Devuelve una salida con cambios menores respecto a la versión soportada (por ejemplo, una columna adicional en `-outfmt 6` o un campo nuevo en el XML tras una actualización menor de BLAST+) |
| Entorno | Degradado — versión de BLAST+ posterior a la validada, no coordinada con el equipo de LocalBlast |
| Artefacto | Parser de salida de BLAST+ dentro del módulo de ejecución (`CU004`) |
| Respuesta | El parser reconoce los campos conocidos y los lee correctamente; detecta la presencia de campos adicionales no mapeados y los ignora sin corromper los campos conocidos, sin abortar la ejecución y sin impedir la presentación en `CU005`; registra una advertencia en el log del sistema para que el equipo pueda actualizar el parser |
| Medida de la respuesta | 100% de las búsquedas con salida de formato "casi conocido" (columnas adicionales no esperadas, campos XML nuevos) completan `CU005` correctamente con los campos de RF-09 intactos; 100% de esos casos quedan registrados en el log con la advertencia correspondiente |

*Criticidad:* BLAST+ es externo, se actualiza en el servidor del laboratorio por decisión del administrador de sistemas, y una actualización menor no debería romper nuestro sistema. Es un escenario realista y recurrente en sistemas que envuelven herramientas que no controlan.

---

### 5.2 Operabilidad (Capacidad de interacción)

**Justificación de criticidad del atributo.** La propuesta de valor explícita de LocalBlast frente a la línea de comandos de BLAST+ y frente a la interfaz pesada de NCBI es **"ágil e intuitiva"** (ver canvas de descubrimiento en el README). Si la operabilidad falla, el investigador vuelve a `blastp` en la terminal y el producto pierde su razón de ser. Es el segundo atributo con más victorias en la matriz (8/9).

**Escenario 1 — entorno normal**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a familiarizado con BLAST pero no con la línea de comandos |
| Estímulo | Configura y lanza su primera búsqueda remota con `blastp` sobre `nr`, aceptando los valores por defecto de los parámetros pre-búsqueda |
| Entorno | Normal — primera sesión del investigador tras una introducción breve a la interfaz |
| Artefacto | Formulario de carga (`CU001`), configuración (`CU002`), validación (`CU003`) y ejecución (`CU004`) |
| Respuesta | El investigador completa los cuatro pasos (cargar la secuencia, elegir modo/BD/programa, aceptar los parámetros por defecto, validar y ejecutar) usando solo lo que la interfaz le ofrece, sin consultar documentación externa |
| Medida de la respuesta | El investigador llega a disparar `CU004` en menos de **2 minutos** desde que entra a la interfaz, sin abrir la documentación de BLAST+ ni pedir ayuda a un par |

*Criticidad:* mide directamente la propuesta de valor "bajar la barrera de entrada frente a la terminal". Si este escenario no se cumple, el sistema no justifica su existencia frente a la alternativa de usar BLAST+ por consola.

**Escenario 2 — entorno de sobrecarga**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a trabajando con una búsqueda de muchos resultados |
| Estímulo | Aplica cuatro filtros post-búsqueda sucesivos (umbral de identidad, umbral de cobertura, umbral de E-value, filtro taxonómico) sobre una tabla con más de 500 hits, ajustando los umbrales varias veces para explorar el conjunto |
| Entorno | Sobrecarga — tabla con 500+ filas y ritmo rápido de ajuste de filtros (varios cambios por minuto) |
| Artefacto | Módulo de filtros post-búsqueda (`CU006`) e interfaz de la tabla de resultados |
| Respuesta | Cada ajuste de filtro refresca la tabla de forma visible, los filtros aplicados quedan mostrados y editables, y el usuario puede combinarlos, aflojarlos o quitarlos en cualquier orden sin tener que empezar de nuevo |
| Medida de la respuesta | Cada actualización de la tabla ante un cambio de filtro se refleja en menos de **1 segundo** con tablas de hasta 500 hits; el estado de los filtros aplicados queda siempre visible y editable mientras dure la sesión |

*Criticidad:* el filtrado interactivo post-búsqueda es una de las dos capacidades que diferencian a LocalBlast de la interfaz web de NCBI (ver propuesta de valor en el SRS §1.2). Si no responde ágilmente en escenarios con muchos hits —que son los más interesantes desde el punto de vista biológico— el investigador vuelve a Excel o a parsear la salida tabular a mano.

**Escenario 3 — entorno degradado**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Modifica un campo del formulario (por ejemplo, cambia el programa de `blastp` a `blastx`) **después** de que la configuración ya había sido validada por `CU003` |
| Entorno | Degradado — el usuario altera una configuración ya marcada como ejecutable, lo que podría llevarlo a lanzar una búsqueda incoherente si el sistema no reacciona |
| Artefacto | Formulario de configuración (`CU002`) y estado de validación (`CU003`, slice `CU003_B` CA-02) |
| Respuesta | El sistema invalida inmediatamente la marca "válida y lista para ejecutar", deshabilita visualmente el botón "Ejecutar búsqueda" y lo señala en la interfaz para que el investigador perciba el cambio sin necesidad de leer un mensaje de texto; preserva todos los valores del formulario para que el investigador no tenga que recargarlos |
| Medida de la respuesta | 100% de los cambios en campos relevantes del formulario (modo, BD, programa, parámetros pre-búsqueda) post-validación disparan la invalidación y deshabilitación en menos de **500 ms**; en 0% de los casos el investigador puede llegar a `CU004` sobre una configuración modificada sin re-validar |

*Criticidad:* evita que el investigador, por inercia visual, lance una búsqueda con una configuración que ya no coincide con lo que validó. Es una protección activa de la operabilidad que no requiere intervención consciente del usuario. Está trazado al criterio CA-02 de `HU05_CU003_B`.

---

### 5.3 Tolerancia a fallos (Fiabilidad)

**Justificación de criticidad del atributo.** LocalBlast depende de dos sistemas externos sobre los que no tiene control: **BLAST+** (local) y **NCBI** (remoto, a través de BLAST+). Los fallos remotos (timeouts, rate limits, errores explícitos de NCBI) están explícitamente contemplados en los casos de uso de ejecución (`CU004_E1`, `HU10_CU004_E1`) porque son frecuentes y previsibles. La tolerancia a fallos protege el trabajo del investigador cuando el entorno externo se degrada.

**Escenario 1 — entorno normal**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | BLAST+ (en modo remoto) |
| Estímulo | Devuelve resultados válidos tras una búsqueda remota exitosa |
| Entorno | Normal — conexión estable, NCBI operativo, sin fallos durante la ejecución |
| Artefacto | Módulo de ejecución asíncrona (`CU004_B`) + persistencia en D2 (`CU005_B`) |
| Respuesta | El sistema recibe los resultados, los deja disponibles en memoria, dispara `CU005` para presentarlos y los persiste automáticamente en D2 con parámetros, BD y timestamp |
| Medida de la respuesta | 100% de las búsquedas que terminan exitosamente en BLAST+ disparan `CU005` y quedan persistidas en D2 sin pérdida de resultados |

*Criticidad:* baseline del flujo exitoso; no es el escenario que exige diseño defensivo, pero sirve de referencia para los dos siguientes.

**Escenario 2 — entorno de sobrecarga**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | NCBI (a través de BLAST+ en modo remoto) |
| Estímulo | Devuelve un error de **rate limit** después de que varios investigadores del laboratorio lanzaron búsquedas remotas en rápida sucesión |
| Entorno | Sobrecarga — múltiples investigadores usan modo remoto simultáneamente, excediendo las políticas de uso de NCBI |
| Artefacto | Módulo de ejecución asíncrona (`CU004_E1`) y manejo del canal de error de BLAST+ |
| Respuesta | Para la(s) búsqueda(s) rechazadas: el sistema corta el flujo de `CU004`, **no dispara `CU005`**, **no persiste nada en D2** y muestra al investigador afectado el mensaje literal de error de BLAST+ (incluyendo el texto original de NCBI). Para las búsquedas de **otros** investigadores en curso: no se ven afectadas, siguen su ejecución normal |
| Medida de la respuesta | 100% de los errores de rate limit se muestran al investigador correspondiente dentro de los **3 segundos** de ser recibidos; 0 búsquedas de otros investigadores interrumpidas o alteradas por el error ajeno |

*Criticidad:* los rate limits de NCBI son uno de los modos de fallo más comunes de BLAST remoto. Protege dos cosas a la vez: honestidad hacia el investigador afectado (no inventar un error "amigable", mostrar el motivo real), y aislamiento entre sesiones concurrentes. Está trazado al criterio CA-02 de `HU10_CU004_E1`.

**Escenario 3 — entorno degradado**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Red / infraestructura externa entre BLAST+ y NCBI |
| Estímulo | Se produce un **timeout** de comunicación con NCBI durante una búsqueda remota ya en curso |
| Artefacto | Módulo de ejecución (`CU004_E1`) + manejo de errores de BLAST+ |
| Entorno | Degradado — fallo intermitente de conectividad, BLAST+ reporta el timeout tras no recibir respuesta en el plazo esperado |
| Respuesta | El sistema detecta el timeout informado por BLAST+, corta el flujo de `CU004`, no dispara `CU005`, no persiste nada en D2, muestra un mensaje que **distingue explícitamente** un timeout de conexión remota de un problema de parámetros de la búsqueda, y deja la interfaz en estado "configuración ejecutable" (sin perder los valores del formulario) para que el investigador pueda relanzar la búsqueda sin reconfigurar |
| Medida de la respuesta | 100% de los timeouts remotos se identifican y comunican como tales (no como "error de configuración" ni como "error genérico") dentro de los **60 segundos** del evento; en 100% de los casos la configuración validada se preserva en la interfaz |

*Criticidad:* la peor experiencia posible es que una búsqueda remota tarde 10 minutos, falle por red, y el investigador tenga que volver a cargar la secuencia y configurar todo desde cero. Preservar la configuración y comunicar bien el motivo del fallo es lo que diferencia una herramienta profesional de una frágil. Trazado al criterio CA-01 de `HU10_CU004_E1`.

---

### 5.4 Protección frente a errores del usuario (Capacidad de interacción)

**Justificación de criticidad del atributo.** El sistema tiene **tres niveles de validación** antes de invocar a BLAST+: sintáctica de la secuencia (`CU001_E1`, RF-02), compatibilidad de programa/query/BD (`CU003_E2`, RF-05 + RF-07) y rangos de parámetros (`CU003_E1`, RF-06 + RF-07). No es una decoración: las búsquedas BLAST, especialmente las remotas, son costosas y un error de configuración no detectado puede traducirse en varios minutos de cómputo perdidos y, en caso remoto, en consumo contra la cuota de uso de NCBI del laboratorio.

**Escenario 1 — entorno normal**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Carga un archivo FASTA bien formado con una secuencia única de proteína |
| Entorno | Normal — archivo válido, un único registro, dentro de los límites esperados |
| Artefacto | Módulo de carga y validación sintáctica (`CU001_B`) |
| Respuesta | El sistema acepta la secuencia, infiere "proteína" como alfabeto a partir de los caracteres observados, habilita los controles de `CU002` y deja la secuencia disponible para una o varias búsquedas sin tener que recargarla |
| Medida de la respuesta | 100% de los archivos FASTA bien formados se aceptan con el alfabeto correcto en menos de **2 segundos** |

*Criticidad:* baseline; no es el escenario desafiante pero es la referencia para los dos siguientes.

**Escenario 2 — entorno de sobrecarga**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Pega como query un texto largo (más de 100.000 caracteres) con **muchos** caracteres fuera del alfabeto biológico (por ejemplo, un fragmento de un documento Word pegado por error) |
| Entorno | Sobrecarga — alta cantidad de errores sintácticos a reportar |
| Artefacto | Validador sintáctico (`CU001_E1`) |
| Respuesta | El sistema no marca la secuencia como cargada, no habilita `CU002` y muestra un mensaje que señala la **primera** ocurrencia de carácter inválido con su posición exacta, sin saturar la UI con miles de mensajes ni ralentizarse al punto de bloquear al usuario |
| Medida de la respuesta | El mensaje de error aparece en menos de **3 segundos** aun con queries de hasta 100.000 caracteres; nunca se muestran más de **5** errores sintácticos simultáneamente en la interfaz |

*Criticidad:* el pegado accidental de contenido no biológico es un error de usuario frecuente. El sistema debe degradar el reporte de errores (no abrumar, no congelarse) sin dejar pasar la validación. Trazado al criterio CA-01 de `HU02_CU001_E1`.

**Escenario 3 — entorno degradado**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Intenta validar una configuración en la que el programa BLAST (`blastn`) es incompatible con el tipo de la secuencia cargada (proteína) y con la base de datos seleccionada (nucleótidos de una BD proteica) |
| Entorno | Degradado — combinación **semánticamente** inválida que ningún chequeo sintáctico aislado detectaría (cada pieza por separado es válida; es la combinación la que no lo es) |
| Artefacto | Módulo de validación semántica (`CU003_E2`) |
| Respuesta | El sistema no marca la búsqueda como válida, no habilita `CU004`, muestra qué combinaciones programa/tipo-de-query/tipo-de-BD **sí serían compatibles** con lo ya cargado y preserva la configuración del formulario para que el investigador pueda ajustarla puntualmente sin recargar la secuencia ni resetear los parámetros |
| Medida de la respuesta | 100% de las combinaciones programa/tipo-query/tipo-BD inválidas se bloquean en `CU003` acompañadas de al menos **una** sugerencia de combinación compatible; 0 búsquedas con combinación inválida llegan a invocar a BLAST+ |

*Criticidad:* este es el error más costoso que puede cometer un investigador — una búsqueda que BLAST+ puede llegar a ejecutar devolviendo cero hits "por diseño" en vez de "por error de configuración". Detectarlo *antes* de la invocación ahorra tiempo de cómputo y evita confundir al investigador con un resultado vacío ambiguo. Trazado a `HU07_CU003_E2`.

---

### 5.5 Comportamiento temporal (Eficiencia de desempeño)

**Justificación de criticidad del atributo.** Dos requerimientos explícitos del TP1 dependen de este atributo: **RF-08** (ejecución asíncrona con indicador de progreso, sin bloquear la UI) y **RF-11** (filtros post-búsqueda interactivos sin volver a correr BLAST). El comportamiento temporal no es "rápido por rápido": es la condición para que la UI *se sienta* responsiva mientras BLAST+ corre en segundo plano, lo cual es, junto con la operabilidad, lo que diferencia a LocalBlast de las alternativas.

**Escenario 1 — entorno normal**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Lanza una búsqueda local con `blastp` contra una base de datos del catálogo de ~50 MB |
| Entorno | Normal — una sola búsqueda en el servidor, sin concurrencia |
| Artefacto | Módulo de ejecución asíncrona (`CU004_B`) e interfaz |
| Respuesta | La interfaz muestra el indicador de progreso inmediatamente después del click en "Ejecutar búsqueda" y permanece navegable mientras BLAST+ corre; el investigador puede moverse por la aplicación sin que la ejecución se interrumpa |
| Medida de la respuesta | El indicador de progreso aparece en menos de **1 segundo** tras el click; la UI responde a eventos del usuario (navegación interna, cancelación) en menos de **500 ms** durante toda la ejecución |

*Criticidad:* materializa RF-08 en condiciones de referencia. Si no se cumple ni siquiera aquí, el resto no tiene sentido.

**Escenario 2 — entorno de sobrecarga**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Varios investigadores del mismo laboratorio |
| Estímulo | Lanzan hasta 5 búsquedas concurrentes desde distintas sesiones de la misma instancia del sistema |
| Entorno | Sobrecarga — 5 invocaciones concurrentes a BLAST+, cada una en su subproceso |
| Artefacto | Módulo de ejecución asíncrona (`CU004_B`) e interfaz web |
| Respuesta | Cada investigador ve el progreso de su propia búsqueda sin interferencia; la interfaz de cada sesión sigue respondiendo a eventos locales (navegación, cambio de filtros sobre búsquedas previas de esa sesión) sin latencias significativas |
| Medida de la respuesta | El tiempo de respuesta de la UI *por sesión* se mantiene por debajo de **1 segundo** con hasta 5 búsquedas concurrentes; 0 búsquedas abortadas por falta de respuesta del servidor |

*Criticidad:* corresponde al escenario típico de fin de jornada en el laboratorio, con varios investigadores lanzando búsquedas antes de irse. Si la UI se vuelve lenta en ese momento, la propuesta de valor "asíncrono + navegable" se cae.

**Escenario 3 — entorno degradado**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador/a |
| Estímulo | Aplica un filtro post-búsqueda sobre una tabla con **más de 1000 hits** (resultados crudos de un `blastn` remoto contra `nt`) |
| Entorno | Degradado — volumen alto de resultados en memoria del cliente; el investigador modifica rápidamente los umbrales explorando el conjunto |
| Artefacto | Módulo de filtros post-búsqueda (`CU006_B`), **sin** invocar nuevamente a BLAST+ |
| Respuesta | La tabla se recalcula sobre el conjunto crudo original (nunca sobre un resultado filtrado previo), mostrando el subconjunto que cumple los umbrales vigentes, sin bloquear la interfaz y sin disparar ninguna llamada adicional a BLAST+ |
| Medida de la respuesta | El re-filtrado se completa en menos de **1 segundo** para tablas de hasta 1000 hits; **0 invocaciones adicionales a BLAST+** por cada cambio de filtro (verificable por log/trace); la UI responde a nuevos cambios de filtro sin acumulación de latencia aun si el usuario encadena 10 cambios en 20 segundos |

*Criticidad:* RF-11 (y los criterios CA-01, CA-02, CA-03 de `HU12_CU006_B`) tiene una condición dura: **ningún** filtro post-búsqueda puede re-ejecutar BLAST, bajo ninguna circunstancia. Este escenario mide dos cosas a la vez: performance (responde rápido con muchos hits) y correctitud estructural (no cae en el antipatrón de "pedir de nuevo a BLAST para refrescar").

---

## Referencias

- [`srs.md`](../srs.md) — Especificación de Requerimientos de Software (TP1).
- [`casos-de-uso.md`](../casos-de-uso.md) — Casos de uso en formato Cockburn.
- [`historias-usuario.md`](../historias-usuario.md) — Historias de usuario con criterios Given-When-Then.
- [`../../uso-ia.md`](../../uso-ia.md) — Bitácora de uso de IA, con la entrada correspondiente al TP2 Parte A.
- Anexo A de la guía del TP2 (taxonomía de atributos de calidad ISO/IEC 25010:2023).
