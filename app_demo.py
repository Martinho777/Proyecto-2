from flask import Flask, render_template, request, redirect

app = Flask(__name__)

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

        print("Datos recibidos (demo, no guardados):")
        for clave, valor in datos.items():
            print(f"{clave}: {valor}")

        return redirect('/')
    
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print(" Intento de login (demo, no verificado):")
        print(f"Email: {email}, Password: {password}")

        # Simula login exitoso
        return redirect('/')

    return render_template('login.html', error=error)

@app.route('/quienes')
def quienes():
    return render_template('quienes.html')


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/dashboard')
def dashboard():
    # Simple route that doesn't require authentication
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    # En una aplicación real, verificaríamos si el usuario está autenticado
    # y obtendríamos sus datos de Neo4j
    
    # Ejemplo de consulta a Neo4j (comentada por ahora)
    # query = """
    # MATCH (u:Usuario {email: $email})
    # RETURN u
    # """
    # user_data = graph.run(query, email=session.get('email')).data()
    
    # Por ahora, solo renderizamos la plantilla con datos de ejemplo
    return render_template('dashboard.html', username="Juan Díaz")

@app.route('/logout')
def logout():
    # En una aplicación real, limpiaríamos la sesión
    # session.clear()
    return redirect('/')

# Rutas adicionales para completar la navegación
@app.route('/calendario')
def calendario():
    return render_template('dashboard.html', active_page="calendario", username="Juan Díaz")

@app.route('/musculos')
def musculos():
    return render_template('dashboard.html', active_page="musculos", username="Juan Díaz")

@app.route('/estadisticas')
def estadisticas():
    return render_template('dashboard.html', active_page="estadisticas", username="Juan Díaz")

@app.route('/perfil')
def perfil():
    return render_template('dashboard.html', active_page="perfil", username="Juan Díaz")

@app.route('/nuevo-ejercicio')
def nuevo_ejercicio():
    return render_template('dashboard.html', active_page="nuevo_ejercicio", username="Juan Díaz")