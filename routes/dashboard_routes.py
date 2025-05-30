# routes/dashboard_routes.py

from flask import Blueprint, render_template, session, redirect, url_for

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def inicio_dashboard():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))
    
    user = session['usuario']
    return render_template('dashboard.html', user=user)