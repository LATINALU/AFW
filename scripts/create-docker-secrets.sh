#!/bin/bash
# ATP v0.8.0 - Crear Docker Secrets
# Generado: 2026-01-21 20:24:07

echo 'U3Y2CZJZbANwupSEM5cyTNI7t6eg1ZifNaqvsZLWb02-U12z015VtZgeUf21zkIFiAIkSzdGXBkd7ix2-i8s8Q' | docker secret create jwt_secret -
echo 'luax9LHPgp35gi-FAbvW2kbWVtOHpbVXfgw0_BrcIdnTX2btxPLuLur_bPXlzDYFUF4JTlOnVRKVuPxlMItBRw' | docker secret create session_secret -
echo '5b6b44ea7efa669c50d68f7423d09b125d46b3b9aa1d74284f12dfe2044d3659' | docker secret create encryption_key -
echo '9e900471540efa74068aeaf6c6012e1e39c43863a94258be1d1d7ad2c69abcbe' | docker secret create redis_key -
echo '$Wvw@A<H+%5C4&kjX[+b^Fj[' | docker secret create db_password -

echo '✅ Todos los secrets de Docker creados'
