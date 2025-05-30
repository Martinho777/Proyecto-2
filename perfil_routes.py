# perfil_routes.py

from flask import Blueprint, render_template, session, redirect
from database import graph

perfil_bp = Blueprint('perfil', __name__)

@perfil_bp.route('/perfil')
def ver_perfil():
    if 'usuario' not in session:
        return redirect('/login')

    usuario = session['usuario']

    # Obtener datos del nodo Usuario desde la base
    query = """
    MATCH (u:Usuario {email: $email})
    RETURN u.telefono AS telefono, u.usuario AS usuario, u.nombre AS nombre,
           u.edad AS edad, u.altura AS altura, u.peso AS peso,
           u.nivel AS nivel, u.objetivo AS objetivo, u.dias_entreno AS dias_entreno
    """
    resultado = graph.run(query, email=usuario['email']).data()

    if resultado:
        datos = resultado[0]
        return render_template('perfil.html', usuario=datos)
    else:
        return "Usuario no encontrado", 404