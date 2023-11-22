from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, template_folder='templates')

def crear_bd():
    conn = sqlite3.connect('reciclaje.db')
    cursor = conn.cursor()

    # Crear tablas en la base de datos (aquí debes definir la estructura de tus tablas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            correo TEXT,
            contrasena TEXT,
            puntos INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seguimientos (
            id INTEGER PRIMARY KEY,
            material TEXT,
            cantidad INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS actividades_reciclaje (
            id INTEGER PRIMARY KEY,
            material TEXT,
            cantidad INTEGER,
            categoria TEXT
        )
    ''')

    conn.commit()
    conn.close()

def conectar_bd():
    return sqlite3.connect('reciclaje.db')

def obtener_usuarios():
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()

    # Crear una lista de diccionarios a partir de los resultados
    lista_usuarios = []
    for usuario in usuarios:
        lista_usuarios.append({
            'id': usuario[0],
            'nombre': usuario[1],
            'correo': usuario[2],
            'puntos': usuario[3],
            'contrasena': usuario[4]
        })

    conn.close()
    return lista_usuarios

# usuarios = [
#     {'correo': 'usuario1@example.com', 'contrasena': 'contrasena1', 'nombre': 'Juan', 'puntos': 100},
#     {'correo': 'usuario2@example.com', 'contrasena': 'contrasena2', 'nombre': 'Mia', 'puntos': 85},
#     {'correo': 'usuario3@example.com', 'contrasena': 'contrasena3', 'nombre': 'Linda', 'puntos': 120},
# ]

# Datos de prueba de seguimientos de reciclaje 
seguimientos = []
# Datos de prueba de actividades de reciclaje
actividades_reciclaje = []

# Ruta principal que renderiza la página de inicio
@app.route('/')
def inicio():
    # Lógica para generar sugerencias de reciclaje
    sugerencias = ['Recicla tus botellas de plástico', 'Reutiliza papel para hacer manualidades', 'Separa vidrio del resto de la basura', '...']
    return render_template('index.html', sugerencias=sugerencias)

@app.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        # Obtener los datos del formulario
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        
        # Realizar la autenticación (simulada en este ejemplo)
        if autenticar_usuario(correo, contrasena):
            # Autenticación exitosa, redirigir a la página de inicio o a donde sea necesario
            return redirect(url_for('pagina_inicio'))
        else:
            # Autenticación fallida, mostrar un mensaje de error en la página de inicio de sesión
            error = "Correo electrónico o contraseña incorrectos. Inténtalo de nuevo."
            return render_template('inicio_sesion.html', error=error)
    else:
        # Método GET: Mostrar la página de inicio de sesión
        return render_template('inicio_sesion.html')

@app.route('/pagina_inicio')
def pagina_inicio():
    return "Bienvenido a la página de inicio. Aquí puedes agregar más contenido."

@app.route('/ranking_comunitario')
def ranking_comunitario():
    # Obtener la lista de usuarios desde la base de datos
    usuarios = obtener_usuarios()
    
    # Ordena la lista de usuarios por puntos en orden descendente
    usuarios_ordenados = sorted(usuarios, key=lambda x: x['puntos'], reverse=True)
    
    # Renderiza la página de ranking con la lista ordenada de usuarios
    return render_template('ranking_comunitario.html', usuarios=usuarios_ordenados)

# Función de autenticación (simulada en este ejemplo)
def autenticar_usuario(correo, contrasena):
    
    for usuario in usuarios:
        if usuario['correo'] == correo and usuario['contrasena'] == contrasena:
            return True
    return False

# Mia
@app.route('/registro', methods=['GET'])
def registro():
    return render_template('registro.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        
        # Comprobar si el correo ya está registrado (simulación)
        if any(usuario['correo'] == correo for usuario in usuarios):
            error = "El correo electrónico ya está registrado. Inicia sesión o utiliza otro correo."
            return render_template('registro.html', error=error)
        
        # Agregar el nuevo usuario a la lista (simulación)
        usuarios.append({'nombre': nombre, 'correo': correo, 'contrasena': contrasena, 'puntos': 0})
        
        # Redirigir al usuario a la página de inicio de sesión o a donde sea necesario
        return redirect(url_for('inicio_sesion'))
    
@app.route('/seguimiento', methods=['GET'])
def seguimiento():
    return render_template('seguimiento.html')

@app.route('/seguir', methods=['POST'])
def seguir():
    if request.method == 'POST':
        # Obtener los datos del formulario
        material = request.form['material']
        cantidad = int(request.form['cantidad'])
        
        # Agregar el seguimiento a la lista (simulación)
        seguimientos.append({'material': material, 'cantidad': cantidad})
        
        # Redirigir al usuario a la página de inicio o a donde sea necesario
        return redirect(url_for('pagina_inicio'))

# Linda
@app.route('/registro_actividades', methods=['GET', 'POST'])
def registro_actividades():
    if request.method == 'POST':
        material = request.form['material']
        cantidad = int(request.form['cantidad'])
        categoria = request.form['categoria']  # Agregar un campo de selección de categoría en el formulario
        
        # Agregar la actividad de reciclaje con categoría a la lista (simulación)
        # actividades_reciclaje.append({'material': material, 'cantidad': cantidad, 'categoria': categoria})
        conn = sqlite3.connect('reciclaje.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO actividades_reciclaje (material, cantidad, categoria) VALUES (?, ?, ?)', (material, cantidad, categoria))
        conn.commit()
        conn.close()

        # Redirigir al usuario a la página de inicio o a donde sea necesario
        return redirect(url_for('pagina_inicio'))
    
    return render_template('registro_actividades.html')

@app.route('/registrar_actividad', methods=['POST'])
def registrar_actividad():
    if request.method == 'POST':
        # Obtener los datos del formulario
        material = request.form['material']
        cantidad = int(request.form['cantidad'])
        
        # Agregar la actividad de reciclaje a la lista (simulación)
        actividades_reciclaje.append({'material': material, 'cantidad': cantidad})
        
        # Redirigir al usuario a la página de inicio o a donde sea necesario
        return redirect(url_for('pagina_inicio'))
    
if __name__ == '__main__':
    app.run(debug=True)
