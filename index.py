

#Este documento es equivalente al init.php

#Importamos las librerias para levantar el servidor local
from flask import Flask, render_template, request, url_for, redirect, flash
#Importamos el driver para conectar con Base de datos
from flask_mysqldb import MySQL

#Creamos una variable que reciba el objeto de la aplicacion
app = Flask(__name__)

#conecion de MySQL
app.config['MYSQL_HOST'] = 'localhost' #Definimos el servidor donde esta alojada nuestra BD
app.config['MYSQL_USER'] = 'Luis' #Nombre de usuario para la BD
app.config['MYSQL_PASSWORD'] = '16630041' #Contraseña del usuario
app.config['MYSQL_DB'] = 'agenda' #Nombre de la base de datos
#Definimos una variable que reciba el objeto de la base de datos que acabamos de instanciar
bd = MySQL(app)

# Configuracion de clave para el cifrado de cookies
app.secret_key = 'mysecret_key'

#@app.route ---Asi es como se definiran las rutas de nuestro servidor
@app.route("/")#Ruta inicial del servidor web (Raiz)
def index():
    cur = bd.connection.cursor()
    cur.execute('Select * from contactos')
    datos = cur.fetchall()
    return render_template('index.html', contactos=datos)


#Ruta para agregar contactos, procesado a traves del metodo POST
@app.route("/add_contact", methods=['POST'])
def add_contact():
    if request.method == 'POST':
        #Extraemos los datos de los campos
        nombre = request.form['nombre']
        tel = request.form['telefono']
        correo = request.form['correo']

        #Definimos un puntero para la base de datos
        cur = bd.connection.cursor()
        #Hacemos la insercion en el puntero de la base de datos
        cur.execute('INSERT into contactos (nombre, telefono, email) VALUES(%s, %s, %s)', (nombre, tel, correo))
        #Realizamos los cambios a la base de datos
        bd.connection.commit()
        #Mensaje emergente en el index.html
        flash("Contacto agregado!")
        #regresamos a la pagina principal
        return redirect(url_for('index'))

#Ruta donde editamos los contactos
@app.route("/edit/<id>")#La ruta es diferente para cada contacto y es definida a partir de su id
def get_contact(id):#El metodo recibira un id
    #definimos un puntero para la base de datos
    cur = bd.connection.cursor()
    #consultamos el dato del id que acabamos de recibir
    cur.execute('Select * from contactos Where id = {}'.format(id))
    #extraemos todos los datos con ese id
    data = cur.fetchall()
    #direccionamos a editar.html con los datos que extraimos
    return render_template("editar.html", contacto=data[0])

#Ruta para eliminar
@app.route("/delete/<string:id>")#La ruta es diferente para cada contacto y es definida a partir de su id
def delete(id):#recibimos el id del datos a borrar
    #definimos el puntero para la base de datos
    cur = bd.connection.cursor()
    #Borramos el dato a partir del puntero con el id que acabamos de recibir
    cur.execute('Delete from contactos Where id = {}'.format(id))
    #Realizamos los cambios en la base de datos
    bd.connection.commit()
    #mostramos al usuario un mensaje
    flash("Contacto Eliminado!")
    #redireccionamos al index
    return redirect(url_for('index'))

#Ruta para actualizar los datos en la base de datos
@app.route("/update/<id>", methods = ['POST'])
def update(id):
    #verificamos lo que recibimos a traves del metodo POST
    if request.method == 'POST':
        #si lo que recibimos fue la peticion de sair solo regresaremos al index
        if "salir" in request.form:
            pass
        else:
            #Si no entonces...
            #Extraemos los datos de los campos
            nombre = request.form['nombre']
            tel = request.form['tel']
            correo = request.form['email']
            #Creamos el puntero de la base de datos
            cur = bd.connection.cursor()
            #Definimos la instruccion con los datos que vamos a modificar con el campo llave = id
            cur.execute("""
            Update contactos
            set nombre = %s,
                email = %s,
                telefono = %s
            Where id = %s
            """, (nombre, correo, tel, id))
            #Realizamos los cambios a la base de datos
            bd.connection.commit()
            #Mostramos mensaje emergente
            flash("Contacto actualizado!")
    #Direccionamos nuevamente al index
    return redirect(url_for("index"))

#Definimos un main
if __name__ == "__main__":
    #Ejecutamos la aplicacion en modo debug activado
    app.run(debug=True)
