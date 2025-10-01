# --------------------------------------------
# 1. Imagen base con Python 3.11
# --------------------------------------------
FROM python:3.11-slim

# Evitar interacciones al instalar
ENV DEBIAN_FRONTEND=noninteractive

# --------------------------------------------
# 2. Instalar dependencias del sistema
# --------------------------------------------
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    # Dependencias para Chrome Headless
    libnss3 \
    libatk-bridge2.0-0 \
    libfontconfig1 \
    libxss1 \
    libasound2 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libgtk-3-0 \
    # Dependencias para audio/voz
    libespeak-ng1 \
    libportaudio2 \
    # Instalación de Google Chrome estable
    && wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i /tmp/chrome.deb || apt-get install -fy \
    && rm /tmp/chrome.deb \
    # Limpiar para reducir tamaño final
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------
# 3. Crear directorio de trabajo
# --------------------------------------------
WORKDIR /app

# --------------------------------------------
# 4. Copiar e instalar dependencias de Python
# --------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# --------------------------------------------
# 5. Copiar el código fuente de la aplicación
# --------------------------------------------
COPY . .

# --------------------------------------------
# 6. Exponer puerto de la API (FastAPI)
# --------------------------------------------
EXPOSE 8000

# --------------------------------------------
# 7. Comando para lanzar FastAPI con Uvicorn
# Asegúrate de que el archivo se llame 'main.py' y tenga 'app = FastAPI()'
# Si tu app está en otro archivo, cambialo por 'archivo:app'
# --------------------------------------------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
