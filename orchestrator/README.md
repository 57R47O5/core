# Orchestrator

El **orchestrator** es el núcleo operativo y director supremo del monorepo.  
Su función es **entender, validar y coordinar** la estructura del repositorio, los proyectos y las herramientas auxiliares (Liquibase, Docker, CI/CD, scripts y micro-agentes), actuando como único punto de entrada para cualquier operación relevante sobre el sistema.

El orquestador no implementa lógica de negocio ni reemplaza a las herramientas existentes:
las gobierna, las sincroniza y las ejecuta.

Está diseñado para:
- Reducir la carga cognitiva del desarrollador
- Centralizar el contexto estructural y operativo del monorepo
- Permitir automatización incremental, segura y trazable
- Servir como punto de entrada único para scripts, agentes y pipelines
- Proveer contexto rápido y confiable a humanos y LLMs

---

## Principios fundamentales

- Punto único de entrada
Ninguna herramienta (Liquibase, Django, CI, scripts) se ejecuta directamente:
todo pasa por el orquestador.

- Docker como lenguaje de ejecución
El orquestador decide qué hacer; Docker (y Docker Compose) es cómo se ejecuta.

- Separación de decisión y ejecución
El orquestador toma decisiones; las herramientas solo actúan.

-  Automatización progresiva
El sistema crece de forma orgánica, sin intentar resolver todo desde el inicio.

- Contexto explícito > convenciones implícitas
Las reglas del sistema viven en código y documentos, no en la memoria humana.

---

## Objetivos

- Validar la coherencia estructural del monorepo
- Convertir convenciones implícitas en reglas explícitas
- Centralizar el conocimiento sobre proyectos, apps y dependencias
- Automatizar tareas repetitivas de bajo valor cognitivo
- Facilitar la incorporación de agentes especializados
- Proveer contexto rápido a humanos y LLMs
- Orquestar la creación, actualización y destrucción de recursos del sistema


---
## Rol del orquestador en el monorepo

Actualmente, el orquestador asume los siguientes roles:

1-  Generación y desmontaje de proyectos

    - Crear estructuras de proyectos
    - Actualizar el registry
    - Mantener coherencia entre filesystem y definición declarativa

2- Validación del registry

    - Verificar consistencia entre proyectos, apps y settings
    - Detectar errores estructurales temprano

3- Orquestación de migraciones y bases de datos

    - Usar el registry para decidir qué bases de datos crear o actualizar
    - Indicar a Liquibase qué ejecutar y dónde hacerlo
    -  Liquibase es una herramienta ejecutada, no un decisor

Estos roles crecerán de forma incremental conforme madure el sistema.


---

## Docker Compose como herramienta central

El orquestador utiliza Docker Compose como lenguaje declarativo de ejecución.

Esto implica que:

- El orquestador genera o selecciona archivos docker-compose
- Decide qué servicios levantar, con qué configuración y en qué contexto

- Docker se convierte en el mecanismo unificador para:

-- Migraciones
-- Inicialización de bases de datos
-- Servicios de backend y frontend (a futuro)
-- Testing y CI

Liquibase, Django y otras herramientas no conocen el monorepo:
son ejecutadas dentro de contenedores definidos por el orquestador.

## Organización de carpetas

```text
orchestrator/
├── scripts/    # Scripts simples, deterministas, ejecutables por CLI
├── agents/     # Micro-agentes con lógica contextual (más que funciones)
├── registry/   # Definiciones declarativas del sistema (fuente de verdad)
└── docs/       # Documentación técnica y de diseño
```

## Scripts vs agentes

### Scripts

- Deterministas
- Bajo contexto
- Fáciles de testear
- Ideales para validaciones y tareas mecánicas

### Micro-agentes

- Operan con mayor contexto
- Encapsulan decisiones no triviales
- Reducen la carga cognitiva humana
- Se diseñan como “funciones inteligentes”
- Son componibles y evolutivos

El orquestador decide cuándo una tarea debe ser script o agente.

## Evolución prevista

### A futuro, el orquestador podrá:

- Orquestar múltiples entornos (dev / test / prod)
- Coordinar Django, React y servicios auxiliares vía Docker
- Ejecutar tests y pipelines locales
- Delegar tareas complejas a micro-agentes especializados
- Servir como interfaz estable para LLMs con contexto persistente
- El crecimiento será orgánico, guiado por necesidades reales, sin sobre-ingeniería prematura.