# Perfiles de usuario — LocalBlast

Esta carpeta contiene los perfiles de usuario que guían el maquetado de la interfaz del sistema. Cada perfil incluye su escenario de uso y su flujo de navegación.

## Actor principal

Según [SRS §2.2](../../requeriments/srs.md#22-actores-del-sistema), el sistema tiene dos actores humanos:

- **Investigador/a** — actor principal de los procesos profundizados **P1 y P2**. Todas las historias de usuario del catálogo (HU01 a HU14) tienen a este actor como protagonista.
- **Administrador/a de bases de datos** — actor del proceso **P3**, que queda explícitamente **fuera de alcance** (ver [SRS §1.4](../../requeriments/srs.md#14-fuera-del-alcance)): no tiene RF asociados, no tiene casos de uso detallados y no tiene historias de usuario.

En consecuencia, **el único actor principal con historias de usuario es "Investigador/a"**, y es el único perfil que corresponde elaborar en esta carpeta.

El Administrador no se perfila porque no hay HUs que respalden pantallas para él, y el principio de diseño del sistema es maquetar únicamente las interfaces respaldadas por una historia de usuario del catálogo. El actor no humano **BLAST+** (sistema externo) no requiere perfil de usuario — no interactúa con la interfaz gráfica, es invocado por el backend.

## Un perfil, con rango interno de variación

El SRS distingue en [§2.1](../../requeriments/srs.md#21-stakeholders) dos **subgrupos de stakeholders** que pueden asumir el rol de Investigador/a (estudiantes de grado/posgrado e investigadores sénior / docentes de bioinformática), caracterizados con niveles de conocimiento técnico y objetivos primarios distintos. Como se trata del mismo actor del sistema (mismas capacidades, mismas HUs, mismo rol), los dos subgrupos quedan representados dentro de un único perfil como **rangos de variación interna** —en nivel de conocimiento técnico, en frecuencia de uso, en qué parte del flujo se ejerce con más intensidad— y no como perfiles separados.

- [`investigador.md`](investigador.md) — perfil del Investigador/a.

## Trazabilidad y declaración de supuestos

Todo lo que el perfil afirma sobre su usuario puede rastrearse a algún documento del proyecto (SRS, DFD, casos de uso o historias de usuario) **o** queda explícitamente marcado como **supuesto del grupo** cuando la documentación no lo cubre. Dentro del perfil, los supuestos se marcan con la etiqueta "**Supuesto del grupo**" al final de la afirmación.
