# auth_routes.py

from flask import Blueprint, render_template, request, redirect, session
from database import graph

auth_bp = Blueprint('auth', __name__)

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

        consulta = """
        MATCH (u:Usuario)
        WHERE u.email = $email OR u.usuario = $usuario
        RETURN u
        """
        existente = graph.run(consulta, email=datos['email'], usuario=datos['usuario']).data()
        if existente:
            error = "El correo o nombre de usuario ya están en uso."
            return render_template('registro.html', error=error)

        crear = """
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
        graph.run(crear, parameters=datos)
        return redirect('/login')

    return render_template('registro.html', error=error)

@auth_bp.route('/login', methods=['GET', 'POST'])
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

@auth_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')