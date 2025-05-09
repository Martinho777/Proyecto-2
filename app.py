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
        # Datos del formulario
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

        # Cypher para crear nodo Usuario en Neo4j
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

if __name__ == '__main__':
    app.run(debug=True)
