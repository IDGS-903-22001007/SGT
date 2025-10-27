from flask import Flask, send_from_directory

# Configuramos la app sin ruta de plantillas para que sirva archivos estáticos
app = Flask(__name__)

# Definimos la ruta de inicio ('/')
@app.route('/')
def index():
    # Usamos send_from_directory para servir el archivo login.html
    # El punto ('.') es el directorio actual (que será /home/site/wwwroot/sgt después del despliegue)
    return send_from_directory('.', 'login.html')

if __name__ == '__main__':
    app.run(debug=True)
