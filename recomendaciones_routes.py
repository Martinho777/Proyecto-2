from flask import Blueprint, render_template, session, redirect
from database import graph

recomendaciones_bp = Blueprint('recomendaciones', __name__)

@recomendaciones_bp.route('/recomendaciones')
def recomendaciones():
    if 'usuario' not in session:
        return redirect('/login')

    nivel = session['usuario']['nivel']
    objetivo = session['usuario']['objetivo']

    query = """
    MATCH (e:Ejercicio)-[:REQUIERE_NIVEL]->(n:Nivel {nombre: $nivel})
    OPTIONAL MATCH (e)-[:ACTIVA_PRIMARIO]->(s1:SubMusculo)
    OPTIONAL MATCH (e)-[:ACTIVA_SECUNDARIO]->(s2:SubMusculo)
    OPTIONAL MATCH (e)-[:ES_TIPO]->(t:Tipo)
    RETURN 
        e.nombre AS nombre,
        COLLECT(DISTINCT s1.nombre) AS primarios,
        COLLECT(DISTINCT s2.nombre) AS secundarios,
        t.nombre AS tipo,
        n.nombre AS nivel
    LIMIT 10
    """

    resultados = graph.run(query, nivel=nivel).data()

    return render_template('recomendaciones.html', ejercicios=resultados, user=session['usuario'])