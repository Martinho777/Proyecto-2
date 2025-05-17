from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        datos = {
            'telefono': request.form.get('telefono', ''),
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

        print("Intento de login (demo, no verificado):")
        print(f"Email: {email}, Password: {password}")

        # Simula login exitoso y redirige al dashboard
        return redirect('/dashboard')

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    # Datos de usuario predeterminados para mostrar en el dashboard
    user_data = {
        'nombre': 'User1',
        'nivel': 'Intermedio',
        'email': 'user1@example.com'
    }
    
    # Datos estadísticos predeterminados
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

# Rutas adicionales para completar la navegación
@app.route('/calendario')
def calendario():
    # Datos de usuario predeterminados
    user_data = {
        'nombre': 'User1',
        'nivel': 'Intermedio',
        'email': 'user1@example.com'
    }
    return render_template('dashboard.html', user=user_data, active_page='calendario')

@app.route('/musculos')
def musculos():
    # Datos de usuario predeterminados
    user_data = {
        'nombre': 'User1',
        'nivel': 'Intermedio',
        'email': 'user1@example.com'
    }
    return render_template('dashboard.html', user=user_data, active_page='musculos')

@app.route('/estadisticas')
def estadisticas():
    # Datos de usuario predeterminados
    user_data = {
        'nombre': 'User1',
        'nivel': 'Intermedio',
        'email': 'user1@example.com'
    }
    return render_template('dashboard.html', user=user_data, active_page='estadisticas')

@app.route('/perfil')
def perfil():
    # Datos de usuario predeterminados
    user_data = {
        'nombre': 'User1',
        'nivel': 'Intermedio',
        'email': 'user1@example.com'
    }
    return render_template('dashboard.html', user=user_data, active_page='perfil')

@app.route('/nuevo-ejercicio')
def nuevo_ejercicio():
    # Datos de usuario predeterminados
    user_data = {
        'nombre': 'User1',
        'nivel': 'Intermedio',
        'email': 'user1@example.com'
    }
    return render_template('dashboard.html', user=user_data, active_page='nuevo-ejercicio')

@app.route('/quienes')
def quienes():
    return render_template('quienes.html')

if __name__ == '__main__':
    app.run(debug=True)