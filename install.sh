#!/bin/bash

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

INSTALL_DIR="$HOME/.local/share/goes19-wallpaper-live"
SERVICE_NAME="goes19-wallpaper-live"

echo -e "${BLUE}=== Instalador de GOES-19 Live Wallpaper ===${NC}"

# 1. Verificar dependencias del sistema
echo -e "${GREEN}[+] Verificando dependencias del sistema...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python3 no está instalado.${NC}"
    exit 1
fi

# 2. Crear directorio de instalación
echo -e "${GREEN}[+] Creando directorio en $INSTALL_DIR...${NC}"
mkdir -p "$INSTALL_DIR"
cp src/main.py "$INSTALL_DIR/main.py"
cp requirements.txt "$INSTALL_DIR/requirements.txt"

# 3. Crear entorno virtual (venv)
echo -e "${GREEN}[+] Configurando entorno virtual Python...${NC}"
python3 -m venv "$INSTALL_DIR/venv"
source "$INSTALL_DIR/venv/bin/activate"

# 4. Instalar librerías
echo -e "${GREEN}[+] Instalando librerías necesarias...${NC}"
pip install -r "$INSTALL_DIR/requirements.txt"
deactivate

# 5. Crear servicio Systemd (User)
echo -e "${GREEN}[+] Creando servicios systemd (user)...${NC}"
mkdir -p "$HOME/.config/systemd/user"

# Archivo .service
cat <<EOF > "$HOME/.config/systemd/user/$SERVICE_NAME.service"
[Unit]
Description=Actualizar fondo de pantalla GOES-19
After=network.target

[Service]
Type=oneshot
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/main.py
Environment=DISPLAY=:0
Environment=XDG_RUNTIME_DIR=/run/user/$(id -u)
EOF

# Archivo .timer (Ejecuta cada 15 min)
cat <<EOF > "$HOME/.config/systemd/user/$SERVICE_NAME.timer"
[Unit]
Description=Ejecutar GOES-19 Wallpaper cada 15 minutos

[Timer]
OnCalendar=*:0/15
Persistent=true

[Install]
WantedBy=timers.target
EOF

# 6. Activar y Recargar
echo -e "${GREEN}[+] Activando timer...${NC}"
systemctl --user daemon-reload
systemctl --user enable --now "$SERVICE_NAME.timer"

# 7. Ejecución de prueba
echo -e "${BLUE}[+] Ejecutando primera prueba...${NC}"
"$INSTALL_DIR/venv/bin/python" "$INSTALL_DIR/main.py"

echo -e "${GREEN}=== Instalación Completada ===${NC}"
echo "El fondo se actualizará automáticamente cada 15 minutos."
echo "Puedes ver los logs con: journalctl --user -u $SERVICE_NAME"