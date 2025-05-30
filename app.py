from flask import Flask, render_template
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

# Página principal
@app.route('/')
def inicio():
    return render_template('inicio.html')

# Página "Quiénes somos"
@app.route('/quienes')
def quienes():
    return render_template('quienes.html')

# Cierre seguro de recursos si es necesario
@app.teardown_appcontext
def shutdown_session(exception=None):
    print("Aplicación cerrada, recursos liberados.")

# Iniciar servidor
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5050)