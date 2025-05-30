# musculos_routes.py

from flask import Blueprint, render_template, redirect, session
from database import graph

musculos_bp = Blueprint('musculos', __name__)

@musculos_bp.route('/musculos')
def ver_musculos():
    if 'usuario' not in session:
        return redirect('/login')

    query = """
    MATCH (e:Ejercicio)-[:ACTIVA_PRIMARIO|:ACTIVA_SECUNDARIO]->(s:SubMusculo)-[:PERTENECE_A]->(g:GrupoMuscular)
    RETURN g.nombre AS grupo, COLLECT(DISTINCT e.nombre) AS ejercicios
    ORDER BY grupo
    """
    resultados = graph.run(query).data()

    return render_template('musculos.html', grupos=resultados, user=session['usuario'])

@musculos_bp.route('/ejercicio/<nombre>')
def detalle_ejercicio(nombre):
    if 'usuario' not in session:
        return redirect('/login')

    query = """
    MATCH (e:Ejercicio {nombre: $nombre})
    OPTIONAL MATCH (e)-[:ACTIVA_PRIMARIO]->(s1:SubMusculo)-[:PERTENECE_A]->(g1:GrupoMuscular)
    OPTIONAL MATCH (e)-[:ACTIVA_SECUNDARIO]->(s2:SubMusculo)-[:PERTENECE_A]->(g2:GrupoMuscular)
    OPTIONAL MATCH (e)-[:ES_TIPO]->(t:Tipo)
    OPTIONAL MATCH (e)-[:REQUIERE_NIVEL]->(n:Nivel)
    RETURN 
        e.nombre AS ejercicio,
        COLLECT(DISTINCT s1.nombre) AS primarios,
        COLLECT(DISTINCT s2.nombre) AS secundarios,
        t.nombre AS tipo,
        n.nombre AS nivel
    """
    resultado = graph.run(query, nombre=nombre).data()

    if resultado:
        data = resultado[0]
        return render_template('detalle_ejercicio.html', ejercicio=data, user=session['usuario'])
    else:
        return f"Ejercicio '{nombre}' no encontrado", 404