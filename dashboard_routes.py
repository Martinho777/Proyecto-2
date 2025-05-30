# dashboard_routes.py

from flask import Blueprint, render_template, redirect, session

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect('/login')

    user_data = session['usuario']

    # Placeholder para estadísticas futuras, puedes conectar métricas reales más adelante
    stats = {
        'racha': 0,
        'racha_cambio': '0',
        'volumen': '0',
        'volumen_cambio': '0%',
        'entrenamientos': 0,
        'entrenamientos_cambio': '0',
        'prs': 0,
        'prs_cambio': '0'
    }

    return render_template('dashboard.html', user=user_data, stats=stats)