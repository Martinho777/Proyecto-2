from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = "clave_demo_segura"

# Cargar ejercicios de un archivo JSON simulado
with open('ejercicios_demo.json', 'r', encoding='utf-8') as f:
    datos_demo = json.load(f)
    ejercicios = datos_demo.get("ejercicios", [])

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        identificador = request.form['identificador']
        password = request.form['password']
        # Simulación básica: cualquier usuario funciona si el password es 'demo'
        if password == 'demo':
            session['user'] = {'nombre': identificador, 'nivel': 'Intermedio', 'email': f'{identificador}@demo.com'}
            return redirect('/dashboard')
        else:
            error = "Usuario o contraseña incorrectos."
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    user = session.get('user', {'nombre': 'Visitante', 'nivel': 'Desconocido'})
    return render_template('dashboard.html', user=user, stats={})

@app.route('/musculos')
def musculos():
    grupos = {}
    for e in ejercicios:
        for sub in e["primarios"]:
            grupos.setdefault(sub, []).append(e["nombre"])
    resultados = [{'grupo': k, 'ejercicios': list(set(v))} for k, v in grupos.items()]
    return render_template('musculos.html', grupos=resultados)

@app.route('/ejercicio/<nombre>')
def detalle_ejercicio(nombre):
    for e in ejercicios:
        if e["nombre"] == nombre:
            return render_template('detalle_ejercicio.html', ejercicio=e)
    return f"Ejercicio '{nombre}' no encontrado", 404

@app.route('/quienes')
def quienes():
    return render_template('quienes.html')

if __name__ == '__main__':
    app.run(debug=True)