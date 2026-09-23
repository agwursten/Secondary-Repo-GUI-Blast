# LocalBlast_2026

## Integrantes
* Farias Valentin
* Gaitan Agustin Facundo
* Wursten Augusto

---
## Estructura del Repositorio

````
LocalBlast_2026/
├── .gitignore
├── README.md
└── docs/
    ├── architecture/
    │   └── contexto-inicial.md
    ├── requeriments/
    │   ├── casos-de-uso.md
    │   ├── historias-usuario.md
    │   ├── modelo-dominio.md
    │   └── srs.md
    └── uso-ia.md
````

## 1. Canvas de Descubrimiento (Síntesis)

### Problema
Actualmente, la realización de alineamientos locales de secuencias mediante BLAST presenta barreras de entrada significativas según el canal utilizado:
* **Línea de comandos (Consola):** Requiere recordar comandos complejos, sintaxis rigurosa y navegar por documentación extensa, lo que ralentiza el trabajo de usuarios sin perfil puramente bioinformático o técnico.
* **Interfaz Web Oficial (NCBI BLAST):** Aunque es accesible, carece de opciones avanzadas de filtrado directo e interactivo (como filtros instantáneos por % de identidad o cobertura posterior a la búsqueda) y resulta sobrecargada para consultas simples y rápidas.

### Stakeholders
* **Estudiantes de Grado y Posgrado:** Que necesitan realizar alineamientos locales rápidos para trabajos prácticos o investigación sin perder tiempo en la configuración de entornos por terminal.
* **Investigadores y Docentes de Bioinformática / Biología Molecular:** Que buscan una herramienta ágil e intuitiva para explorar resultados con filtros visuales personalizados que no están disponibles de forma nativa en la web tradicional.

### Alcance del Proyecto
* **Interfaz Gráfica Intuitiva:** Diseño web o desktop amigable para la introducción de secuencias query (FASTA/texto plano) y configuración simple de parámetros.
* **Integración con Motor BLAST:** Capacidad de enviar consultas y recibir resultados conectándose a NCBI (vía API/remoto) o ejecutables de BLAST local.
* **Filtros Avanzados y Personalizados:** Opciones de visualización y filtrado dinámico sobre la lista de resultados (ej. umbrales de identidad, cobertura, E-value, taxones).
* **Exportación de Resultados:** Descarga de resultados filtrados en formatos estándar (CSV, JSON, FASTA).

#### Fuera del Alcance (Out of Scope)
* Reescritura o modificación del algoritmo de alineamiento subyacente de BLAST.
* Implementación de herramientas de alineamiento múltiple (como ClustalW o Muscle) o modelado 3D de estructuras.
* **Administración de bases de datos locales desde la aplicación (rol Administrador).** El diseño integral del sistema contempla un rol Administrador que dé de alta, actualice y baje bases de datos BLAST locales a partir de archivos FASTA. Esta capacidad **se documenta a nivel de diagramas** (DFD Nivel 0/1, modelo de dominio) para dejar la visión completa del producto, pero **queda fuera del alcance de este cuatrimestre** por restricciones de tiempo: no se profundiza como casos de uso ni historias de usuario, no tiene requerimientos funcionales asociados y no se implementará. Para las historias de usuario del modo local se asume que ya existe al menos una base de datos cargada en el catálogo.

---

## 2. Documentación del Proyecto
Para consultar la Especificación de Requisitos de Software (SRS) completa, visión, casos de uso y escenarios de calidad, diríjase a:
👉 [`docs/requeriments/srs.md`](docs/requeriments/srs.md)

---

## 3. Modelo de Ciclo de Vida Específico

El grupo se decanta por una **metodologia incremental con practicas agiles**. 

Esta elección se basa en que la herramienta posee características
funcionales intrínsecas que se pueden modularizar naturalmente.
Donde es posible la entrega de un modulo operativo cuyo desarrollo
es independiente de otros del mismo sistema (Por ejemplo, *procesar_secuencia*). 

Cada incremento añade una capacidad operativa completa y utilizable.

• Descartamos enfoques como *Cascada* dado que es un flujo estrictamente secuencial, donde no se avanza a la siguiente fase sin cerrar por completo al anterior, lo cual no es caracteristico de este proyecto dado que como bien mencionamos es posible separar responsabilidades. 

• Descartamos enfoques como *Modelo en V* porque es en parte una variacion del metodo en cascada. 

• Descartamos enfoques como *Espiral* dado que esta pensado para proyectos más grandes en donde un fallo implica consecuencias catastroficas y por eso
se deben llevar a cabo gestion de riesgos, en un proyecto como el presente añadir la complejidad de un modelo en espiral supera ampliamente la complejidad del software en si, lo que ralentiza el desarrollo.

• Descartamos enfoques como *iterativo* debido a que obligaria a rehacer todo
el sistema en cada ciclo, lo cual es ineficiente cuando **ya contamos con requisitos bien definidos**. Por lo que no seria necesario primero desarrollar un esqueleto basico del sistema para luego ir refinandolo, sino que al conocer bien los requisitos podemos simplemente construir un modulo dejandolo listo para produccion y luego construir el siguiente. 


