# Bitácora de uso de IA — TP1

Este documento registra el uso crítico de asistentes de IA generativa durante el TP1, según lo pedido por la cátedra: qué herramienta se usó, para qué tarea puntual, qué generó, qué se aceptó / modificó / descartó, y qué errores o imprecisiones se detectaron.

---

## Entrada 1 — Redacción inicial de casos de uso y HU a partir del canvas

- **Herramienta usada:** asistente de IA generativa basado en LLM.
- **Tarea concreta:** a partir del canvas de descubrimiento y de la lista inicial de requerimientos funcionales que armamos como grupo, pedirle a la IA que propusiera un primer borrador de casos de uso (formato Cockburn) y de historias de usuario con criterios Given-When-Then.
- **Qué generó:**
  - Un CU-01 "Configurar y lanzar búsqueda BLAST" con flujo principal detallado, ~7 pasos, y una lista de slices secundarios A1/A2 nombrados.
  - Un primer intento de historias de usuario para el camino feliz y para el manejo de parámetros inválidos.
- **Qué aceptamos:**
  - La estructura Cockburn (actor / objetivo / precondición / flujo / postcondición / slices) del CU-01, porque encajaba con lo que pide el instructivo del TP1.
  - Los nombres de los slices secundarios como punto de partida.
- **Qué modificamos:**
  - **Alcance del CU:** el primer borrador de la IA mezclaba en un solo CU la carga de la secuencia, la elección del modo, la ejecución **y** la descarga de resultados. Lo dejamos así como CU-01 porque el objetivo del actor es realmente único ("obtener resultados BLAST descargados").
  - **Slices sobre modo remoto y modo local:** la IA los había pensado como CUs distintos ("CU-01a" y "CU-01b"). Los unificamos en el flujo principal con una bifurcación en el paso 2, porque el objetivo del actor es el mismo y el mecanismo se decide con un solo control ("elegir modo") — no son casos de uso distintos.
- **Qué descartamos:**
  - Un slice "el usuario cambia de idioma en la interfaz" que la IA agregó de oficio. No es un slice del CU de búsqueda: si aparece como requerimiento, es un RF transversal o un atributo de calidad, no una variante del flujo.
  - Un intento de la IA de sumar filtros por "score bruto" y "longitud del alineamiento" como criterios post-búsqueda esenciales. En el dominio real esos criterios existen pero los investigadores del grupo confirmaron que los cuatro que dejamos (identidad, cobertura, E-value observado, taxonomía) son los que efectivamente se usan; los otros se pueden sumar más adelante sin cambiar el modelo.
- **Errores / imprecisiones detectadas:**
  - La IA propuso, en un primer borrador, que el sistema **descargara automáticamente SwissProt** al dar de alta el sistema. Es un error: SwissProt se actualiza con frecuencia, tiene tamaño no trivial (~200 MB comprimida), y el laboratorio puede no querer que se cargue por defecto. Discutimos también la variante intermedia — permitir que el administrador indicara una URL desde la interfaz — y también la descartamos: en esta primera versión toda base de datos se carga por subida directa del archivo FASTA desde el equipo del administrador, incluso si el archivo proviene de una base de datos pública como SwissProt (el admin la descarga por fuera del sistema y sube el resultante). Simplifica el modelo, elimina una entidad externa del diagrama de contexto y evita meter en el sistema una descarga de red que no aporta al valor del TP.
  - La IA sugirió como **valor por defecto** del E-value máximo `1e-5` para todo BLAST, sin distinguir programa. En la práctica el default sano varía según el programa (`blastp` y `blastn` usan defaults distintos). Ajustamos el RF-04 para que diga "valores por defecto sensatos **según el programa BLAST correspondiente**", en vez de fijar el número.

## Entrada 2 — Revisión de la primera versión del DFD

