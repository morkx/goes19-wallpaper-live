# GOES-19 Live Wallpaper 🛰️

Script automatizado para sistemas Linux que descarga la última imagen satelital del sector "Southern South America" (SSA) capturada por el satélite **GOES-19** y la establece como fondo de pantalla.

Ideal para monitorear el clima en tiempo real sobre el Cono Sur (Uruguay, Argentina, Chile, Brasil).

## Características
- 📡 Obtiene imágenes en tiempo real del CDN de NOAA.
- 🕒 **Sincronización inteligente:** Busca el último archivo disponible en el servidor, evitando errores 404 por discrepancias horarias.
- 🖼️ **Procesamiento de imagen:** Centra la imagen de 1800x1080 sobre un lienzo 1080p (Full HD) para evitar deformaciones.
- ⚙️ **Systemd Timer:** Se integra nativamente con Linux usando timers de usuario (sin necesidad de sudo ni cron sucio).
- 🐍 **Entorno aislado:** Usa `venv` para no tocar las librerías de tu sistema.


## Instalación Rápida

1. Clona este repositorio:
   ```bash
   git clone [https://github.com/tususuario/goes19-wallpaper.git](https://github.com/tususuario/goes19-wallpaper.git)
   cd goes19-wallpaper


Esto fue generado con ayuda de gemini
