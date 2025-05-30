from flask import Flask, render_template
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

# Registrar blueprints
app.register_blueprint(auth_bp)

# Página principal
@app.route('/')
def inicio():
    return render_template('inicio.html')

# Ruta directa para quienes.html
@app.route('/quienes')
def quienes():
    return render_template('quienes.html')

if __name__ == '__main__':
    app.run(debug=True)