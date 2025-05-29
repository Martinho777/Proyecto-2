from flask import Flask, render_template, request, redirect, session
from py2neo import Graph

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

graph = Graph("bolt://localhost:7687", auth=("neo4j", "DinoPythons3000"))

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    error = None
    if request.method == 'POST':
        datos = {
            'telefono': request.form['telefono'],
            'usuario': request.form['usuario'],
            'email': request.form['email'],
            'nombre': request.form['nombre'],
            'password': request.form['password'],
            'edad': request.form['edad'],
            'altura': request.form['altura'],
            'peso': request.form['peso'],
            'nivel': request.form['nivel'],
            'objetivo': request.form['objetivo'],
            'dias_entreno': request.form['dias_entreno']
        }

        # Verificar si ya existe un usuario o correo igual
        consulta = """
        MATCH (u:Usuario)
        WHERE u.email = $email OR u.usuario = $usuario
        RETURN u
        """
        existente = graph.run(consulta, email=datos['email'], usuario=datos['usuario']).data()

        if existente:
            error = "El correo o nombre de usuario ya están en uso."
            return render_template('registro.html', error=error)

        query_crear = """
        CREATE (u:Usuario {
            telefono: $telefono,
            usuario: $usuario,
            email: $email,
            nombre: $nombre,
            password: $password,
            edad: toInteger($edad),
            altura: toFloat($altura),
            peso: toFloat($peso),
            nivel: $nivel,
            objetivo: $objetivo,
            dias_entreno: toInteger($dias_entreno)
        })
        """
        graph.run(query_crear, parameters=datos)
        return redirect('/login')
    
    return render_template('registro.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        identificador = request.form['identificador']
        password = request.form['password']

        query = """
        MATCH (u:Usuario)
        WHERE (u.email = $identificador OR u.usuario = $identificador)
          AND u.password = $password
        RETURN u LIMIT 1
        """
        resultado = graph.run(query, identificador=identificador, password=password).data()

        if resultado:
            usuario = resultado[0]['u']
            session['usuario'] = {
                'nombre': usuario['nombre'],
                'nivel': usuario['nivel'],
                'email': usuario['email']
            }
            return redirect('/dashboard')
        else:
            error = "Usuario o contraseña incorrectos."

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect('/login')

    user_data = session['usuario']

    # Aquí puedes conectar futuras métricas estadísticas personalizadas
    return render_template('dashboard.html', user=user_data)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')

@app.route('/calendario')
def calendario():
    if 'usuario' not in session:
        return redirect('/login')
    return render_template('dashboard.html', active_page='calendario', user=session['usuario'])

@app.route('/musculos')
def musculos():
    if 'usuario' not in session:
        return redirect('/login')

    query = """
    MATCH (e:Ejercicio)-[:ACTIVA_PRIMARIO|:ACTIVA_SECUNDARIO]->(s:SubMusculo)-[:PERTENECE_A]->(g:GrupoMuscular)
    RETURN g.nombre AS grupo, COLLECT(DISTINCT e.nombre) AS ejercicios
    ORDER BY grupo
    """
    resultados = graph.run(query).data()
    return render_template('musculos.html', grupos=resultados, user=session['usuario'])

@app.route('/estadisticas')
def estadisticas():
    if 'usuario' not in session:
        return redirect('/login')
    return render_template('dashboard.html', active_page='estadisticas', user=session['usuario'])

@app.route('/perfil')
def perfil():
    if 'usuario' not in session:
        return redirect('/login')
    return render_template('dashboard.html', active_page='perfil', user=session['usuario'])

@app.route('/nuevo-ejercicio')
def nuevo_ejercicio():
    if 'usuario' not in session:
        return redirect('/login')
    return render_template('dashboard.html', active_page='nuevo-ejercicio', user=session['usuario'])

@app.route('/quienes')
def quienes():
    return render_template('quienes.html')

@app.route('/ejercicio/<nombre>')
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

if __name__ == '__main__':
    app.run(debug=True)