function Initialize-FrontendApps {
    param (
        [Parameter(Mandatory)]
        [string]$FrontendPath
    )

    $srcPath  = Join-Path $FrontendPath "src"
    $appsPath = Join-Path $srcPath "apps"

    if (-not (Test-Path $srcPath)) {
        throw "No se encontró src/ en el frontend"
    }

    if (-not (Test-Path $appsPath)) {
        New-Item -ItemType Directory -Path $appsPath | Out-Null
    }

    # --------------------------------------------------
    # Contenido congelado de App.jsx
    # --------------------------------------------------
    $appsJsxContent = @"
import { BrowserRouter, Routes, Route } from "react-router-dom";
import apps from "./apps/apps.registry";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {apps.flatMap(app =>
          app.routes.map(route => (
            <Route
              key={route.path}
              path={route.path}
              element={route.element}
            />
          ))
        )}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
"@

    # --------------------------------------------------
    # Contenido inicial del registry (solo base)
    # --------------------------------------------------
    $registryContent = @"
import base from "@apps/base";

export default [
  base,
];
"@

    # --------------------------------------------------
    # Escritura de archivos
    # --------------------------------------------------
    $appsJsxPath = Join-Path $srcPath "App.jsx"
    Set-Content -Path $appsJsxPath -Value $appsJsxContent -Encoding UTF8

    $registryPath = Join-Path $appsPath "apps.registry.js"
    Set-Content -Path $registryPath -Value $registryContent -Encoding UTF8

    Write-Host "App.jsx y apps.registry.js generados correctamente"
}
