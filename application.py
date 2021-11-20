from flask import Flask, render_template, redirect, url_for, request, session, flash
from cs50 import SQL
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


db = SQL("sqlite:///notas.db")

@app.route("/home")
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/salir")
def logout():
    session.clear()
    return redirect("register")
    
    
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        # ASEGURAR ENVIO DEL USER
        if not request.form.get("username"):
            flash("Ingrese un nombre")
            return render_template("register.html")
        elif not request.form.get("password"):
            flash("Ingrese una contraseña")
            return render_template("register.html")
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Las contraseñas no coinciden")
            return render_template("register.html")
        
        
        # GUARDAR DATOS
        user = request.form.get("username")
        passw = request.form.get("password")
        # REGISTRAR NUEVO USUARIO
        
        result = db.execute("INSERT INTO users (username,password) VALUES (:username, :password)",
                            username = user, password = generate_password_hash(passw)
                            )
        # VERIFICANDO SI EL USUARIO YA EXISTE                   
        if not result:
            flash("El usuario ya existe")
            return render_template("register.html")
        
        # ALMACENANDO EN LA SESSION
        session["user_id"] = result
        
        return redirect("/")
    else:
        return render_template("register.html")
        
        
        
@app.route("/login")
def login():
    return render_template("login.html")