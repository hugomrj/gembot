import os
import time
import json
from bottle import static_file
from bottle import Bottle, request, response, hook, JSONPlugin
from app.services import analyze_question_with_ai, generate_rag_response, get_ia_response

app = Bottle()

# Plugin JSON con formato bonito y UTF-8
app.install(JSONPlugin(json_dumps=lambda s: json.dumps(s, indent=2, ensure_ascii=False)))

# BASE_DIR = carpeta donde está app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# STATIC_DIR = carpeta "static" al mismo nivel que "app"
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")


def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, Authorization'
        if request.method == 'OPTIONS':
            return {}
        return fn(*args, **kwargs)
    return _enable_cors


# Ruta principal
@app.route('/')
@enable_cors
def hello_world():
    return 'Hello from Bottle!'

# Endpoint de generación de texto
@app.post('/generate/')
def generate_text_with_gemma():
    try:
        data = request.json
        if not data or 'prompt' not in data:
            response.status = 400
            return {"error": "Falta el campo 'prompt'"}

        prompt = data['prompt']
        gemma_output = get_ia_response(prompt)
        return {"response": gemma_output}

    except Exception as e:
        response.status = 500
        return {"error": f"Error al generar contenido con Gemma: {str(e)}"}




@app.post('/generate_rag')
def generate_response():
    """
    Endpoint para generación de respuestas RAG
    """
    try:
        # 1. Validar datos de entrada
        data = request.json
        print(data)  # Debug

        if not data or 'user_query' not in data:
            response.status = 400
            return json.dumps({
                "error": "Se requiere 'user_query' en el JSON",
                "ejemplo": {
                    "user_query": "¿Cuántos días de vacaciones tengo?",
                    "context": "Opcional",
                    "datos": "Opcional"
                }
            })

        # 2. Extraer datos del JSON
        user_query = data['user_query']
        context = data.get('context', '')
        datos = data.get('datos', '')  # <- Nuevo campo opcional

        # 3. Generar respuesta
        rag_response = generate_rag_response(user_query, context, datos)


        # 4. Respuesta HTTP
        response.content_type = 'application/json'
        return json.dumps({
            "response": rag_response
        })

    except Exception as e:
        response.status = 500
        return json.dumps({"error": f"Error interno: {str(e)}"})











@app.post('/analyze_question/')
def analyze_question():
    try:
        data = request.json
        if not data or 'question' not in data:
            response.status = 400
            return {"error": "El campo 'question' es requerido"}

        user_question = data['question'].strip()  # Added strip() to clean input
        if not user_question:  # Check for empty string after stripping
            response.status = 400
            return {"error": "La pregunta no puede estar vacía"}

        analysis_result = analyze_question_with_ai(user_question)

        response.content_type = 'application/json; charset=utf-8'
        return json.dumps(analysis_result, indent=2, ensure_ascii=False) + "\n"

    except ValueError as e:
        response.status = 400
        return {"error": f"Error en el formato de datos: {str(e)}"}
    except Exception as e:
        response.status = 500
        return {"error": f"Error interno al procesar la pregunta: {str(e)}", "details": str(type(e))}





# Ruta de salud
@app.route('/health')
def health_check():
    return {"status": "ok"}

# Ruta de prueba
@app.route('/ping')
def ping():
    start = time.time()
    end = time.time()
    return {
        "message": "pong",
        "response_time_ms": round((end - start) * 1000, 2)
    }


@app.route('/tester')
def serve_tester():
    file_path = os.path.join(STATIC_DIR, "test_api.html")
    if not os.path.exists(file_path):
        return {"error": f"No se encontró el archivo en {file_path}"}
    return static_file("test_api.html", root=STATIC_DIR)

# Para PythonAnywhere
application = app