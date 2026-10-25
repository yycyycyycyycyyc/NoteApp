$ErrorActionPreference = "Stop"
$certDirectory = Join-Path $PSScriptRoot "nginx\certs"
New-Item -ItemType Directory -Force -Path $certDirectory | Out-Null

$keyPath = Join-Path $certDirectory "notesapp.key"
$certPath = Join-Path $certDirectory "notesapp.crt"
if ((Test-Path $keyPath) -and (Test-Path $certPath)) {
    Write-Host "Certificate pair already exists in nginx/certs."
    exit 0
}

docker run --rm `
    -v "${certDirectory}:/certs" `
    alpine/openssl req -x509 -newkey rsa:2048 -sha256 -days 365 -nodes `
    -keyout /certs/notesapp.key -out /certs/notesapp.crt `
    -subj "/CN=localhost" `
    -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

if ($LASTEXITCODE -ne 0) { throw "Certificate generation failed." }
Write-Host "Created a local self-signed certificate for localhost."
