# 1. Clonar el proyecto
git clone https://github.com/tuusuario/tu-repo.git
cd tu-repo

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la app
uvicorn main:app --reload