- **Herramienta usada:** asistente de IA generativa basado en LLM.
- **Tarea concreta:** pegarle nuestro DFD Nivel 0 y Nivel 1 y pedirle que verificara el balanceo de flujos externos.
- **Qué generó:** una lista de siete flujos externos identificados y su presencia (sí / no) en cada nivel.
- **Qué aceptamos:** el chequeo de balanceo — nos ayudó a detectar que la primera versión del Nivel 1 tenía el flujo del administrador conectado por error al proceso P1 en lugar de a P3.
- **Qué modificamos:** reubicamos ese flujo en el diagrama antes de commitear la versión final.
- **Qué descartamos:** una sugerencia de la IA de "unir P1 y P2 en un solo proceso" para simplificar. La rechazamos porque justamente la separación entre P1 (ejecución) y P2 (filtrado post-búsqueda + entrega) refleja una decisión de dominio importante: los filtros post-búsqueda **no** vuelven a correr BLAST, y esa distinción se pierde si el DFD los mezcla.
- **Errores detectados:** ninguno de la IA en esta revisión; el error estaba en nuestro diagrama y la IA lo ayudó a detectar.

## Entrada 3 — Corrección del diagrama de contexto: BLAST+ como sistema externo (no NCBI)

- **Herramienta usada:** asistente de IA generativa basado en LLM.
- **Tarea concreta:** una vez que teníamos el DFD con Investigador, Administrador y NCBI como entidades externas, un integrante del grupo señaló que NCBI aparecía mal ubicado: nuestro sistema no habla directamente con NCBI. BLAST+ es el que hace toda la comunicación con NCBI internamente cuando se lo invoca con la flag `-remote`. Le pedimos a la IA que rediseñara el DFD para reflejar esto.
- **Qué generó:** un DFD con BLAST+ como entidad externa en lugar de NCBI, mantenimiento del stakeholder NCBI en la tabla (como stakeholder indirecto), y una explicación del modelo local vs. remoto: ambos son invocaciones a BLAST+, la diferencia está del lado de BLAST+ y no del nuestro.
- **Qué aceptamos:**
  - La estructura del nuevo DFD con BLAST+ como sistema externo.
  - Redefinir el almacén D1 como "catálogo de bases de datos" (metadatos) en lugar de "bases de datos BLAST locales" (índices físicos): los índices físicos los produce y consume BLAST+, nuestro sistema solo mantiene el catálogo de qué hay y dónde está.
  - La aclaración de que NCBI queda en la tabla de stakeholders **pero con un rol distinto**: no interactúa con nuestro sistema, solo sus políticas afectan al comportamiento de BLAST+ que sí interactúa.
- **Qué modificamos:**
  - **Textos en las flechas del DFD.** El primer borrador de la IA seguía con etiquetas cortas (F1, F2, …) y una tabla aparte, pero el grupo decidió que era más legible poner el contenido de cada flujo directamente sobre la flecha, con saltos de línea para evitar superposición. Reescribimos cada etiqueta con ese criterio.
  - **Naming del sistema.** La IA propuso renombrar el proyecto entero de "LocalBlast" a "BlastGUI" o similar. Decidimos mantener "LocalBlast" (así se llama el repo) y en su lugar dejar en el proceso 0 el rótulo *"LocalBlast · GUI web para BLAST+"* para que quede claro que el sistema es una GUI, no un motor de alineamiento propio.
- **Qué descartamos:** una sugerencia de la IA de "unir P1 y P2 en un solo proceso" para simplificar (venía de una revisión anterior).
- **Errores detectados:**
  - La primera versión que generó la IA seguía poniendo un flujo directo del sistema hacia NCBI en modo remoto, "por prolijidad de que se vea el destino final". Le tuvimos que insistir explícitamente en que ese flujo pasa por dentro de BLAST+ y no debe representarse como flujo de nuestro sistema, para no mentir sobre la arquitectura real.

## Entrada 4 — Corrección posterior a la devolución del profesor (iteración de casos de uso, slices, alternativas/excepciones y HU en formato Given-When-Then)

