from flask import Flask, render_template, request, session, redirect, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave secreta segura en un entorno de producción
bootstrap = Bootstrap(app)

# Estructura de datos para almacenar las credenciales de usuario (reemplaza esto con una base de datos en un entorno de producción)
users = {
    'garcciaos': '1002'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Página de inicio del sistema de inicio de sesión.

    Permite a los usuarios iniciar sesión proporcionando su nombre de usuario y contraseña.
    Si las credenciales son válidas, se redirige al usuario al panel de control.
    Si las credenciales son inválidas, se muestra un mensaje de error.

    Returns:
        Si el método de solicitud es POST y las credenciales son válidas, redirige al usuario al panel de control.
        Si el método de solicitud es GET, muestra la página de inicio de sesión.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('h.html', message='Invalid username or password. Please try again.')
    return render_template('h.html')

@app.route('/dashboard')
def dashboard():
    """
    Panel de control del sistema de inicio de sesión.

    Muestra el nombre de usuario del usuario actualmente autenticado.

    Returns:
        Si el usuario ha iniciado sesión, muestra el panel de control con el nombre de usuario.
        Si el usuario no ha iniciado sesión, redirige al usuario a la página de inicio de sesión.
    """
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """
    Página de cierre de sesión del sistema de inicio de sesión.

    Cierra la sesión del usuario actualmente autenticado y redirige al usuario a la página de inicio de sesión.

    Returns:
        Redirige al usuario a la página de inicio de sesión.
    """
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
