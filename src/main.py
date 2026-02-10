#!/usr/bin/env python3
import os
import re
import sys
import subprocess
import requests
from datetime import datetime
from PIL import Image

# --- CONFIGURACIÓN ---
BASE_URL = "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/SECTOR/ssa/GEOCOLOR/"
FILE_PATTERN = r'(\d{11}_GOES19-ABI-ssa-GEOCOLOR-1800x1080\.jpg)'
SAVE_PATH = os.path.expanduser("~/.cache/wallpaper_goes19.jpg")

# Si tu monitor es 1080p, esto asegura que quede perfecto
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def get_latest_url():
    try:
        log(f"Buscando en {BASE_URL}...")
        res = requests.get(BASE_URL, timeout=10)
        res.raise_for_status()
        
        matches = re.findall(FILE_PATTERN, res.text)
        if not matches:
            log("No se encontraron imágenes con el patrón solicitado.")
            return None
            
        # Ordenamos y tomamos el último (el más reciente)
        latest_file = sorted(list(set(matches)))[-1]
        return f"{BASE_URL}{latest_file}"
    except Exception as e:
        log(f"Error obteniendo URL: {e}")
        return None

def download_and_process(url):
    try:
        log(f"Descargando {url}...")
        res = requests.get(url, stream=True)
        if res.status_code != 200:
            return None

        # Guardar en memoria temporal
        temp_file = "/tmp/goes19_temp.jpg"
        with open(temp_file, 'wb') as f:
            for chunk in res.iter_content(1024):
                f.write(chunk)
        
        # Procesar con Pillow (Centrar en fondo negro)
        img = Image.open(temp_file)
        bg = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), "black")
        
        # Centrar la imagen 1800x1080 en el canvas 1920x1080
        x = (SCREEN_WIDTH - img.width) // 2
        y = (SCREEN_HEIGHT - img.height) // 2
        bg.paste(img, (x, y))
        
        bg.save(SAVE_PATH, quality=95)
        log(f"Imagen procesada guardada en {SAVE_PATH}")
        return SAVE_PATH
    except Exception as e:
        log(f"Error procesando imagen: {e}")
        return None

def set_wallpaper(path):
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    uri = f"file://{path}"
    
    try:
        if "gnome" in desktop:
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri])
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", uri])
        elif "kde" in desktop:
            # KDE Plasma 5/6 script via qdbus
            script = f"""
            var allDesktops = desktops();
            for (i=0;i<allDesktops.length;i++) {{
                d = allDesktops[i];
                d.wallpaperPlugin = "org.kde.image";
                d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
                d.writeConfig("Image", "{path}");
            }}
            """
            subprocess.run(["qdbus", "org.kde.plasmashell", "/PlasmaShell", "org.kde.PlasmaShell.evaluateScript", script])
        else:
            # Fallback para i3, bspwm, xfce, etc.
            subprocess.run(["feh", "--bg-scale", path])
        log("Wallpaper actualizado.")
    except Exception as e:
        log(f"Error configurando entorno gráfico: {e}")

if __name__ == "__main__":
    url = get_latest_url()
    if url:
        local_path = download_and_process(url)
        if local_path:
            set_wallpaper(local_path)