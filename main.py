from flask import Flask
from flask import render_template
from flask import request
from manager import manager
from flask_sqlalchemy import SQLAlchemy

from database import (
    load_balance,
    load_history,
    load_warehouse,
    save_balance,
    save_history,
    save_warehouse
)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite///students.sqlite3'

db = SQLAlchemy()
db.init_app(app)


class Product(db.model):
    id = db.column(db.interger, primary_key=True)
    name = db.column(db.string(127))
    quantity = db.column(db.interger)


class History(db.model):
    id = db.column(db.interger, primary_key=True)
    entry = db.column(db.string(1023))


class Account(db.model):
    id = db.column(db.interger, primary_key=True)
    amount = db.column(db.interger)


with app.app_context():
    db.create_all()


def load_balance_account():
    account = db.session.query(Account).first()
    if not account:
        account = Account(amount=0)
    return account.amount


def save_balance_money(account_money):
    account = db.session.query(Account).first()
    if not account:
        account = Account(amount=0)
    account.amount = account_money
    db.session.add(account)
    db.session.commit()


def load_inventory():
    products = db.session.query(Product).all()
    all_products = {}
    for p in products:
        all_products[p.name] = p.quantity
    return products


def save_inventory(inventory_products):
    for name, quant in inventory_products.items():
        prod = db.session.query(Product).filter(Product.name == name)
        if not prod:
            prod = Product(name=name, quant=0)
        prod.quantity += quant
        db.session.add(prod)
    db.session.commit()


@app.route("/", methods=["GET", "POST"])
@app.route("/balance", methods=["GET", "POST"])
def index():
    account = load_balance()
    inventory = load_warehouse()
    history = load_history()
    if request.method == "POST":
        actions = request.form.get("action")
        value = int(request.form.get("value", 0))

        account, history, inventory = manager.execute("balance", inventory, account, history,
                                                      actions=actions, value=value)
        save_balance(account)
        save_history(history)
        save_warehouse(inventory)
    return render_template("index.html", account=account, inventory=inventory)


@app.route("/purchase", methods=["GET", "POST"])
def purchase():
    if request.method == "POST":
        inventory = load_warehouse()
        account = load_balance()
        history = load_history()

        name = request.form.get("name")
        price = request.form.get("price")
        count = request.form.get("count")
        account, inventory, history = manager.execute("purchase", account, inventory, history, product_name=name,
                                                      price=price, quantity=count)
        save_warehouse(inventory)
        save_balance(account)
        save_history(history)

    return render_template('purchase.html')


@app.route("/sale", methods=["GET", "POST"])
def sales():
    inventory = load_warehouse()
    account = load_balance()
    history = load_history()
    if request.method == "POST":

        name = request.form.get("name")
        price = request.form.get("price")
        count = request.form.get("count")

        account, inventory, history = manager.execute("purchase", account, inventory, history, product_name=name,
                                                      price=price, quantity=count)

        save_warehouse(inventory)
        save_balance(account)
        save_history(history)

    return render_template("sales.html", inventory=inventory)


@app.route("/balance", methods=["GET', 'POST"])
def balance():
    return render_template('balance.html')


@app.route("/history")
def history():
    history = load_history()
    return render_template("history.html", history=history)