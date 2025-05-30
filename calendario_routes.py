# calendario_routes.py

from flask import Blueprint, render_template, session, redirect

calendario_bp = Blueprint('calendario', __name__)

@calendario_bp.route('/calendario')
def ver_calendario():
    if 'usuario' not in session:
        return redirect('/login')

    return render_template('calendario.html', usuario=session['usuario'])