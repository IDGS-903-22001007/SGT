from flask import Flask, render_template

# Flask automáticamente busca en la subcarpeta 'templates'
app = Flask(__name__) 

@app.route('/')
def index():
    # Flask buscará este archivo en la carpeta 'templates'
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
