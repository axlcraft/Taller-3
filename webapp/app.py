from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import os

app = Flask(__name__)

# Configuración de claves secretas
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# URL de la API
API_URL = os.getenv("API_URL", "http://localhost:8000")

# -------------------------------
# Helpers
# -------------------------------

def api_request(method, endpoint, data=None, params=None, token_required=False):
    """
    Realiza peticiones a la API
    """
    headers = {}
    if token_required and "token" in session:
        headers["Authorization"] = f"Bearer {session['token']}"

    url = f"{API_URL}{endpoint}"
    response = requests.request(method, url, json=data, params=params, headers=headers)

    try:
        return response.json()
    except Exception:
        return {"error": "Respuesta inválida de la API"}

def is_logged_in():
    return "token" in session

# -------------------------------
# Rutas
# -------------------------------

@app.route("/")
def index():
    productos = api_request("GET", "/api/v1/products")
    # Si la respuesta es un dict, busca la lista de productos
    if isinstance(productos, dict):
        productos = productos.get("productos") or productos.get("products") or productos
    # Si la respuesta es una lista de strings, conviértela a dict vacíos
    if isinstance(productos, list):
        productos = [p if isinstance(p, dict) else {} for p in productos]
    else:
        productos = []
    return render_template("index.html", productos=productos)

@app.route("/products")
def products():
    productos = api_request("GET", "/api/v1/products")
    if isinstance(productos, dict):
        productos = productos.get("productos") or productos.get("products") or productos
    if isinstance(productos, list):
        productos = [p if isinstance(p, dict) else {} for p in productos]
    else:
        productos = []
    return render_template("products.html", productos=productos)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email and password:
            data = {"email": email, "password": password}
            res = api_request("POST", "/api/v1/users/login", data=data)
            if "token" in res:
                session["token"] = res["token"]
                session["user"] = res.get("user", {})
                flash("Inicio de sesión exitoso", "success")
                return redirect(url_for("index"))
            else:
                flash(res.get("error", "Error en inicio de sesión"), "danger")
        else:
            flash("Todos los campos son obligatorios", "danger")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if username and email and password:
            data = {"username": username, "email": email, "password": password}
            res = api_request("POST", "/api/v1/users/register", data=data)
            if res.get("success"):
                flash("Registro exitoso, ahora puedes iniciar sesión", "success")
                return redirect(url_for("login"))
            else:
                flash(res.get("error", "Error en el registro"), "danger")
        else:
            flash("Todos los campos son obligatorios", "danger")
    return render_template("register.html")

@app.route("/cart")
def cart():
    if not is_logged_in():
        flash("Debes iniciar sesión para ver el carrito", "warning")
        return redirect(url_for("login"))

    carrito = api_request("GET", "/cart", token_required=True)
    return render_template("cart.html", carrito=carrito)

@app.route("/add-to-cart/<int:producto_id>")
def add_to_cart(producto_id):
    if not is_logged_in():
        flash("Debes iniciar sesión para agregar productos", "warning")
        return redirect(url_for("login"))

    res = api_request("POST", f"/cart/add/{producto_id}", token_required=True)

    if res.get("success"):
        flash("Producto agregado al carrito", "success")
    else:
        flash(res.get("error", "No se pudo agregar al carrito"), "danger")

    return redirect(url_for("cart"))

@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión", "info")
    return redirect(url_for("index"))

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
