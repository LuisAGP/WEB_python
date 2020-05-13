

#Este documento es equivalente al init.php
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")#Ruta inicial del servidor web
def index():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=False)
