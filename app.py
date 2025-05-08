from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Página de inicio
@app.route('/')
def inicio():
    return render_template('inicio.html')

# Página de registro de usuario
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Obtener datos del formulario
        datos = {
            'nombre': request.form['nombre'],
            'email': request.form['email'],
            'password': request.form['password'],
            'edad': request.form['edad'],
            'altura': request.form['altura'],
            'peso': request.form['peso'],
            'nivel': request.form['nivel'],
            'objetivo': request.form['objetivo'],
            'dias_entreno': request.form['dias_entreno']
        }

        # 🔧 Aquí conectaremos con Neo4j para guardar al usuario
        print("[INFO] Usuario registrado:")
        for k, v in datos.items():
            print(f"{k}: {v}")

        return redirect('/')
    
    return render_template('registro.html')

# Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)
