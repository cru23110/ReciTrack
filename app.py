from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates')

usuarios = [
    {'correo': 'usuario1@example.com', 'contrasena': 'contrasena1', 'nombre': 'Juan', 'puntos': 100},
    {'correo': 'usuario2@example.com', 'contrasena': 'contrasena2', 'nombre': 'Mia', 'puntos': 85},
    {'correo': 'usuario3@example.com', 'contrasena': 'contrasena3', 'nombre': 'Linda', 'puntos': 120},
]


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

if __name__ == '__main__':
    app.run(debug=True)
