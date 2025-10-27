import os, re, json, requests
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv
 
load_dotenv()
app = Flask(__name__)
 
OCR_API_KEY = os.getenv("OCR_API_KEY")
OCR_URL = "https://api.ocr.space/parse/image"
 
genai.configure()  # toma GOOGLE_APPLICATION_CREDENTIALS automáticamente
 
def limpiar_texto(texto):
    texto = re.sub(r'[^\wáéíóúÁÉÍÓÚñÑ.,:/()\-\n ]+', '', texto)
    texto = re.sub(r'\n+', '\n', texto)
    texto = re.sub(r'[ ]+', ' ', texto)
    return texto.strip()
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/upload', methods=['POST'])
def upload_image():
    texto_manual = request.form.get('texto_manual')
    if texto_manual:
        return jsonify({'texto_ocr': limpiar_texto(texto_manual)})
 
    if 'image' not in request.files:
        return jsonify({'error': 'No se subió ninguna imagen'}), 400
 
    image = request.files['image']
    try:
        payload = {'apikey': OCR_API_KEY, 'language': 'spa'}
        files = {'file': (image.filename, image.stream, image.mimetype)}
        ocr_resp = requests.post(OCR_URL, data=payload, files=files, timeout=60)
        ocr_json = ocr_resp.json()
        texto = ocr_json["ParsedResults"][0].get("ParsedText", "").strip()
    except Exception as e:
        return jsonify({'error': 'Error OCR', 'detalle': str(e), 'ocr_json': ocr_resp.text}), 500
 
    return jsonify({'texto_ocr': limpiar_texto(texto)})
 
@app.route('/procesar_ia', methods=['POST'])
def procesar_ia():
    texto = request.form.get('texto_manual')
    accion = request.form.get('accion', '')
    if not texto:
        return jsonify({'error': 'No se recibió texto para procesar'}), 400
 
    texto_limpio = limpiar_texto(texto)
 
    if accion:
        prompt = f"Texto original: {texto_limpio}\nAcción solicitada: {accion}\nResponde acorde a la acción solicitada."
    else:
        prompt = f"Texto original: {texto_limpio}\nEres un asistente experto. Indica qué se puede hacer con este texto."
 
    try:
        modelo = genai.GenerativeModel("gemini-2.5-flash")
        respuesta = modelo.generate_content(prompt)
        texto_gemini = respuesta.text
        print("Texto Gemini:", texto_gemini)
    except Exception as e:
        return jsonify({'error': 'Error Gemini', 'detalle': str(e)}), 500
 
    try:
        parsed = json.loads(texto_gemini)
    except Exception:
        parsed = {
            "texto_bruto": texto_gemini,
            "accion": accion
        }
 
    return jsonify({'analisis_gemini': parsed})
 
if __name__ == '__main__':
    app.run(debug=True)
