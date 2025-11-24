# Script para Windows PowerShell: construir frontend Svelte y arrancar Flask
# Uso: abre PowerShell en esta carpeta y ejecuta: .\run_all.ps1

# Comprueba que Node y npm están disponibles
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js no está instalado o 'node' no está en PATH. Instala Node.js antes de continuar."
    exit 1
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Error "npm no está disponible. Instala Node.js (incluye npm)."
    exit 1
}

# Moverse al frontend y construir
Push-Location -Path .\frontend_svelte
Write-Output "Instalando dependencias en frontend_svelte (usando --legacy-peer-deps)..."
npm install --legacy-peer-deps
if ($LASTEXITCODE -ne 0) { Write-Error "npm install falló"; Pop-Location; exit 1 }

Write-Output "Construyendo frontend (npm run build)..."
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Warning "npm run build falló, intentando 'npx vite build' como fallback..."
    npx vite build
    if ($LASTEXITCODE -ne 0) { Write-Error "npx vite build falló"; Pop-Location; exit 1 }
}

Pop-Location

# Ejecutar Flask
Write-Output "Iniciando backend Flask..."
python .\app.py

# Nota: Flask correrá en primer plano. Detén con Ctrl+C cuando quieras.
