from flask import Flask, render_template

# Flask automáticamente busca en la subcarpeta 'templates'
# Si movemos login.html a /sgt/templates/, este código funciona
app = Flask(__name__) 

@app.route('/')
def index():
    # 🔥 Esta función necesita que login.html esté en la carpeta /sgt/templates/
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
