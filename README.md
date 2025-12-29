# Monorepo – Visión General, Organización y Filosofía

## 1. Propósito del monorepo

Este monorepo existe para **centralizar, orquestar y estandarizar** el desarrollo de múltiples proyectos y aplicaciones que comparten:

* Infraestructura
* Herramientas de migración de base de datos
* Convenciones técnicas
* Flujos de CI/CD
* Filosofía de automatización

El objetivo principal **no es solo ejecutar código**, sino **reducir la carga cognitiva**, preservar contexto y permitir que el desarrollo escale sin que la mente humana se convierta en el cuello de botella.

Este repositorio está pensado para ser entendido no solo por desarrolladores humanos, sino también por **LLMs y agentes automáticos**, que deben poder obtener contexto rápidamente y operar con seguridad.

---

## 2. Principios rectores

1. **Separación clara de responsabilidades**

   * Las herramientas no deben conocerse entre sí más de lo estrictamente necesario.
   * El orquestador coordina, las herramientas ejecutan.

2. **Contexto explícito > Conocimiento implícito**

   * Las reglas del sistema deben vivir en archivos, no en la cabeza del desarrollador.

3. **Automatización progresiva y modular**

   * Primero scripts simples
   * Luego micro‑agentes
   * Nunca magia

4. **Idempotencia y reproducibilidad**

   * Cualquier entorno debe poder reconstruirse desde cero.

5. **Optimización del ciclo de feedback**

   * Cambios pequeños
   * Migraciones incrementales
   * Validación inmediata

---

## 3. Organización por carpetas (alto nivel)

```
monorepo/
│
├── orchestrator/
│   ├── scripts/
│   ├── agents/
│   ├── registry/
│   └── docs/
│
├── projects/
│   ├── proyecto_a/
│   │   └──proyecto_a/
│   │       ├── apps/
│   │       ├── docker/
│   │       └── liquibase/
│   └── proyecto_b/
│
├── docker/
│   ├── postgres/
│   └── liquibase/
│
├── ci/
│   └── gitlab/
│
└── README.md
```

---

## 4. El orquestador (pieza central)

El **orquestador** es el "director supremo" del monorepo.

### Responsabilidades

* Conocer **qué proyectos existen**
* Conocer **qué apps componen cada proyecto**
* Decidir **qué cambios aplicar y dónde**
* Coordinar herramientas externas (Liquibase, Docker, CI)

### Lo que NO hace

* No define lógica de negocio
* No contiene SQL ni XML de migraciones
* No ejecuta cambios directamente sin delegar

### Registry

El `registry`:

* Es una **fuente de verdad** del monorepo
* Define relaciones entre proyectos, apps y bases de datos
* **No pertenece a Liquibase** ni a Docker
* Es consumido por el orquestador

---

## 5. Liquibase

Liquibase se utiliza como **motor de migraciones de base de datos**.

### Filosofía de uso

* Migraciones **incrementales**
* Nunca destructivas por defecto
* Cambios pequeños y explícitos

### Organización

* Cada app posee sus propios changelogs
* Existen master changelogs generados automáticamente
* Liquibase **no conoce el registry**

Liquibase recibe:

* Un changelog
* Una base de datos

El *qué* y el *dónde* son decisiones del orquestador.

---

## 6. Docker

Docker se utiliza para:

* Bases de datos locales
* Ejecución aislada de Liquibase
* Reproducibilidad total del entorno

### Beneficios clave

* Ciclo de feedback extremadamente corto
* Desarrollo local idéntico a CI
* Eliminación de dependencias globales

El patrón buscado es:

> *Modificar changelog → ejecutar Liquibase → ver el cambio inmediatamente*

---

## 7. Integración con GitLab CI

GitLab CI se utiliza como:

* Verificador de consistencia
* Ejecutor automático de migraciones
* Guardia de integridad del monorepo

### Principios

* Lo que corre en CI debe poder correrse localmente
* Ninguna magia específica de CI
* Variables sensibles desacopladas del código

---

## 8. Scripts

Los scripts son **herramientas determinísticas**.

### Características

* Entrada y salida clara
* Sin razonamiento complejo
* Repetibles
* Predecibles

### Uso típico

* Generar estructuras de carpetas
* Validar estado del repo
* Invocar herramientas externas

Cuando un script comienza a requerir:

* heurísticas
* interpretación
* contexto amplio

➡️ deja de ser script y pasa a ser micro‑agente.

---

## 9. Micro‑agentes

Los micro‑agentes son unidades de automatización **ligeramente inteligentes**.

### Qué son

* Más que una función
* Mucho menos que un sistema autónomo
* Especialistas en tareas acotadas

### Qué hacen

* Aplican reglas existentes
* Interpretan contexto local
* Explican decisiones
* Dejan TODOs cuando hay ambigüedad

### Qué NO hacen

* No crean políticas nuevas
* No toman decisiones globales
* No modifican el registry sin supervisión

### Ejemplos

* Modelo → changelog Liquibase
* App nueva → estructura + registro
* Sincronización de master changelogs

---

## 10. Filosofía general

Este monorepo está diseñado para:

* Proteger la capacidad cognitiva del desarrollador
* Externalizar decisiones repetitivas
* Permitir que humanos y LLMs colaboren

La automatización no busca reemplazar criterio humano, sino:

> **liberar al humano para pensar en problemas de mayor alcance**

---

## 11. Posibles mejoras futuras

* Agentes con memoria local (design docs)
* Validadores automáticos de consistencia
* Simulación de impacto de migraciones
* Generación asistida de documentación
* Orquestación multi‑cliente / multi‑entorno

---

## 12. Resumen ejecutivo

Este monorepo no es solo un repositorio de código.

Es un **sistema de coordinación** entre:

* proyectos
* herramientas
* personas
* agentes

Diseñado para escalar **en complejidad sin escalar en caos**.
