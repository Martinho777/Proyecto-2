from flask import Blueprint, render_template, session, redirect
from database import graph

ejercicio_bp = Blueprint('ejercicio', __name__)

@ejercicio_bp.route('/ejercicio/<nombre>')
def detalle(nombre):
    if 'usuario' not in session:
        return redirect('/login')

    query = """
    MATCH (e:Ejercicio {nombre: $nombre})
    OPTIONAL MATCH (e)-[:ACTIVA_PRIMARIO]->(s1:SubMusculo)-[:PERTENECE_A]->(g1:GrupoMuscular)
    OPTIONAL MATCH (e)-[:ACTIVA_SECUNDARIO]->(s2:SubMusculo)-[:PERTENECE_A]->(g2:GrupoMuscular)
    OPTIONAL MATCH (e)-[:REQUIERE_NIVEL]->(n:Nivel)
    OPTIONAL MATCH (e)-[:ES_TIPO]->(t:Tipo)
    RETURN e.nombre AS nombre,
           COLLECT(DISTINCT s1.nombre) AS primarios,
           COLLECT(DISTINCT s2.nombre) AS secundarios,
           t.nombre AS tipo,
           n.nombre AS nivel
    """
    resultado = graph.run(query, nombre=nombre).data()

    if resultado:
        ejercicio = resultado[0]
        return render_template("detalle_ejercicio.html", ejercicio=ejercicio)
    else:
        return "Ejercicio no encontrado", 404