# estadisticas_routes.py

from flask import Blueprint, render_template, session, redirect
from database import graph

estadisticas_bp = Blueprint('estadisticas', __name__)

@estadisticas_bp.route('/estadisticas')
def ver_estadisticas():
    if 'usuario' not in session:
        return redirect('/login')

    # Estadísticas por grupo muscular
    query_grupos = """
    MATCH (e:Ejercicio)-[:ACTIVA_PRIMARIO|:ACTIVA_SECUNDARIO]->(:SubMusculo)-[:PERTENECE_A]->(g:GrupoMuscular)
    RETURN g.nombre AS grupo, COUNT(DISTINCT e) AS total_ejercicios
    ORDER BY grupo
    """
    grupo_stats = graph.run(query_grupos).data()

    # Estadísticas por tipo de ejercicio
    query_tipos = """
    MATCH (e:Ejercicio)-[:ES_TIPO]->(t:Tipo)
    RETURN t.nombre AS tipo, COUNT(e) AS cantidad
    """
    tipo_stats = graph.run(query_tipos).data()

    # Estadísticas por nivel de dificultad
    query_niveles = """
    MATCH (e:Ejercicio)-[:REQUIERE_NIVEL]->(n:Nivel)
    RETURN n.nombre AS nivel, COUNT(e) AS cantidad
    """
    nivel_stats = graph.run(query_niveles).data()

    return render_template(
        'estadisticas.html',
        grupos=grupo_stats,
        tipos=tipo_stats,
        niveles=nivel_stats,
        user=session['usuario']
    )