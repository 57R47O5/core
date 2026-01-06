# 📚 Bibliotecario del Orquestador

El **Bibliotecario** es el agente responsable de **conocer, describir, validar y sincronizar** el estado estructural de los proyectos del monorepo. Actúa como la *fuente de verdad* (source of truth) para el orco y para cualquier otro agente que necesite información confiable sobre proyectos, apps y su coherencia.

Su objetivo principal es **reducir incertidumbre** y **acortar ciclos de realimentación**, convirtiendo el filesystem real en un **registry explícito**, validable y versionable.

---

## 🎯 Responsabilidades

El bibliotecario:

* Descubre qué proyectos existen realmente
* Detecta qué apps usa cada proyecto
* Genera un **registry estructural** (`registry.json`)
* Valida que el registry tenga un esquema correcto
* Valida proyectos reales contra:

  * su *spec*
  * el *registry*
* Detecta desvíos (drift) entre filesystem y registry
* Informa al orco si el estado está sincronizado o no

El bibliotecario **no crea proyectos**, **no ejecuta servicios**, **no decide políticas**. Solo observa, describe y valida.

---

## 🗂️ Registry

El registry es un archivo JSON ubicado en:

```
orchestrator/registry/registry.json
```

### Esquema actual

```json
{
  "projects": {
    "elecciones": {
      "apps": ["base"]
    },
    "carteles": {
      "apps": ["base"]
    }
  }
}
```

Este archivo representa el **contrato estructural** del monorepo.

---

## 🧩 Funciones del Bibliotecario

### 1️⃣ `Get-OrcProjectSpec`

Define la *especificación esperada* de un proyecto, independientemente de si existe o no.

```powershell
Get-OrcProjectSpec -Project elecciones
```

Devuelve:

* Nombre del proyecto
* Paths esperados (backend / frontend)

Se usa como base para validaciones estructurales.

---

### 2️⃣ `New-OrcRegistry`

Genera el registry **a partir del estado real del filesystem**.

```powershell
New-OrcRegistry -RepoRoot C:\repo
```

Qué hace:

* Recorre `backend/projects`
* Recorre `backend/apps`
* Inspecciona `settings.py` de cada proyecto
* Detecta apps usadas
* Genera `registry.json`

Es **determinístico**: mismo filesystem → mismo registry.

---

### 3️⃣ `Test-OrcProjectAgainstSpec`

Valida un proyecto contra su *spec* estructural.

```powershell
Test-OrcProjectAgainstSpec -Project elecciones -RepoRoot C:\repo
```

Valida:

* Existencia en registry
* Existencia de paths esperados

Devuelve un objeto estructurado con:

* checks por path
* validez global

---

### 4️⃣ `Test-OrcRegistry`

Valida que el registry:

* Exista
* Sea JSON válido
* Cumpla el esquema mínimo esperado

```powershell
Test-OrcRegistry -RepoRoot C:\repo
```

Valida por proyecto:

* Presencia de `apps`
* Tipo correcto

Es el *lint* del registry.

---

### 5️⃣ `Sync-OrcRegistry`

Sincroniza el registry con el filesystem.

```powershell
Sync-OrcRegistry -RepoRoot C:\repo
```

Qué hace:

* Genera un registry nuevo en memoria
* Compara contra el registry existente
* Detecta:

  * proyectos agregados
  * proyectos removidos
  * proyectos modificados

Con `-Write`, escribe los cambios.

```powershell
Sync-OrcRegistry -RepoRoot C:\repo -Write
```

Devuelve un resumen de cambios (diff estructural).

---

### 6️⃣ `Test-OrcProjectAgainstRegistry`

Valida un proyecto real contra el **contrato declarado en el registry**.

```powershell
Test-OrcProjectAgainstRegistry -Project elecciones -RepoRoot C:\repo
```

Valida:

* Que el proyecto exista en el registry
* Que existan sus paths reales
* Que existan las apps declaradas

Clasifica resultados en:

* Errors (rompen validez)
* Warnings (desvíos tolerables)

Esta función convierte al registry en un **contrato ejecutable**.

---

## 🔁 Ciclos de uso típicos

### Flujo de desarrollo

1. Crear / modificar proyectos
2. `Sync-OrcRegistry`
3. `Test-OrcRegistry`
4. `Test-OrcProjectAgainstRegistry`
5. Orco decide acciones (Liquibase, up, down, etc.)

---

## 🧠 Filosofía

* El filesystem es *realidad*
* El registry es *modelo*
* El bibliotecario detecta divergencias
* El orco decide qué hacer con esa información

Separar observación de acción mantiene el sistema **simple, extensible y testeable**.

---

## 🚀 Próximos usos naturales

* Generación dinámica de `liquibase.properties`
* `orc status`
* `orc doctor`
* Validaciones pre-deploy
* Migraciones seguras

El bibliotecario ya está listo para sostenerlos.
