

#Este documento es equivalente al init.php
from flask import Flask, render_template, request, url_for, redirect, flash
#Importamos el driver para conectar con Base de datos
from flask_mysqldb import MySQL

app = Flask(__name__)

#conecion de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Luis'
app.config['MYSQL_PASSWORD'] = '16630041'
app.config['MYSQL_DB'] = 'agenda'
bd = MySQL(app)

# configuraciones
app.secret_key = 'mysecret_key'

@app.route("/")#Ruta inicial del servidor web (Raiz)
def index():
    cur = bd.connection.cursor()
    cur.execute('Select * from contactos')
    datos = cur.fetchall()
    return render_template('index.html', contactos=datos)



@app.route("/add_contact", methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombre = request.form['nombre']
        tel = request.form['telefono']
        correo = request.form['correo']

        cur = bd.connection.cursor()
        cur.execute('INSERT into contactos (nombre, telefono, email) VALUES(%s, %s, %s)', (nombre, tel, correo))
        bd.connection.commit()
        flash("Contacto agregado!")
        return redirect(url_for('index'))

@app.route("/edit/<id>")
def get_contact(id):
    cur = bd.connection.cursor()
    cur.execute('Select * from contactos Where id = {}'.format(id))
    print(id)
    data = cur.fetchall()
    return render_template("editar.html", contacto=data[0])

@app.route("/delete/<string:id>")
def delete(id):
    cur = bd.connection.cursor()
    cur.execute('Delete from contactos Where id = {}'.format(id))
    bd.connection.commit()

    flash("Contacto Eliminado!")
    return redirect(url_for('index'))

@app.route("/update/<id>", methods = ['POST'])
def update(id):
    if request.method == 'POST':
        if "salir" in request.form:
            pass
        else:
            nombre = request.form['nombre']
            tel = request.form['tel']
            correo = request.form['email']
            cur = bd.connection.cursor()
            cur.execute("""
            Update contactos
            set nombre = %s,
                email = %s,
                telefono = %s
            Where id = %s
            """, (nombre, correo, tel, id))
            bd.connection.commit()
            flash("Contacto actualizado!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
