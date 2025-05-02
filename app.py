from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def inicio():
    return '<h1>¡Bienvenido a MyGymAI!</h1><p>Tu sistema inteligente de recomendaciones de ejercicios.</p>'

if __name__ == '__main__':
    app.run(debug=True)
