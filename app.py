from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clothes_shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

        hash_password = password #todo

        clients = Client.query.all()


        #...

        return render_template("products_a.html")
    else:
        return render_template("login.html")


@app.route("/login/registration", methods=['POST', 'GET'])
def show_registration():
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']

        hash_password = password #todo




        new_client = Client(name=name, surname=surname, phone=phone, email=email, password=hash_password)

        try:
            db.session.add(new_client)
            db.session.commit()
            return redirect("/")
        except:
            return "Помилка при додаванні статті"
    else:
        return render_template("registration.html")




@app.route("/about")
def about():
    return render_template("about.html")










@app.route("/product")
def product():
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
            return "Помилка при додаванні статті"
    else:
        return render_template("product_create.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