- **Herramienta usada:** asistente de IA generativa basado en LLM.
- **Tarea concreta:** después de una devolución del profesor sobre la primera versión del TP1, le pasamos a la IA la guía de la cátedra (`tp1-requerimientos.md` y `ejemplo-resuelto-tp1.md`) junto con nuestro repo actual, y le pedimos que aplicara todas las correcciones señaladas en clase, manteniendo el resto del trabajo intacto.
- **Correcciones que había que aplicar (según lo que anotamos de la clase):**
  1. Los casos de uso deben derivar todos de **un solo proceso** del DFD Nivel 1. Elegimos **P1 · Ejecutar búsqueda BLAST**. Esto implica que el anterior `CU-02 · Administrar base de datos BLAST local` (que venía del proceso P3) **no corresponde** en este TP y debía eliminarse del documento de casos de uso.
  2. El camino feliz de `CU001` es largo (12 pasos): había que **descomponerlo en slices básicos** con valor propio (`B1`, `B2`, `B3`, …) siempre que cada slice aporte por sí mismo al objetivo del CU.
  3. Distinguir **alternativas** (`A1`, `A2`, …: caminos alternativos al feliz que igual permiten avanzar) de **excepciones** (`E1`, `E2`, …: terminaciones abruptas del flujo). En la versión anterior teníamos todo mezclado como "slices A1-A7", lo cual era conceptualmente incorrecto.
  4. **Relación 1:1 entre slice e historia de usuario.** La HU asociada a un slice conserva su identificador de origen para no romper la trazabilidad: por ejemplo la HU del slice `CU001_B1` se llama `HU01_CU001_B1`.
  5. **Criterios de aceptación en formato Given-When-Then**, no en prosa como los teníamos.
  6. **Trazabilidad final:** `RF → CU → slice → HU`, con la aclaración explícita de que un CU puede implementar uno o varios RF (y a la inversa, un RF puede estar realizado por varios slices del mismo CU).
- **Qué generó la IA:**
  - Un nuevo `casos-de-uso.md` con un único caso de uso `CU001 · Ejecutar búsqueda BLAST` derivado de P1, descompuesto en tres slices básicos (`B1` carga y configuración, `B2` ejecución y resultados, `B3` filtrado y descarga), tres alternativas (`A1` cancelación manual, `A2` resultado vacío, `A3` cambio de local a remoto) y cuatro excepciones (`E1` a `E4`, agrupando los cuatro casos previos de "sistema no lanza la búsqueda" o "corte abrupto durante la ejecución").
  - Un nuevo `historias-usuario.md` con cuatro HU detalladas (`HU01_CU001_B1`, `HU02_CU001_B2`, `HU03_CU001_B3`, `HU04_CU001_E1`), todas con criterios Given-When-Then, y el resto de los slices nombrados en la tabla de trazabilidad pero sin desarrollar todavía.
  - Un `srs.md` con la sección 5 reescrita para justificar que se profundiza únicamente P1, la lista de RF acotada a P1 (RF-01 a RF-10), y la tabla resumen de trazabilidad actualizada.
- **Qué aceptamos:**
  - La descomposición del camino feliz en tres slices `B1/B2/B3`. Discutimos primero si convenían dos (pre-ejecución vs post-ejecución) o tres (configuración / ejecución / entrega) y nos quedamos con tres porque cada uno aporta un valor claramente distinto y demarcable: `B1` deja la búsqueda lista para lanzar, `B2` deja los resultados crudos frente al investigador, `B3` deja el archivo entregable en su equipo.
  - La reclasificación de los antiguos "A1..A7" en tres alternativas (`A1`, `A2`, `A3`) y cuatro excepciones (`E1`, `E2`, `E3`, `E4`). La IA aplicó bien el criterio del profesor: "terminación abrupta" ⇒ excepción, "camino alterno válido" ⇒ alternativa.
  - El formato de identificadores `CU001`, `CU001_B1`, `HU01_CU001_B1`, tal como se lo pidió el profesor.
- **Qué modificamos:**
  - **Slice `A3` (base de datos local no disponible).** La primera versión que generó la IA lo clasificó como excepción (`E5`), argumentando que era una "falla del entorno". Lo movimos a alternativa (`A3`) porque el sistema no termina abruptamente: informa el estado y devuelve el control al investigador, con lo cual el flujo puede continuar y alcanzar el objetivo por otra ruta — que es justamente la definición de camino alternativo. La IA propuso además, en una versión intermedia, que el sistema "sugiriera automáticamente cambiar a modo remoto contra una base equivalente de NCBI". **Descartamos** esa propuesta: no existen equivalencias reales entre una base local del laboratorio y las bases estándar de NCBI (una es datos internos o un espejo puntual, la otra es un catálogo público con otra fecha y otra composición), y proponer el cambio sería científicamente engañoso — el investigador podría interpretar como equivalentes resultados que no lo son. La versión final del slice deja al sistema únicamente informando el estado de la base local no disponible y devolviendo el control al investigador para que él decida.
  - **Un criterio Given-When-Then que juntaba dos acciones en el When.** En la primera versión de `HU03_CU001_B3`, la IA había puesto un criterio con `When el investigador aplica filtros y descarga en CSV`. Lo separamos en dos criterios (`CA-01` filtrado, `CA-02` descarga), siguiendo el aviso de la propia guía del TP1 de que un When con más de una acción es señal de que en realidad son dos criterios o de que el slice está mal cortado.
  - **Trazabilidad RF-06.** La IA en la primera pasada asignó RF-06 solo al slice `B1`. Extendimos la trazabilidad a los slices `E1` y `E2` también, porque las excepciones de validación son otra forma en la que se cumple el RF de validación (aunque el resultado sea distinto). Dejamos escrito ese razonamiento en el propio `casos-de-uso.md`.
