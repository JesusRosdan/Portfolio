from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Configuración de MySQL
app.config['MYSQL_HOST'] = '192.168.1.91'
app.config['MYSQL_USER'] = 'tocinacio'
app.config['MYSQL_PASSWORD'] = 'tocino'
app.config['MYSQL_DB'] = 'loginapp'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[2], password): 
            session['loggedin'] = True
            session['username'] = username
            return redirect(url_for('home'))
        else:
            msg = 'Credenciales incorrectas'
            
    return render_template('login.html', msg=msg)

@app.route('/home')
def home():
    if 'loggedin' in session:
        return f'Hola, {session["username"]}! Bienvenido.'
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()
        # Verifica si el usuario ya existe
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        if user:
            msg = 'El usuario ya existe'
        else:
            # Inserta el nuevo usuario
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            mysql.connection.commit()
            msg = 'Usuario registrado exitosamente'
        cur.close()
    return render_template('register.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True)
