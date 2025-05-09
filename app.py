from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Página de inicio
@app.route('/')
def inicio():
    return render_template('inicio.html')

# Página de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Recoger datos del formulario (pero NO se guardan en ninguna base)
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

        print(" Datos recibidos (simulado, sin guardar):")
        for clave, valor in datos.items():
            print(f"{clave}: {valor}")

        return redirect('/')
    
    return render_template('registro.html')

# Ejecutar el servidor local
if __name__ == '__main__':
    app.run(debug=True)
