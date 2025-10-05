


![FastAPI Logo](/assets-readme/ducktalk.jpg)

🗣️ ¿Eres programador y tu patito de goma no te contesta?

¿Harto de hablar solo mientras debuggeas?
¡Tenemos la solución perfecta!

🦆 ¿Qué es DuckTalk?

DuckTalk es una extensión para Chrome y Firefox que te permite hablar con un patito virtual, curioso y atento, que está listo para que le cuentes todo lo que quieras.

---

# 👨‍💻 Tecnologías

🧠 Backend:

- 🐍 Python

- ⚡ FastAPI — Framework rápido y moderno para construir APIs

🎨 Frontend:

- 💻 JavaScript

- 🌐 HTML & CSS (para la extensión)

🗣️ Voz Preentrenada:

- 🗣 Piper TTS — Motor de texto a voz de código abierto, para darle voz al patito 🦆


## 📹 Video de demostración

[![Ver video](https://img.youtube.com/vi/dQw4w9WgXcQ/0.jpg)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

---

## 🛠️ 1.Instalación Backend

Sigue estos pasos para clonar y ejecutar el proyecto:

### Opcion 1: Modo local 🌐

#### 1. 🔽 Clonar el repositorio principal

```bash
git clone https://github.com/Cristianyelmo/DuckTalk.git 
cd DuckTalk 
```
#### 2. Crear el entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

#### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```


#### 4. Ejecutar la app

```bash
uvicorn main:app --reload
```

### Opcion 2: con Docker 🐋


#### 1. Construir imagen

```bash
docker build -t ducktalk .
```

#### 2. Ejecutar contenedor

```bash
docker run -d -p 8000:8000 ducktalk
```

## 🛠️ 2.Instalación Frontend

### App hecha con Electron ⚛️

#### 1.Entras a la carpeta Ducktalk

![FastAPI Logo](/assets-readme/electron-1.png)

#### 2.Entras a la carpeta "App-Extension" y seleccionas el sistema operativo Linux,Windows
(es un app portable es decir que haces doble click y se abre,no tenes que instalar nada)

![FastAPI Logo](/assets-readme/electron-2.png)


### Firefox 🦊

#### 1.Entrar al navegador a este link
```bash
about:debugging#/setup
```
#### 2. Entra a This Firefox

![FastAPI Logo](/assets-readme/firefox-1.png)

#### 3. Entra a Load Temporary Add-on…

![FastAPI Logo](/assets-readme/firefox-2.png)

#### 4. Entrar a la carpeta Ducktalk y entrar a "App-Extension"

![FastAPI Logo](/assets-readme/firefox-3.png)


#### 4. Una vez dentro,abri el archivo DuckTalk--Firefox.xpi

![FastAPI Logo](/assets-readme/firefox-4.png)






## ✅ ¡Listo para hablar con tu patito virtual! 🦆


















