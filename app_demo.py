from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

# Cargar los datos desde records.json
with open("records.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

# Filtrar nodos por tipo
usuarios = [n for n in datos if "Usuario" in n["etiquetas"]]
ejercicios = [n for n in datos if "Ejercicio" in n["etiquetas"]]
submusculos = [n for n in datos if "SubMusculo" in n["etiquetas"]]
grupos = [n for n in datos if "GrupoMuscular" in n["etiquetas"]]

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Registro falso (no guarda nada)
        return redirect('/login')
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        identificador = request.form['identificador']
        password = request.form['password']

        for u in usuarios:
            props = u["propiedades"]
            if (props["email"] == identificador or props["usuario"] == identificador) and props["password"] == password:
                session['user'] = {
                    'nombre': props["nombre"],
                    'nivel': props["nivel"],
                    'email': props["email"]
                }
                return redirect('/dashboard')
        error = "Credenciales incorrectas"
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    user = session['user']
    stats = {
        'racha': 0,
        'racha_cambio': '0',
        'volumen': '0',
        'volumen_cambio': '0%',
        'entrenamientos': 0,
        'entrenamientos_cambio': '0',
        'prs': 0,
        'prs_cambio': '0'
    }
    return render_template('dashboard.html', user=user, stats=stats)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/musculos')
def musculos():
    grupos_listos = []
    for grupo in grupos:
        nombre = grupo["propiedades"]["nombre"]
        grupos_listos.append({"grupo": nombre, "ejercicios": []})  # Sin relaciones, solo nombre
    return render_template('musculos.html', grupos=grupos_listos)

@app.route('/ejercicio/<nombre>')
def detalle_ejercicio(nombre):
    resultado = next((e for e in ejercicios if e["propiedades"]["nombre"] == nombre), None)
    if not resultado:
        return f"Ejercicio '{nombre}' no encontrado", 404
    data = {
        "ejercicio": nombre,
        "primarios": [],
        "secundarios": [],
        "tipo": "Compuesto",
        "nivel": "Intermedio"
    }
    return render_template("detalle_ejercicio.html", ejercicio=data)

@app.route('/quienes')
def quienes():
    return render_template('quienes.html')

@app.route('/calendario')
@app.route('/estadisticas')
@app.route('/perfil')
@app.route('/nuevo-ejercicio')
def en_construccion():
    return render_template("dashboard.html", active_page="en_construccion")

if __name__ == '__main__':
    app.run(debug=True)