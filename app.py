from flask import Flask, render_template, request, redirect
from py2neo import Graph

app = Flask(__name__)

# Conexión a Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "DinoPythons3000"))

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        datos = {
            'telefono': request.form['telefono'],
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

        query = """
        CREATE (u:Usuario {
            telefono: $telefono,
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
        graph.run(query, parameters=datos)
        return redirect('/')
    
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        query = """
        MATCH (u:Usuario)
        WHERE u.email = $email AND u.password = $password
        RETURN u
        """
        result = graph.run(query, email=email, password=password).data()

        if result:
            print(f"✅ Login exitoso de: {email}")
            return redirect('/')
        else:
            error = "Credenciales incorrectas. Intenta nuevamente."

    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
