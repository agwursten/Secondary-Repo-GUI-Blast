# Perfiles de usuario — LocalBlast

Esta carpeta contiene los perfiles de usuario que guían el maquetado de la interfaz (sección 4.1 del TP2 Parte B). Cada perfil incluye su escenario de uso y su flujo de navegación, siguiendo lo pedido por la consigna 4.2.

## Actor principal del TP1

El TP1 identifica dos actores humanos del sistema (ver [SRS §2.2](../../requeriments/srs.md#22-actores-del-sistema)):

- **Investigador/a** — actor principal de los procesos profundizados **P1 y P2**. Todas las historias de usuario del TP1 (HU01 a HU14) tienen a este actor como protagonista.
- **Administrador/a de bases de datos** — actor del proceso **P3**, que el TP1 declara explícitamente **fuera de alcance** (ver [SRS §1.4](../../requeriments/srs.md#14-fuera-del-alcance)): no tiene RF asociados, no tiene casos de uso detallados y no tiene historias de usuario.

En consecuencia, **el único actor principal del TP1 con historias de usuario es "Investigador/a"**. Siguiendo la consigna 4.2 (*"Para cada actor principal identificado en el TP1, el grupo elabora..."*), este es el único perfil que corresponde elaborar.

El Administrador no se perfila porque no hay HUs del TP1 que respalden pantallas para él, y la consigna 4.1 prohíbe maquetar fuera de las HUs del TP1. El actor no humano **BLAST+** (sistema externo) no requiere perfil de usuario — no interactúa con la interfaz gráfica, es invocado por el backend.

## Un perfil, con rango interno de variación

El SRS distingue en [§2.1](../../requeriments/srs.md#21-stakeholders) dos **subgrupos de stakeholders** que pueden asumir el rol de Investigador/a (estudiantes de grado/posgrado y investigadores sénior / docentes de bioinformática), caracterizados con niveles de conocimiento técnico y objetivos primarios distintos. Como se trata del mismo actor del sistema (mismas capacidades, mismas HUs, mismo rol), los dos subgrupos quedan representados dentro de un único perfil como **rangos de variación interna** —en nivel de conocimiento técnico, en frecuencia de uso, en qué parte del flujo ejercen con más intensidad— y no como perfiles separados.

- [`investigador.md`](investigador.md) — perfil del Investigador/a.

## Trazabilidad y declaración de supuestos

Siguiendo la consigna 4.2, todo lo que el perfil afirma sobre su usuario puede rastrearse a algún documento del TP1 (SRS, DFD, casos de uso o historias de usuario) **o** queda explícitamente marcado como **supuesto del grupo** cuando el TP1 no lo cubre. Dentro del perfil, los supuestos se marcan con la etiqueta "**Supuesto del grupo**" al final de la afirmación.