- **Qué descartamos:**
  - Una propuesta inicial de la IA de dejar un `HU05_CU001_A1` (cancelación manual) también detallado. Decidimos no hacerlo por dos razones: (a) la guía del TP1 pide detallar el slice básico y "un slice secundario relevante por CU", y (b) el slice de excepción `E1` ya es el "slice secundario relevante" más informativo del CU en esta iteración, porque toca directamente la validación previa a la invocación de BLAST+, que es lo distintivo del proceso.
- **Errores / imprecisiones detectadas:**
  - La IA, en su primera pasada, mantuvo referencias a "CU-02" en varios lados del SRS y del contexto inicial, aunque le habíamos dicho explícitamente que había que eliminarlo. Tuvimos que pedirle una segunda pasada de barrido para asegurarnos de que ninguna sección quedaba mencionando a CU-02 o al proceso P3 profundizado. Volvió a demostrar lo que ya habíamos anotado: la IA es útil como generador rápido, pero requiere una revisión sistemática por parte del grupo antes de commitear.

## Entrada 5 — Reestructuración de casos de uso: capacidades del sistema, no trazos secuenciales del actor

- **Herramienta usada:** asistente de IA generativa basado en LLM.
- **Tarea concreta:** volver a iterar sobre el `casos-de-uso.md` a partir de un comentario del profesor que uno de los integrantes recordaba de clase: *"no se debe pensar el caso de uso como algo secuencial que hace el actor"*. Le pedimos a la IA que revisara nuestro modelado —hasta ese momento un único `CU001` con tres slices básicos (`B1` config, `B2` ejecución, `B3` filtrado y descarga)— y evaluara si esa forma no era justamente "pensar el CU como secuencia".
- **Qué generó:**
  - Una propuesta de reestructurar el modelado en **dos casos de uso** derivados del proceso P1, donde cada CU representa una capacidad discreta del sistema hacia el actor y no un tramo de un workflow:
    - `CU001 · Ejecutar una búsqueda BLAST` (objetivo: obtener alineamientos visibles en la interfaz), con 9 pasos en el camino feliz — se subdivide en dos slices porque está en el borde de "largo": `B1` (cargar, configurar y validar) y `B2` (ejecutar y presentar resultados).
    - `CU002 · Refinar y descargar los resultados de una búsqueda` (objetivo: obtener un archivo con los alineamientos filtrados), con 4 pasos en el camino feliz — no se subdivide.
  - Una tabla de trazabilidad `RF → CU → slice → HU` reorganizada, donde ningún RF cruza entre los dos CU (RF-01 a RF-08 → `CU001`; RF-09 y RF-10 → `CU002`), lo cual es una consecuencia natural de haber separado los CU por capacidad.
  - Una explicación agregada al principio del `casos-de-uso.md` de por qué un CU no es una secuencia de pasos del actor, para que la decisión de tener dos CU en vez de uno quede justificada por escrito (y no requiera contar la historia de clase).
- **Qué aceptamos:**
  - La separación en dos CU. Discutimos primero si tres podían tener sentido (por ejemplo, un tercer CU aparte para "Cancelar una búsqueda"), y lo descartamos con un razonamiento del propio Cockburn: cancelar es abandonar un objetivo, no un objetivo en sí, así que corresponde como slice alternativo dentro del CU al que pertenece la acción cancelada (`CU001_A1`), no como CU independiente.
  - El slicing de `CU001` en `B1` y `B2`. 9 pasos son el borde superior de lo que Cockburn considera un happy path sano; dividirlo en dos slices con valor incremental —dejar la búsqueda validada versus mostrar los alineamientos— hace más natural la trazabilidad a HU.
  - El uso de `CU002_B` (letra `B` sin número) como identificador del slice básico único de `CU002`, siguiendo el ejemplo del profesor sobre la notación (`"CU001_B pasaría a CU001_B1 y CU001_B2"` cuando se subdivide → si no se subdivide, queda como `CU00X_B`).
