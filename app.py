from flask import Flask
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.musculos_routes import musculos_bp
from routes.perfil_routes import perfil_bp
from routes.calendario_routes import calendario_bp
from routes.estadisticas_routes import estadisticas_bp
from routes.ejercicios_routes import ejercicios_bp
from routes.quienes_routes import quienes_bp

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

# Registrar Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(musculos_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(calendario_bp)
app.register_blueprint(estadisticas_bp)
app.register_blueprint(ejercicios_bp)
app.register_blueprint(quienes_bp)

# Ruta raíz (puedes redirigir si lo deseas)
@app.route('/')
def inicio():
    return "<h2>Página de inicio. Usa /login o /registro para comenzar.</h2>"

if __name__ == '__main__':
    app.run(debug=True)