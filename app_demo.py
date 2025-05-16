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
