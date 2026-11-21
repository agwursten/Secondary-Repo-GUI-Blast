# Escenarios de Atributo de Calidad — LocalBlast

Este documento contiene la selección, priorización y especificación de los atributos de calidad críticos para **LocalBlast**, junto con sus escenarios de calidad (seis componentes cada uno). Es parte del TP2 — Parte A y se apoya en el proyecto del TP1 (visión, alcance y requerimientos) para dar contexto a cada escenario.

**Taxonomía utilizada.** Las subcaracterísticas se toman del modelo de calidad del producto de la **ISO/IEC 25010:2023** (ver Anexo A de la guía del TP2). Para cada atributo elegido se declara explícitamente la característica y la subcaracterística correspondientes.

---

## Índice

1. [Metodología](#1-metodología)
2. [Filtrado inicial de atributos](#2-filtrado-inicial-de-atributos)
3. [Matriz de priorización](#3-matriz-de-priorización)
4. [Resultados y atributos seleccionados](#4-resultados-y-atributos-seleccionados)
5. [Escenarios de calidad](#5-escenarios-de-calidad)
   - 5.1 [Interoperabilidad](#51-interoperabilidad)
   - 5.2 [Operabilidad](#52-operabilidad)
   - 5.3 [Confidencialidad](#53-confidencialidad)
   - 5.4 [Tolerancia a fallos](#54-tolerancia-a-fallos)
   - 5.5 [Modularidad](#55-modularidad)

---

## 1. Metodología

Aplicamos el método de priorización por matriz comparativa visto en clase, con los siguientes pasos:

1. **Filtrado inicial.** Partimos del catálogo completo de subcaracterísticas de la ISO/IEC 25010:2023 y descartamos las que no aportan valor significativo al tipo de sistema que estamos desarrollando (una interfaz gráfica web para BLAST+, de ámbito de un laboratorio, con pocos usuarios concurrentes, que opera sobre secuencias biológicas potencialmente sensibles, y que está pensada para evolucionar iterativamente). Quedamos con **diez atributos candidatos**.
2. **Comparación por pares.** Construimos una matriz triangular 10×10 donde comparamos cada atributo con cada uno de los otros, respondiendo la pregunta: *¿cuál es más crítico para LocalBlast?*. Usamos la notación `^` / `<` descrita en la sección 3.
3. **Conteo y umbral.** Para cada atributo contamos cuántas veces resultó ganador en las comparaciones. Fijamos un umbral de **5 victorias** y nos quedamos con los **cinco atributos** por encima de ese umbral.
4. **Especificación de escenarios.** Para cada atributo elegido redactamos **dos escenarios**, ambos en entornos de sobrecarga, degradados o significativos, con los seis componentes de la plantilla ISO: fuente del estímulo, estímulo, artefacto, entorno, respuesta y medida de la respuesta. Siguiendo la indicación de la guía del TP2 (sección 3.1), no incluimos escenarios en condición normal: los escenarios deben capturar las situaciones en las que el atributo realmente se pone en juego.

---

## 2. Filtrado inicial de atributos

### 2.1 Atributos descartados

La ISO/IEC 25010:2023 define ocho características con sus subcaracterísticas (unas 30 en total). Para LocalBlast descartamos las siguientes antes de la matriz comparativa, porque **no aportan valor significativo al alcance definido del proyecto**:

| Subcaracterística | Motivo del descarte |
|---|---|
| **Completitud / Corrección / Pertinencia funcional** (Adecuación funcional) | Son requerimientos de "correctitud funcional" que ya quedan cubiertos por los requerimientos funcionales del TP1. No se tratan como atributos no funcionales a especificar aparte. |
| **Utilización de recursos** (Eficiencia de desempeño) | El cuello de botella real de performance es BLAST+ (externo), no nuestro código. No tenemos una restricción fuerte de CPU/RAM/disco impuesta por el laboratorio. |
| **Capacidad** (Eficiencia de desempeño) | El laboratorio tiene pocos usuarios concurrentes (menos de diez). Los límites máximos no son el driver de arquitectura. |
| **Ausencia de fallos** (Fiabilidad) | Queda cubierta implícitamente por *Tolerancia a fallos* y por la validación semántica de la configuración antes de ejecutar BLAST+. |
| **No repudio** (Seguridad) | Típico de dominios financiero/legal. No hay requerimiento del laboratorio de poder probar formalmente que un investigador lanzó cierta búsqueda. |
| **Responsabilidad / accountability** (Seguridad) | Mismo motivo que no repudio. El historial sirve al usuario, no como mecanismo de auditoría formal. |
| **Resistencia** (Seguridad) | Pensada para sistemas bajo ataque sostenido. LocalBlast es un sistema interno de laboratorio, sin exposición pública relevante. |
| **Reconocibilidad de la adecuación** (Capacidad de interacción) | Más propia de productos de catálogo público, no de una herramienta interna cuyos usuarios ya conocen por qué la usan. |
| **Capacidad de aprendizaje** (Capacidad de interacción) | Importante, pero queda subsumida por *Operabilidad* en nuestro caso: los usuarios ya conocen BLAST; lo que hay que aprender es la interfaz. |
| **Compromiso del usuario** (Capacidad de interacción) | Pensada para productos de consumo. Los investigadores no vuelven a LocalBlast por "engagement", sino para hacer su trabajo. |
| **Inclusividad / Asistencia al usuario / Autodescriptividad** (Capacidad de interacción) | Importantes en general; no son los drivers principales para una herramienta interna de laboratorio con usuarios de perfil técnico. |
| **Coexistencia** (Compatibilidad) | LocalBlast corre en un servidor dedicado del laboratorio. No convive con otros sistemas que compitan por sus recursos. |
| **Reusabilidad / Analizabilidad / Capacidad de prueba** (Mantenibilidad) | Importantes para el equipo, pero quedan cubiertas por buenas prácticas internas; no son requerimientos exigidos por el usuario final ni condicionan la arquitectura al nivel que lo hace *Modularidad*. |
| **Modificabilidad** (Mantenibilidad) | Queda subsumida por *Modularidad*: la capacidad de modificar sin romper se materializa, en nuestro caso, a través de la separación en módulos independientes. |
| **Adaptabilidad / Instalabilidad / Reemplazabilidad** (Flexibilidad) | El entorno de despliegue está definido (servidor del laboratorio, BLAST+ instalado por el administrador de sistemas). No hay requerimiento de portabilidad entre entornos ni de reemplazo. |
| **Escalabilidad** (Flexibilidad) | El dimensionamiento es conocido (una decena de investigadores). Crecimientos mayores están fuera del horizonte del proyecto. |

### 2.2 Atributos candidatos para la matriz de priorización

Quedan diez atributos para comparar entre sí:

| # | Subcaracterística | Característica (ISO 25010:2023) |
|---|---|---|
| 1 | Comportamiento temporal | Eficiencia de desempeño |
| 2 | Disponibilidad | Fiabilidad |
| 3 | Tolerancia a fallos | Fiabilidad |
| 4 | Capacidad de recuperación | Fiabilidad |
| 5 | Confidencialidad | Seguridad |
| 6 | Autenticidad | Seguridad |
| 7 | Operabilidad | Capacidad de interacción |
| 8 | Protección frente a errores del usuario | Capacidad de interacción |
| 9 | Interoperabilidad | Compatibilidad |
| 10 | Modularidad | Mantenibilidad |

La numeración de este listado se mantiene como índice de referencia para la matriz comparativa de la sección siguiente, en la que las columnas se referencian por su número para que la tabla no quede excesivamente ancha.

---

## 3. Matriz de priorización

**Convención.** En cada celda `(fila, columna)` se compara el atributo de la fila contra el atributo de la columna:

- `^` indica que **el atributo de la columna es más crítico** para LocalBlast.
- `<` indica que **el atributo de la fila es más crítico** para LocalBlast.
- La diagonal queda vacía (no se compara un atributo consigo mismo).
- Solo se completa el **triángulo superior** (la matriz es antisimétrica).

El puntaje final de cada atributo es la cantidad de comparaciones en que resultó ganador: se cuentan los `<` de su fila más los `^` de su columna (en las filas que están por encima de la diagonal).

### 3.1 Grilla comparativa 10×10

Las filas llevan el nombre completo del atributo; las columnas se identifican con el número de orden del listado de la sección 2.2.

| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | **Puntaje** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1. Comportamiento temporal                         | — | `<` | `^` | `<` | `^` | `<` | `^` | `^` | `^` | `^` | **3** |
| 2. Disponibilidad                                  |   | — | `^` | `<` | `^` | `<` | `^` | `^` | `^` | `^` | **2** |
| 3. Tolerancia a fallos                             |   |   | — | `<` | `^` | `<` | `^` | `<` | `^` | `<` | **6** |
| 4. Capacidad de recuperación                       |   |   |   | — | `^` | `<` | `^` | `^` | `^` | `^` | **1** |
| 5. Confidencialidad                                |   |   |   |   | — | `<` | `^` | `<` | `^` | `<` | **7** |
| 6. Autenticidad                                    |   |   |   |   |   | — | `^` | `^` | `^` | `^` | **0** |
| 7. Operabilidad                                    |   |   |   |   |   |   | — | `<` | `^` | `<` | **8** |
| 8. Protección frente a errores del usuario         |   |   |   |   |   |   |   | — | `^` | `^` | **4** |
| 9. Interoperabilidad                               |   |   |   |   |   |   |   |   | — | `<` | **9** |
| 10. Modularidad                                    |   |   |   |   |   |   |   |   |   | — | **5** |

**Verificación.** Suma total de puntajes = 3 + 2 + 6 + 1 + 7 + 0 + 8 + 4 + 9 + 5 = **45**, que coincide con la cantidad total de comparaciones C(10,2) = 10·9/2 = 45. ✓


---

## 4. Resultados y atributos seleccionados

### 4.1 Ranking

Umbral elegido: **5 victorias**. Quedan los cinco atributos que superan ese umbral.

| Posición | Atributo (subcaracterística) | Puntaje | ¿Seleccionado? |
|:---:|---|:---:|:---:|
| 1 | Interoperabilidad | 9 | ✅ |
| 2 | Operabilidad | 8 | ✅ |
| 3 | Confidencialidad | 7 | ✅ |
| 4 | Tolerancia a fallos | 6 | ✅ |
| 5 | Modularidad | 5 | ✅ |
| 6 | Protección frente a errores del usuario | 4 | ❌ |
| 7 | Comportamiento temporal | 3 | ❌ |
| 8 | Disponibilidad | 2 | ❌ |
| 9 | Capacidad de recuperación | 1 | ❌ |
| 10 | Autenticidad | 0 | ❌ |

### 4.2 Síntesis de por qué estos cinco y no los otros

Los cinco atributos seleccionados cubren cuatro dimensiones distintas del sistema, todas críticas para LocalBlast:

- **Interoperabilidad** cubre la relación con el actor externo del que depende todo el sistema (BLAST+ y, a través suyo, NCBI). Sin ella no hay producto.
- **Operabilidad** cubre la relación con el actor humano principal (el investigador) y materializa la propuesta de valor frente a la línea de comandos.
- **Confidencialidad** cubre la protección de los datos sensibles que atraviesan el sistema. Las secuencias que un investigador puede cargar incluyen material biológico de origen humano, lo que las convierte en datos sensibles; la exposición de red (navegador ↔ servidor), el almacenamiento del historial y el acceso entre investigadores del mismo laboratorio son los tres frentes donde esta protección se juega.
- **Tolerancia a fallos** cubre la robustez ante los fallos externos previsibles (timeouts, rate limits, errores de NCBI reportados a través de BLAST+), que son frecuentes en el modo remoto.
- **Modularidad** cubre la evolución del sistema. El proyecto declara explícitamente un modelo de ciclo de vida incremental y deja fuera del alcance de este cuatrimestre el rol administrador, formatos adicionales y filtros adicionales, con la intención explícita de incorporarlos iterativamente. Un diseño no modular convierte esa intención en reescrituras.

Los que quedaron afuera no son irrelevantes, pero son de **menor prioridad relativa**: *Protección frente a errores del usuario* ya está ampliamente cubierta por los requerimientos funcionales de validación (sintáctica de la secuencia y semántica de la configuración); *Comportamiento temporal* importa pero queda subordinada a Operabilidad, que la contiene en términos de experiencia percibida; *Disponibilidad* y *Capacidad de recuperación* son moderadas en un lab que no exige 24/7 y tolera reintentos; y *Autenticidad* se materializa como mecanismo que apoya a Confidencialidad, no como atributo con exigencia propia independiente.

---

## 5. Escenarios de calidad

Para cada uno de los cinco atributos seleccionados se definen **dos escenarios**, ambos en entornos de sobrecarga, degradados o significativos, con los seis componentes de la plantilla ISO. Siguiendo la indicación de la guía del TP2, no se incluyen escenarios en condición normal: los escenarios buscan capturar las situaciones en las que el atributo realmente se pone en juego.

---

### 5.1 Interoperabilidad

**Característica / Subcaracterística:** Compatibilidad / Interoperabilidad.

**Justificación de criticidad del atributo.** LocalBlast *es*, por definición, una interfaz gráfica para BLAST+. Toda ejecución —local o remota— termina siendo una invocación al binario de BLAST+ con los argumentos adecuados y un parseo de su salida. La interoperabilidad con este sistema externo es condición de existencia del producto, y es el atributo con más victorias en la matriz comparativa (9 sobre 9).

**Escenario 1 — sobrecarga por concurrencia de invocaciones**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Varios investigadores del mismo laboratorio, trabajando simultáneamente |
| Estímulo | Lanzan hasta cinco búsquedas concurrentes contra el sistema, mezclando búsquedas locales (contra el catálogo del laboratorio) y remotas (contra NCBI a través de BLAST+) |
| Entorno | Sobrecarga — cinco invocaciones concurrentes a BLAST+ sobre el mismo servidor, cada una con parámetros, bases de datos y resultados distintos |
| Artefacto | Módulo de ejecución asíncrona del sistema, responsable de invocar BLAST+ como subproceso y de mantener la correspondencia entre cada subproceso y la sesión del investigador que lo originó |
| Respuesta | El sistema lanza cada búsqueda como un subproceso independiente de BLAST+, con su propio contexto de ejecución y su propio identificador; mantiene la asociación entre cada subproceso y la sesión del investigador correspondiente, y al terminar entrega los resultados exclusivamente a esa sesión, sin cruzarlos con los de otras búsquedas en curso |
| Medida de la respuesta | Cero cruces de resultados entre búsquedas concurrentes con hasta cinco búsquedas simultáneas |

*Criticidad:* un cruce de resultados entre investigadores sería un error silencioso: el investigador vería alineamientos ajenos como si fueran los suyos y los interpretaría en el contexto equivocado. Es el escenario típico de un laboratorio al final de la jornada, cuando varios investigadores lanzan búsquedas al mismo tiempo.

**Escenario 2 — degradado por cambio menor de versión de BLAST+**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | BLAST+ como sistema externo |
| Estímulo | Devuelve una salida con cambios menores respecto a la versión soportada por el sistema: una columna adicional en la salida tabular, o un campo nuevo en la salida XML, tras una actualización menor del binario BLAST+ realizada por el administrador de sistemas sin coordinarla con el equipo de desarrollo |
| Entorno | Degradado — versión de BLAST+ posterior a la validada por el equipo de LocalBlast |
| Artefacto | Parser de la salida de BLAST+ dentro del módulo de ejecución, responsable de convertir el texto devuelto por el binario en la tabla de alineamientos que el investigador ve |
| Respuesta | El parser reconoce los campos conocidos y los extrae correctamente, detecta la presencia de campos adicionales no mapeados y los ignora sin corromper los campos conocidos, no aborta la ejecución, no bloquea la presentación de los resultados al investigador y registra una advertencia en el log del sistema para que el equipo de desarrollo pueda incorporar el nuevo campo en una iteración futura |
| Medida de la respuesta | El 100% de las búsquedas con salida de formato "casi conocido" (columnas adicionales no esperadas o campos XML nuevos) completan la presentación de resultados con los campos obligatorios (identificador del hit, score, E-value observado, porcentaje de identidad y porcentaje de cobertura) intactos; el 100% de esos casos quedan registrados en el log con la advertencia correspondiente |

*Criticidad:* BLAST+ es externo y lo actualiza el administrador de sistemas del laboratorio por decisiones ajenas al equipo de desarrollo de LocalBlast. Una actualización menor del motor no debería romper nuestro sistema. Es un escenario realista y recurrente en productos que envuelven herramientas que no controlan.

---

### 5.2 Operabilidad

**Característica / Subcaracterística:** Capacidad de interacción / Operabilidad.

**Justificación de criticidad del atributo.** La propuesta de valor explícita de LocalBlast frente a la línea de comandos de BLAST+ y frente a la interfaz web oficial de NCBI es ser *"ágil e intuitiva"* (ver canvas de descubrimiento en el README). Si la operabilidad falla, el investigador vuelve a la terminal y el producto pierde su razón de ser. Es el segundo atributo con más victorias en la matriz comparativa.

**Escenario 1 — sobrecarga por filtrado interactivo sobre muchos resultados**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador trabajando con una búsqueda que devolvió un conjunto grande de alineamientos |
| Estímulo | Aplica sucesivamente cuatro filtros sobre la tabla de resultados (umbral de identidad, umbral de cobertura, umbral de E-value y filtro por taxonomía), modificando los umbrales varias veces por minuto para explorar interactivamente el conjunto |
| Entorno | Sobrecarga — tabla con más de 500 hits y ritmo rápido de ajuste de filtros |
| Artefacto | Módulo de filtrado posterior a la búsqueda y la interfaz de la tabla de resultados en el navegador |
| Respuesta | Cada cambio de filtro refresca la tabla en el momento sobre el conjunto crudo original (nunca sobre un resultado filtrado previo), los filtros aplicados quedan siempre visibles y editables, y el investigador puede combinarlos, aflojarlos, endurecerlos o quitarlos en cualquier orden sin tener que reiniciar nada y sin esperas significativas entre cambios |
| Medida de la respuesta | Cada actualización de la tabla ante un cambio de filtro se refleja en menos de **1 segundo** con tablas de hasta 500 hits; el estado de los filtros aplicados permanece visible y editable durante toda la sesión |

*Criticidad:* el filtrado interactivo posterior a la búsqueda es una de las dos capacidades que diferencian a LocalBlast de la interfaz web oficial de NCBI. Si no responde ágilmente en escenarios con muchos hits —que son los más interesantes desde el punto de vista biológico— el investigador vuelve a parsear la salida tabular a mano y pierde la ventaja del producto.

**Escenario 2 — degradado por modificación posterior a la validación de la configuración**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Investigador |
| Estímulo | Modifica un campo del formulario (por ejemplo, cambia el programa BLAST de `blastp` a `blastx`, o cambia la base de datos seleccionada) **después** de que ya le había pedido al sistema que validara su configuración y había recibido el visto bueno explícito "configuración válida, lista para ejecutar" |
| Entorno | Degradado — el usuario altera una configuración ya marcada como ejecutable; si el sistema no reacciona, podría disparar la búsqueda sobre una combinación inconsistente con lo que se había validado |
| Artefacto | Formulario de configuración de la búsqueda y mecanismo que rastrea el estado "validada / no validada" de la configuración |
| Respuesta | El sistema invalida inmediatamente la marca "válida, lista para ejecutar", deshabilita visualmente el botón de ejecución de la búsqueda, señala en la interfaz que el cambio invalidó la validación previa (sin exigirle al investigador que lea un mensaje de texto para percibirlo), y preserva todos los demás valores del formulario para que el investigador no tenga que volver a cargarlos |
| Medida de la respuesta | El 100% de los cambios posteriores a la validación sobre campos relevantes del formulario (modo local/remoto, base de datos, programa, parámetros previos a la búsqueda) disparan la invalidación visual y la deshabilitación del botón en menos de **500 ms**; en el 0% de los casos puede dispararse una búsqueda sobre una configuración modificada después de la validación sin volver a pasar por el paso de validación |

*Criticidad:* evita que el investigador, por inercia visual, lance una búsqueda con una configuración que ya no coincide con lo que había validado. Es una protección activa de la operabilidad que no requiere intervención consciente del usuario: el sistema le ahorra el error antes de que lo cometa.

---

### 5.3 Confidencialidad

**Característica / Subcaracterística:** Seguridad / Confidencialidad.

**Justificación de criticidad del atributo.** Las secuencias biológicas que un investigador carga en LocalBlast pueden provenir de muestras de origen humano (ADN de pacientes, por ejemplo) y, en ese caso, califican como **datos sensibles** desde el punto de vista bioético y de protección de datos personales. La confidencialidad se juega en tres frentes concretos: la transmisión por red entre el navegador del investigador y el servidor, el almacenamiento del historial de búsquedas en el servidor, y el aislamiento entre los historiales de los distintos investigadores del laboratorio. Que ninguno de esos tres frentes se pierda es responsabilidad del sistema; una fuga en cualquiera de ellos es un incidente irreversible.

**Escenario 1 — degradado por intercepción pasiva del tráfico de red**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Un tercero con capacidad de observar el tráfico de la red interna del laboratorio (por ejemplo, un nodo intermedio comprometido o un sniffer en la red Wi-Fi del laboratorio) |
| Estímulo | Captura los paquetes de red que viajan entre el navegador del investigador y el servidor donde corren LocalBlast y BLAST+, durante una búsqueda cuyo query es una secuencia potencialmente sensible (ADN proveniente de una muestra humana) |
| Entorno | Degradado — red del laboratorio en la que no se puede asumir que todos los nodos intermedios sean confiables; el sistema debe comportarse como si la red estuviera siendo observada |
| Artefacto | Canal de comunicación entre el navegador del investigador y el servidor del sistema, y archivos temporales que el sistema pueda generar en disco para pasar la secuencia al subproceso de BLAST+ |
| Respuesta | Toda la comunicación entre el navegador y el servidor viaja cifrada mediante TLS; la secuencia query nunca se transmite por canales en texto plano; en el servidor, los archivos temporales que el sistema necesite para pasar la secuencia al subproceso de BLAST+ existen únicamente durante la ejecución y se eliminan al finalizar la búsqueda, con permisos restringidos al usuario del sistema mientras existen |
| Medida de la respuesta | Cero paquetes capturados contienen la secuencia query en texto plano (verificable con una captura de tráfico de referencia); cero archivos temporales con la secuencia query permanecen en el disco del servidor más allá de **1 minuto** después de que la búsqueda finaliza (verificable con una inspección del directorio temporal del sistema) |

*Criticidad:* una secuencia de ADN humano publicada o filtrada identifica indirectamente a la persona de la que proviene y, en combinación con otras bases de datos, puede re-identificarla. La protección en tránsito y en almacenamiento transitorio no es "nice to have": es la línea mínima para que el laboratorio pueda usar LocalBlast con muestras humanas.

**Escenario 2 — degradado por intento de acceso cruzado al historial de otro investigador**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Un investigador autenticado en el sistema, perteneciente al mismo laboratorio que la víctima |
| Estímulo | Intenta acceder al historial de búsquedas de otro investigador (que incluye las secuencias query usadas, los parámetros y los resultados crudos), ya sea manipulando parámetros de URL, forjando un identificador de sesión o cualquier otra variante |
| Entorno | Degradado — usuario legítimamente autenticado en el sistema, pero intentando acceder a datos que no le pertenecen |
| Artefacto | Mecanismo de autorización que gobierna el acceso al historial persistido del sistema |
| Respuesta | El sistema rechaza el acceso con una respuesta de "no autorizado" (código HTTP 403 o equivalente), no devuelve siquiera metadatos de las búsquedas ajenas (ni títulos, ni timestamps, ni confirmación sobre si existen o no), y registra el intento en el log de auditoría del servidor con el identificador del investigador que lo intentó y el recurso al que intentó acceder |
| Medida de la respuesta | El 100% de los intentos de acceso al historial ajeno son rechazados sin revelar información alguna sobre su existencia (ni siquiera distinguir entre "existe pero no tenés permiso" y "no existe"); el 100% de los intentos quedan registrados en el log de auditoría con el investigador que los realizó y el recurso solicitado |

*Criticidad:* en un laboratorio con varios investigadores que comparten infraestructura, la autenticación por sí sola no basta: hace falta aislamiento entre historiales. Un investigador no debe poder ver qué secuencias está analizando otro (podrían corresponder a un paciente, a un proyecto en curso no publicado, o a datos sometidos a acuerdos de confidencialidad). El escenario también exige que el sistema no filtre información por "canales laterales" (confirmar la existencia de recursos ajenos aunque no se devuelva su contenido).

---

### 5.4 Tolerancia a fallos

**Característica / Subcaracterística:** Fiabilidad / Tolerancia a fallos.

**Justificación de criticidad del atributo.** LocalBlast depende de dos sistemas externos sobre los que no tiene control: **BLAST+** y, a través de BLAST+ cuando se usa el modo remoto, **NCBI**. Los fallos remotos (timeouts, rate limits, errores explícitos devueltos por NCBI) son frecuentes y previsibles en el día a día del laboratorio. La tolerancia a fallos es lo que protege el trabajo del investigador cuando el entorno externo se degrada.

**Escenario 1 — sobrecarga por rate limit de NCBI**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | NCBI, el proveedor del servicio BLAST remoto, a través de BLAST+ |
| Estímulo | Devuelve un error de rate limit después de que varios investigadores del laboratorio lanzaron búsquedas remotas en rápida sucesión, excediendo las políticas de uso aceptable de NCBI |
| Entorno | Sobrecarga — múltiples investigadores usan el modo remoto simultáneamente desde la misma red del laboratorio (NCBI identifica como "mismo origen" al conjunto) |
| Artefacto | Módulo de ejecución asíncrona del sistema y canal de manejo de errores proveniente de BLAST+ |
| Respuesta | Para las búsquedas que NCBI rechaza: el sistema corta su flujo, no genera un registro de resultados en el historial, muestra al investigador afectado el mensaje literal de error de BLAST+ (incluyendo el texto original devuelto por NCBI, para que el investigador pueda distinguir entre un rechazo por rate limit, por rechazo del query, o por otro motivo). Para las búsquedas de otros investigadores que están en curso en ese momento: no se ven afectadas y siguen su ejecución normal sin interrupciones |
| Medida de la respuesta | El 100% de los errores de rate limit se muestran al investigador correspondiente dentro de los **3 segundos** de ser recibidos por el sistema; cero búsquedas de otros investigadores interrumpidas o alteradas como consecuencia del error ajeno |

*Criticidad:* los rate limits de NCBI son uno de los modos de fallo más comunes del modo remoto de BLAST. Protege dos cosas a la vez: honestidad hacia el investigador afectado (mostrar el motivo real, no un error genérico) y aislamiento entre sesiones concurrentes (el error de uno no se propaga a los demás).

**Escenario 2 — degradado por timeout de NCBI durante una búsqueda en curso**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Red o infraestructura externa entre BLAST+ (que corre en el servidor del laboratorio) y los servidores de NCBI |
| Estímulo | Se produce un timeout de comunicación con NCBI durante una búsqueda remota que llevaba varios minutos de ejecución |
| Entorno | Degradado — fallo intermitente de conectividad; BLAST+ reporta el timeout tras no recibir respuesta de NCBI dentro del plazo esperado |
| Artefacto | Módulo de ejecución asíncrona del sistema y su manejo de errores de BLAST+ |
| Respuesta | El sistema detecta el timeout reportado por BLAST+, corta el flujo de ejecución, no genera un registro de resultados en el historial, muestra un mensaje que distingue explícitamente un timeout de conexión remota de un problema de parámetros de la búsqueda (para que el investigador no reconfigure lo que no estaba mal), y deja la interfaz en el estado "configuración ejecutable" preservando los valores del formulario, para que el investigador pueda relanzar la misma búsqueda sin tener que reconfigurar nada |
| Medida de la respuesta | El 100% de los timeouts remotos se identifican y comunican como tales dentro de los **60 segundos** del evento (no como "error de configuración" ni como "error genérico"); en el 100% de los casos la configuración validada se preserva íntegramente en la interfaz |

*Criticidad:* la peor experiencia posible es que una búsqueda remota tarde diez minutos, falle por red y obligue al investigador a cargar de nuevo la secuencia y configurar todo desde cero. Preservar la configuración y comunicar bien el motivo del fallo es lo que diferencia una herramienta profesional de una frágil.

---

### 5.5 Modularidad

**Característica / Subcaracterística:** Mantenibilidad / Modularidad.

**Justificación de criticidad del atributo.** El proyecto tiene un modelo de ciclo de vida explícitamente **incremental con prácticas ágiles** (ver README, sección "Modelo de Ciclo de Vida"). El TP1 declara explícitamente **fuera de alcance** para este cuatrimestre varias capacidades que están previstas para iteraciones futuras: el rol administrador de bases de datos locales (con alta, actualización y baja desde la propia aplicación), búsquedas en lote con múltiples queries simultáneas, y la posibilidad de añadir nuevos formatos de descarga y nuevos filtros posteriores a la búsqueda. Si el diseño no soporta esta evolución planeada sin reescribir módulos existentes, el enfoque incremental se vuelve impracticable: cada incorporación requeriría rehacer lo que ya funciona.

**Escenario 1 — significativo por incorporación de un nuevo formato de descarga**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Equipo de desarrollo, en una iteración futura |
| Estímulo | Debe incorporar un nuevo formato de descarga de resultados (por ejemplo, Parquet, o un formato propio del laboratorio) al conjunto de formatos ya soportados (CSV, JSON, FASTA, tabular BLAST y XML) |
| Entorno | Significativo — evolución planeada del sistema dentro del modelo de ciclo de vida incremental declarado para el proyecto |
| Artefacto | Módulo de descarga de resultados, su registro de formatos disponibles, y la interfaz de usuario que lista las opciones de descarga |
| Respuesta | El equipo agrega el soporte del nuevo formato implementando la interfaz definida para "formato de descarga" (serializar un conjunto de alineamientos + metadatos de la búsqueda) y registrándolo en el único punto previsto para ello; no modifica la lógica de los formatos preexistentes, ni la interfaz de usuario que lista los formatos (la lista se arma dinámicamente desde el registro), ni el módulo de filtrado previo a la descarga |
| Medida de la respuesta | La incorporación del nuevo formato afecta exclusivamente a archivos nuevos (la implementación del nuevo formato) y a un único punto de registro en el módulo de descarga; los tests automatizados de los formatos preexistentes siguen pasando sin modificación; el tiempo de incorporación del nuevo formato (desde que empieza el desarrollo hasta que está integrado y testeado) es bajo |

*Criticidad:* el enfoque incremental compromete al equipo a sumar capacidades sin romper las existentes. Si incorporar un formato nuevo exige retocar los demás, cada incremento se vuelve una regresión potencial. Este escenario mide la propiedad arquitectónica (bajo acoplamiento del módulo de descarga) de la que depende todo el modelo de ciclo de vida.

**Escenario 2 — significativo por incorporación del rol administrador**

| Campo | Contenido |
|---|---|
| Fuente del estímulo | Equipo de desarrollo, en una iteración futura |
| Estímulo | Debe incorporar el rol de **administrador de bases de datos locales** (actualmente documentado en los diagramas pero fuera del alcance del TP1), que le permitirá a un administrador dar de alta, actualizar y dar de baja bases de datos BLAST locales desde la propia aplicación, invocando internamente a `makeblastdb` |
| Entorno | Significativo — evolución planeada que suma un **tipo de usuario nuevo** con un proceso propio (el proceso de administración del catálogo del DFD Nivel 1, hasta ahora no implementado) |
| Artefacto | Capa de autenticación y autorización del sistema, módulo nuevo de administración del catálogo de bases de datos, almacén del catálogo (ya existente y usado hoy en modo lectura) y vistas asociadas al nuevo rol |
| Respuesta | El equipo introduce el nuevo rol sin modificar el flujo ni la interfaz del rol investigador: la autenticación/autorización se extiende para distinguir dos roles, el nuevo módulo de administración del catálogo se incorpora como componente separado que lee y escribe el almacén del catálogo existente, y la lógica actual de ejecución de búsquedas (que hoy lee el catálogo) no se modifica — sigue leyendo del mismo almacén, que ahora también se escribe desde el módulo nuevo |
| Medida de la respuesta | La incorporación del rol administrador no requiere modificar los módulos existentes de ejecución de búsqueda, filtrado posterior a la búsqueda ni descarga de resultados; los tests automatizados de las funcionalidades del rol investigador siguen pasando sin cambios; los cambios en la capa de autorización se limitan a extender el esquema de roles sin alterar la lógica de autorización existente para el rol investigador |

*Criticidad:* el rol administrador es la pieza más ambiciosa de las que están fuera del alcance del TP1. Si el diseño actual no permite incorporarlo sin tocar el flujo del investigador, la decisión de haberlo dejado "para después" se vuelve una deuda estructural costosa. Este escenario mide si la arquitectura del sistema soporta la separación por actor y por proceso que el DFD ya anticipa.

---

## Referencias

- [`srs.md`](../srs.md) — Especificación de Requerimientos de Software (TP1).
- [`casos-de-uso.md`](../casos-de-uso.md) — Casos de uso en formato Cockburn.
- [`historias-usuario.md`](../historias-usuario.md) — Historias de usuario con criterios Given-When-Then.
- [`../../uso-ia.md`](../../uso-ia.md) — Bitácora de uso de IA, con las entradas correspondientes al TP2 Parte A.
- Anexo A de la guía de cátedra del TP2 (taxonomía de atributos de calidad ISO/IEC 25010:2023).

