# Gembot API

API de prueba hecha con Bottle.

## 🚀 Requisitos

- Python 3.7 o superior
- pip

## ⚙️ Instalación y ejecución

```bash
# Clonar el repositorio (si corresponde)
git clone https://github.com/hugomrj/gembot
cd gembot

# Crear entorno virtual
python3 -m venv venv

# Activar el entorno virtual
# En Linux/macOS:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt


# Configuración inicial

Crear el archivo `app/google_keys.json` con el siguiente contenido, reemplazando "api_key" por tu clave real:

{
    "GOOGLE_API_KEYS": [
        "api_key"
    ]
}




# Ejecutar local
python run.py






# probar
curl -X POST http://localhost:3000/generate/ \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hola, ¿cómo estás?"}'


curl -X POST http://localhost:3000/analyze_question/ \
  -H "Content-Type: application/json" \
  -d '{"question":"Cómo buscar laptops gamers bajo $1000"}'