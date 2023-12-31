# Universidad del Valle de Guatemala
# Programacion orientada a objetos
# Proyecto final
# Grupo 
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__, template_folder='templates')
app.secret_key = 'Gdsafg54dsT6'

def crear_bd():
    conn = sqlite3.connect('reciclaje.db')
    cursor = conn.cursor()

    # Crear tablas en la base de datos
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
            usuario_id INTEGER,
            material TEXT,
            cantidad INTEGER,
            categoria TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
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
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        
        # Realizar la autenticación utilizando la base de datos
        if autenticar_usuario_bd(correo, contrasena):
            # Autenticación exitosa, establecer la sesión y redirigir
            session['usuario'] = correo
            return redirect(url_for('pagina_usuario'))
        else:
            error = "Correo electrónico o contraseña incorrectos. Inténtalo de nuevo."
            
            # Verificar si el usuario no existe y redirigir a la página de registro
            if not usuario_existe(correo):
                return redirect(url_for('registro', error=error))
            
            return render_template('inicio_sesion.html', error=error)
    else:
        # Método GET: Mostrar la página de inicio de sesión o la de usuario si ya está logueado
        if 'usuario' in session:
            return redirect(url_for('pagina_usuario'))
        return render_template('inicio_sesion.html')
    
# Función para comprobar si un usuario ya existe en la base de datos
def usuario_existe(correo):
    conn = sqlite3.connect('reciclaje.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE correo = ?', (correo,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario is not None

# Función para registrar un nuevo usuario en la base de datos
def registrar_usuario(nombre, correo, contrasena):
    conn = sqlite3.connect('reciclaje.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (nombre, correo, contrasena, puntos) VALUES (?, ?, ?, 0)', (nombre, correo, contrasena))
    conn.commit()
    conn.close()

# Función para autenticar un usuario utilizando la base de datos
def autenticar_usuario_bd(correo, contrasena):
    conn = sqlite3.connect('reciclaje.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE correo = ? AND contrasena = ?', (correo, contrasena))
    usuario = cursor.fetchone()
    conn.close()
    return usuario is not None


# página de usuario
@app.route('/usuario')
def pagina_usuario():
    if 'usuario' in session:
        usuario_actual = obtener_usuario_por_correo(session['usuario'])
        return render_template('usuario.html', usuario=usuario_actual)
    else:
        return redirect(url_for('inicio_sesion'))
    
def obtener_usuario_por_correo(correo):
    conn = sqlite3.connect('reciclaje.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre FROM usuarios WHERE correo = ?', (correo,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        nombre = resultado[0]
        return {'nombre': nombre}
    else:
        return None


# cerrar sesión
@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('usuario', None)
    return redirect(url_for('inicio_sesion'))

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
        
        # Comprobar si el correo ya está registrado en la base de datos
        if usuario_existe(correo):
            error = "El correo electrónico ya está registrado. Inicia sesión o utiliza otro correo."
            return render_template('registro.html', error=error)
        
        # Agregar el nuevo usuario a la base de datos
        registrar_usuario(nombre, correo, contrasena)
        
        # Redirigir al usuario a la página de inicio de sesión
        return redirect(url_for('inicio_sesion'))

@app.route('/seguimiento', methods=['GET'])
def seguimiento():
    if 'usuario' in session:
        usuario_actual = obtener_usuario_por_correo_id(session['usuario'])
        # Obtener las actividades recientes del usuario
        actividades_recientes = obtener_actividades_recientes(usuario_actual[0])
        return render_template('seguimiento.html', actividades_recientes=actividades_recientes)
    else:
        return redirect(url_for('inicio_sesion'))
    
def obtener_usuario_por_correo_id(correo):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    # Seleccionar el campo 'id' además de otros campos
    cursor.execute('SELECT id, nombre, correo, puntos FROM usuarios WHERE correo = ?', (correo,))
    usuario = cursor.fetchone()
    
    conn.close()
    return usuario

def obtener_actividades_recientes(usuario_id):
    conn = sqlite3.connect('reciclaje.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT material, cantidad, categoria
        FROM actividades_reciclaje
        WHERE usuario_id = ?
        ORDER BY id DESC
        LIMIT 5  -- Obtener las últimas 5 actividades reciclaje
    ''', (usuario_id,))
    actividades_recientes = cursor.fetchall()
    conn.close()

    return actividades_recientes

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
    if 'usuario' not in session:
        # Si no hay un usuario registrado, redirige a la página de inicio de sesión
        return redirect(url_for('inicio_sesion'))
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        material = request.form['material']
        cantidad = int(request.form['cantidad'])
        categoria = request.form['categoria']

        # Obtener el ID del usuario activo
        usuario_actual = obtener_usuario_por_correo_id(session['usuario'])
        print(usuario_actual)
        usuario_id = usuario_actual[0]  # Asegúrate de que esta es la posición correcta

        # Agregar la actividad de reciclaje a la base de datos con el ID del usuario
        conn = sqlite3.connect('reciclaje.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO actividades_reciclaje (usuario_id, material, cantidad, categoria) VALUES (?, ?, ?, ?)', (usuario_id, material, cantidad, categoria))
        conn.commit()
        # conn.close()

        # Actualizar los puntos del usuario en la tabla usuarios
        cursor.execute('UPDATE usuarios SET puntos = puntos + 1 WHERE id = ?', (usuario_id,))
        conn.commit()
        conn.close()

        # Redirigir al usuario a la página de inicio o a donde sea necesario
        # return redirect(url_for('pagina_inicio'))
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
