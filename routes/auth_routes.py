from flask import Blueprint, render_template, request, redirect, session, url_for
from database import graph

auth_bp = Blueprint('auth', __name__)

# ------------------ REGISTRO ------------------ #
@auth_bp.route('/registro', methods=['GET', 'POST'])
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

        # Validar si ya existe un usuario con ese email o username
        existe = graph.run(
            """MATCH (u:Usuario)
               WHERE u.email = $email OR u.usuario = $usuario
               RETURN u""",
            email=datos['email'], usuario=datos['usuario']
        ).data()

        if existe:
            error = "Correo o usuario ya registrado."
        else:
            # Crear nodo Usuario
            graph.run(
                """CREATE (u:Usuario {
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
                })""",
                parameters=datos
            )
            return redirect(url_for('auth.login'))

    return render_template('registro.html', error=error)


# ------------------ LOGIN ------------------ #
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        identificador = request.form['identificador']
        password = request.form['password']

        result = graph.run(
            """MATCH (u:Usuario)
               WHERE (u.email = $identificador OR u.usuario = $identificador)
               AND u.password = $password
               RETURN u LIMIT 1""",
            identificador=identificador, password=password
        ).data()

        if result:
            usuario = result[0]['u']
            session['usuario'] = {
                'nombre': usuario['nombre'],
                'nivel': usuario['nivel'],
                'email': usuario['email']
            }
            return redirect(url_for('dashboard.recomendaciones'))  # ← Corregido aquí
        else:
            error = "Usuario o contraseña incorrectos."

    return render_template('login.html', error=error)


# ------------------ LOGOUT ------------------ #
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


# ------------------ QUIÉNES SOMOS ------------------ #
@auth_bp.route('/quienes')
def quienes():
    return render_template('quienes.html')