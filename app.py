from flask import Flask, render_template, request, redirect
from py2neo import Graph

app = Flask(__name__)
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
            user_data = {
                'nombre': usuario['nombre'],
                'nivel': usuario['nivel'],
                'email': usuario['email']
            }
            return render_template('dashboard.html', user=user_data)
        else:
            error = "Usuario o contraseña incorrectos."

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    user_data = {
        'nombre': 'Juan',
        'nivel': 'Intermedio',
        'email': 'juan@example.com'
    }

    stats = {
        'racha': 7,
        'racha_cambio': '+2',
        'volumen': '12,540',
        'volumen_cambio': '+8%',
        'entrenamientos': 4,
        'entrenamientos_cambio': 'Igual',
        'prs': 3,
        'prs_cambio': '+1'
    }

    return render_template('dashboard.html', user=user_data, stats=stats)

@app.route('/logout')
def logout():
    return redirect('/')

@app.route('/calendario')
def calendario():
    return render_template('dashboard.html', active_page='calendario')

@app.route('/musculos')
def musculos():
    return render_template('dashboard.html', active_page='musculos')

@app.route('/estadisticas')
def estadisticas():
    return render_template('dashboard.html', active_page='estadisticas')

@app.route('/perfil')
def perfil():
    return render_template('dashboard.html', active_page='perfil')

@app.route('/nuevo-ejercicio')
def nuevo_ejercicio():
    return render_template('dashboard.html', active_page='nuevo-ejercicio')

@app.route('/quienes')
def quienes():
    return render_template('quienes.html')

if __name__ == '__main__':
    app.run(debug=True)
