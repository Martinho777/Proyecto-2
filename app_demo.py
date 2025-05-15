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

        # Simula guardado: imprime los datos en consola
        print("📦 Datos recibidos (sin Neo4j):")
        for k, v in datos.items():
            print(f"{k}: {v}")

        return redirect('/')
    
    return render_template('registro.html')

if __name__ == '__main__':
    app.run(debug=True)