- **Qué modificamos:**
  - **Precondición de `CU002`.** La IA en un primer borrador escribió la precondición como *"`CU001` fue ejecutado exitosamente"*. La reescribimos como *"existe una búsqueda con resultados visibles en la interfaz"* — que es el mismo hecho, pero expresado como estado del sistema y no como dependencia entre CU. Cockburn recomienda explícitamente eso: la precondición fija un estado que el CU necesita encontrar, no obliga a que otro CU se haya ejecutado antes en la misma sesión.
  - **Persistencia en el historial (D2).** La IA la incluyó primero como paso final de `CU001`, luego como paso final de `CU002`. Discutimos entre nosotros y la dejamos en `CU002` — se guarda cuando el investigador cierra el ciclo con una descarga. La decisión implica que una búsqueda ejecutada pero nunca descargada no queda en el historial; lo dejamos anotado como decisión consciente en el propio CU.
  - **`A2` de `CU001` (BD local no disponible).** En esta reestructuración volvimos a mirar ese slice y confirmamos la definición honesta que ya habíamos acordado: el sistema informa y devuelve el control al investigador, sin proponer equivalencias con bases remotas (que no existen). La numeración del slice pasa de `A3` (versión anterior) a `A2` (versión actual), porque ahora `CU001` tiene menos alternativas — el "resultado vacío" pasó a ser `CU002_A1`, ya que ocurre en el momento de descargar, no en el de ejecutar.
- **Qué descartamos:**
  - Una propuesta inicial de la IA de tener **tres CU** (`CU001` configurar, `CU002` ejecutar, `CU003` filtrar y descargar). La rechazamos porque "configurar" sin ejecutar no le deja nada al actor —no es un objetivo terminado, es un paso intermedio— y por lo tanto no cumple con la definición de CU como capacidad discreta. Terminó siendo, en la versión final, el slice `CU001_B1` dentro del CU de ejecución.
- **Errores / imprecisiones detectadas:**
  - La IA, en la primera pasada de esta reestructuración, arrastró la persistencia en D2 como paso separado de `CU002` "para que quede alineado con el DFD", pero lo puso también como paso final de `CU001` "por prolijidad de que la búsqueda quede guardada apenas termina". Tuvimos que insistir en que la duplicación era mala señal (dos CU no pueden compartir un paso de la misma forma, o uno lo incluye al otro con `<<include>>` o hay que decidir en cuál va) y forzarla a elegir uno solo con criterio. La versión final deja el registro en historial dentro de `CU002`, con la consecuencia asumida ya mencionada arriba.
  - En la primera versión de la tabla `RF → CU → slice`, la IA olvidó que la validación previa a la invocación de BLAST+ (RF-06) también se realiza en los slices de excepción `E1` y `E2` — cuando la validación falla y corta el flujo. Igual que en la iteración anterior, tuvimos que pedirle expresamente que verificara la trazabilidad de cada RF sobre todos los slices, no solo el básico.

---

## Reflexión general

El uso de IA fue útil como **primer generador rápido de borradores** — sobre todo para arrancar sin quedarse mirando la hoja en blanco, y en la última entrada, para aplicar de manera consistente una lista de correcciones que afectaba varios archivos a la vez — pero **requiere revisión sistemática por parte del grupo**. Los errores que detectamos no fueron formales (formato, sintaxis) sino de **dominio y arquitectura**: la IA no sabe que SwissProt no se autodescarga, ni que el E-value default varía por programa, ni que hay una distinción conceptual entre parámetros pre-búsqueda y filtros post-búsqueda, ni que nuestro sistema no habla con NCBI sino con BLAST+, ni distingue por sí sola cuándo un flujo es un camino alternativo válido y cuándo es una terminación abrupta. Todo eso solo lo pudimos poner porque discutimos entre nosotros el modelo antes de aceptar el texto generado.

La lección para los próximos TPs: usar la IA para agilizar la **redacción** y para aplicar cambios transversales de manera consistente, pero seguir discutiendo el **contenido** entre nosotros — el asistente ayuda a escribir más rápido lo que ya entendimos, no a entender por nosotros.
