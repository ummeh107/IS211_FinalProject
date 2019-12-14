from flask import Flask, render_template, request, url_for, redirect, session
import sqlite3 as lite
import os
import re
import datetime
import bs4_products as bsp

app = Flask(__name__)
app.secret_key = os.urandom(24)


global cart, registerd, categoryList, products
registerd = ''
cart = []
categoryList = []
products = []


@app.route('/')
def index():
    return redirect('/dashboard')


@app.route('/login')
def login_user():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    error = None
    cart.clear()
    mail = request.form['mail']
    password = request.form['password']
    user = query_fetch_data(
        "select * from Registration where email=? and password=?", (mail, password))
    if user:
        # print(user)
        global registerd
        registerd = user
        session['mail'] = request.form['mail']
        return redirect('/dashboard')
    else:
        error = "Wrong username or password"
        return render_template("login.html", error=error)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        first_name = request.form['first']
        last_name = request.form['last']
        email = request.form['email']
        gender = request.form['gender']
        city = request.form['city']
        password = request.form['password']
        if first_name != '' and last_name != '' and gender != '' and city != 'Select City' and password != '' and email != '':
            registerd = query_fetch_data(
                "Insert into Registration (first_name, last_name, email, gender, city, password) values(?,?,?,?,?,?)",
                (first_name, last_name, email, gender, city, password), "POST")
            # print(registerd)
            if registerd:
                return render_template('login.html')
            else:
                return render_template('registration.html', error="Please try again!")
        else:
            return render_template('registration.html',
                                   error="Field can not be empty!")


@app.route('/dashboard', methods=['GET'])
def dashboard():
    global products, categoryList
    categoryList = []
    categoryList = bsp.get_category()
    products = bsp.product_by_category()
    # print(registerd)
    if 'mail' in session:
        return render_template('dashboard.html', products=products, categoryList=categoryList, register=registerd, cart=cart)
    else:
        return render_template('dashboard.html', products=products, categoryList=categoryList)


@app.route('/dashboard/<item>', methods=['GET'])
def dashboard_category(item):
    # print(cart)
    global products
    products = []
    # print(categoryList)
    for i, dic in enumerate(categoryList):
        if dic['category'] == item:
            item = i
            # print(i)
    products = bsp.product_by_category(int(item))
    # print(registerd)
    if 'mail' in session:
        return render_template('dashboard.html', products=products, categoryList=categoryList, register=registerd, cart=cart)
    else:
        return render_template('dashboard.html', products=products, categoryList=categoryList)


@app.route('/dashboard/details/<id>', methods=['GET'])
def details_products(id):
    # print(cart)
    global product_id
    product_id = id
    if 'mail' in session:
        return render_template('details.html', product=products[int(id) - 1], categoryList=categoryList, register=registerd, cart=cart)
    else:
        return render_template('details.html', product=products[int(id) - 1], categoryList=categoryList)


@app.route('/cart/buy', methods=['GET', 'POST'])
def buy_product():
    total_price = 0
    date_now = datetime.datetime.now()
    if request.method == 'GET':
        print(cart)
        for item in cart:
            total_price = total_price + float(item['price'].split('$')[1])
        return render_template('payment.html', cart=cart, price=total_price, register=registerd, categoryList=categoryList)
    elif request.method == 'POST':
        for item in cart:
            total_price = total_price + float(item['price'].split('$')[1])
        saved = query_fetch_data(
            "insert into Users(reg_id, item, amount, date) values(?,?,?,?)", (registerd[0], len(cart), total_price, date_now), "POST")
        print(saved)
        if saved:
            cart.clear()
            return redirect('/user-profile')


@app.route('/user-profile', methods=['GET'])
def user_profile():
    id = registerd[0]
    user_profile = query_fetch_data(
        "select * from Users where reg_id=?", str(id), "GET")
    print(user_profile)
    if 'mail' in session:
        return render_template('user_profile.html', user=user_profile, register=registerd, categoryList=categoryList)
    else:
        return render_template('user_profile.html', user=user_profile, categoryList=categoryList)


@app.route('/add/cart/', methods=['POST'])
def cart_add():
    if 'mail' in session:
        cart.append(products[int(product_id) - 1])
        return redirect("/dashboard")

    else:
        return redirect("/login")


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    registerd = ''
    cart.clear()
    return redirect('/dashboard')


# Query Generator


def query_fetch_data(query, item=None, method=None):
    conn = lite.connect('E-App.db')
    db = conn.cursor()
    if item == None:
        db.execute(query)
    elif method == "POST":
        try:
            print("user")
            db.execute(query, item)
            conn.commit()
            return True
        except:
            return False
    elif method == "GET":
        try:
            print(query, item)
            db.execute(query, item)
            return db.fetchall()
        except:
            return False
    else:
        try:
            print("3")
            db.execute(query, item)
            return db.fetchone()
        except:
            return False
    return db.fetchall()


if __name__ == '__main__':
    app.run(debug=True, port=5001)
