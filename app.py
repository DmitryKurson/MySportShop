from itertools import product

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clothes_shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def compute_sha512_hash(input_string):
    sha512_hash = hashlib.sha512()
    sha512_hash.update(input_string.encode('utf-8'))
    return sha512_hash.hexdigest()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracker_code = db.Column(db.Integer, nullable=False)
    goods = db.Column(db.String(1000), nullable=False)
    client_phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Order %r>' % self.id


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.id


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    cart = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Client %r>' % self.id




@app.route("/", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        hash_password = compute_sha512_hash(password)

        clients = Client.query.all()
        found_user = None
        for i in clients:
            if i.email == login:
                if i.password == hash_password:
                    found_user = i
                    break
        if found_user == None:
            return redirect("/")
        if found_user.email.endswith("admin"):
            return render_template("welcome_page.html")
        else:
            products = Product.query.all()
            return render_template("product_u.html", products=products, c_id=found_user.id)
    else:
        return render_template("login.html")


@app.route("/registration", methods=['POST', 'GET'])
def show_registration():
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        hash_password = compute_sha512_hash(password)
        new_client = Client(name=name, surname=surname, phone=phone, email=email, password=str(hash_password),cart="")
        try:
            db.session.add(new_client)
            db.session.commit()
            return redirect("/")
        except:
            return "Помилка при додаванні клієнта"
    else:
        return render_template("registration.html")

@app.route("/clients")
def show_clients():
    clients = Client.query.all()
    return render_template("clients.html", clients=clients)

@app.route("/<int:c_id>/buy/<int:id>")
def buy(c_id, id):
    client = Client.query.get_or_404(c_id)
    client.cart += Product.query.get_or_404(id).title + " "
    products = Product.query.all()
    db.session.commit()
    return render_template("product_u.html", products=products, id=client.id)

@app.route("/<int:id>/cart")
def show_cart(id):
    client = Client.query.get_or_404(id)
    client_cart = client.cart

    return render_template("cart.html", cart=client_cart, id=client.id)

@app.route("/<int:id>/buy/finish")
def finish(id):
    client = Client.query.get_or_404(id)
    client.cart = ""
    products = Product.query.all()
    db.session.commit()
    return render_template("product_u.html", products=products, id=client.id)


@app.route("/products")
def show_products():
    products = Product.query.all()
    return render_template("product_a.html", products=products)

@app.route("/product/create", methods=['POST', 'GET'])
def create_product():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        country = request.form['country']

        new_product = Product(title=title, price=price, country=country)

        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect("/")
        except:
            return "Помилка при додаванні товару"
    else:
        return render_template("product_create.html")


@app.route("/product/<int:id>")
def product_detail(id):
    product = Product.query.get(id)
    return render_template("product_details.html", product=product)

@app.route("/product/<int:id>/update", methods=['POST', 'GET'])
def product_update(id):
    product = Product.query.get(id)
    if request.method == "POST":
        product.title = request.form['title']
        product.price = request.form['price']
        product.country = request.form['country']

        try:
            db.session.commit()
            return redirect("/products")
        except:
            return "Сталася помилка редагування"

    else:
        return render_template("product_update.html", product=product)

@app.route("/product/<int:id>/delete", methods=['POST', 'GET'])
def product_delete(id):
    product = Product.query.get(id)
    try:
        db.session.delete(product)
        db.session.commit()
        return redirect("/products")
    except:
        return "Сталася помилка видалення"




@app.route("/client/<int:id>")
def client_detail(id):
    client = Client.query.get(id)
    return render_template("client_details.html", client=client)

@app.route("/client/<int:id>/update", methods=['POST', 'GET'])
def client_update(id):
    client = Client.query.get(id)
    if request.method == "POST":
        client.name = request.form['name']
        client.surname = request.form['surname']
        client.phone = request.form['phone']

        try:
            db.session.commit()
            return redirect("/clients")
        except:
            return "Сталася помилка редагування"
    else:
        return render_template("client_update.html", client=client)

@app.route("/client/<int:id>/delete", methods=['POST', 'GET'])
def client_delete(id):
    client = Client.query.get(id)
    try:
        db.session.delete(client)
        db.session.commit()
        return redirect("/clients")
    except:
        return "Сталася помилка видалення"

@app.route("/client/<int:id>/reset_password")
def client_reset_password(id):
    client = Client.query.get(id)
    try:
        client.password = compute_sha512_hash("1234")
        db.session.commit()
        return redirect("/clients")
    except:
        return "Сталася помилка скидання паролю"

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


