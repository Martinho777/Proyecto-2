from flask import Blueprint, render_template, request, redirect, session
from database import graph
import uuid
from datetime import date

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/recomendaciones', methods=['GET', 'POST'])
def recomendaciones():
    if 'usuario' not in session:
        return redirect('/login')

    if request.method == 'POST':
        grupos = request.form.getlist('grupos')
        nivel = request.form.get('nivel')

        if not (1 <= len(grupos) <= 3):
            return "Debes seleccionar entre 1 y 3 grupos musculares.", 400
        if nivel not in ["Principiante", "Intermedio", "Avanzado"]:
            return "Nivel inválido", 400

        limite = {"Principiante": 4, "Intermedio": 6, "Avanzado": 8}[nivel]

        # ✅ Query Cypher corregido (REQUIERE_NIVEL, ACTIVA_SECUNDARIO)
        query = """
        MATCH (s:SubMusculo)-[:PERTENECE_A]->(g:GrupoMuscular)
        WHERE g.nombre IN $grupos
        MATCH (e:Ejercicio)-[:ACTIVA_PRIMARIO|ACTIVA_SECUNDARIO]->(s)
        MATCH (e)-[:REQUIERE_NIVEL]->(n:Nivel)
        WHERE n.nombre = $nivel
        MATCH (e)-[:ES_TIPO]->(t:Tipo)
        RETURN DISTINCT e.nombre AS nombre, t.nombre AS tipo
        ORDER BY CASE t.nombre WHEN "Compuesto" THEN 0 ELSE 1 END
        LIMIT $limite
        """
        ejercicios = graph.run(query, grupos=grupos, nivel=nivel, limite=limite).data()
        print("EJERCICIOS RECOMENDADOS:", ejercicios)  # Depuración

        # Crear y guardar rutina si hay resultados
        if ejercicios:
            rutina_id = str(uuid.uuid4())
            usuario_email = session['usuario']['email']
            hoy = str(date.today())

            graph.run("""
            MATCH (u:Usuario {email: $email})
            CREATE (r:Rutina {
                id: $rutina_id,
                fecha: date($fecha),
                nivel: $nivel
            })
            MERGE (u)-[:GENERÓ]->(r)
            WITH r
            UNWIND $ejercicios AS ej
            MATCH (e:Ejercicio {nombre: ej.nombre})
            MERGE (r)-[:INCLUYE]->(e)
            """, email=usuario_email, rutina_id=rutina_id, fecha=hoy, nivel=nivel, ejercicios=ejercicios)

        return render_template("recomendacion.html", ejercicios=ejercicios)

    return render_template("recomendacion.html", ejercicios=None)