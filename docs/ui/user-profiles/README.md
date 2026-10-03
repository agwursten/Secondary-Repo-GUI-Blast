# Perfiles de usuario — LocalBlast

Esta carpeta contiene los perfiles de usuario que guían el maquetado de la interfaz (sección 4.1 del TP2 Parte B). Cada perfil incluye su escenario de uso y su flujo de navegación, siguiendo lo pedido por la consigna 4.2.

## Actor principal del TP1

El TP1 identifica dos actores humanos del sistema (ver [SRS §2.2](../../requeriments/srs.md#22-actores-del-sistema)):

- **Investigador/a** — actor principal de los procesos profundizados **P1 y P2**. Todas las historias de usuario del TP1 (HU01 a HU14) tienen a este actor como protagonista.
- **Administrador/a de bases de datos** — actor del proceso **P3**, que el TP1 declara explícitamente **fuera de alcance** (ver [SRS §1.4](../../requeriments/srs.md#14-fuera-del-alcance)): no tiene RF asociados, no tiene casos de uso detallados y no tiene historias de usuario.

En consecuencia, **el único actor principal del TP1 con historias de usuario sobre las que maquetar es "Investigador/a"**. El Administrador no se perfila en esta carpeta porque no hay HUs del TP1 que respalden pantallas para él, y la consigna 4.1 prohíbe maquetar fuera de las HUs del TP1.

El actor no humano **BLAST+** (sistema externo) no requiere perfil de usuario — no interactúa con la interfaz gráfica, es invocado por el backend.

## Dos perfiles bajo un mismo actor

El SRS distingue en [§2.1](../../requeriments/srs.md#21-stakeholders) dos **subgrupos de stakeholders** que pueden asumir el rol de Investigador/a, caracterizados de forma distinta:

- **Estudiantes de Grado y Posgrado**, que *"necesitan realizar alineamientos locales rápidos para trabajos prácticos o investigación sin perder tiempo en la configuración de entornos por terminal"*.
- **Investigadores y Docentes de Bioinformática / Biología Molecular**, que *"buscan una herramienta ágil e intuitiva para explorar resultados con filtros visuales personalizados que no están disponibles de forma nativa en la web tradicional"*.

Son el mismo actor del sistema (mismos permisos, mismas capacidades habilitadas), pero el TP1 los diferencia explícitamente en nivel de conocimiento técnico, objetivo primario frente al sistema y frustraciones con las alternativas existentes. Elaboramos un perfil por cada subgrupo para que el maquetado contemple ambas realidades sin promediarlas:

- [`investigador-estudiante.md`](investigador-estudiante.md) — perfil del Investigador/a en su subgrupo *Estudiante de grado o posgrado*.
- [`investigador-senior.md`](investigador-senior.md) — perfil del Investigador/a en su subgrupo *Investigador/a sénior o Docente de bioinformática / biología molecular*.

## Trazabilidad y declaración de supuestos

Siguiendo la consigna 4.2, todo lo que cada perfil afirma sobre su usuario puede rastrearse a algún documento del TP1 (SRS, DFD, casos de uso o historias de usuario) **o** queda explícitamente marcado como **supuesto del grupo** cuando el TP1 no lo cubre. Dentro de cada perfil, los supuestos se marcan con la etiqueta "**Supuesto del grupo**" al final de la afirmación.
