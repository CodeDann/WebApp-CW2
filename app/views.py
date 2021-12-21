from flask import render_template, request, session, redirect, url_for, flash
from app import app, db, admin
from flask_admin.contrib.sqla import ModelView
# from app import app
from . import db, models
from .forms import AddToBasket, RemoveFromBasket, LoginForm, SingupForm, ChangePassword, ChangeName
from .models import Product, User, Order, NumProduct
from collections import Counter
import logging

# add admin to allow easier editing of the DB
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Order, db.session))


@app.route('/', methods=['GET', 'POST'])
def entry():
    message = ' Please log into your account if you do not have an account please register a new one'
    # prompt user to login and verify information
    form1 = LoginForm()
    form2 = SingupForm()

    # check if user is in the session
    if 'user' in session:
        return redirect(url_for('index'))

    # handle login form
    if form1.validate_on_submit():
        given_email = form1.email.data.lower()
        given_pass = form1.password.data
        query = User.query.filter_by(email=given_email).first()
        if query is None:
            app.logger.error('unsuccessful login attempt')
            message = str("Username: " + given_email + " does not exist")
        else:
            if query.verify_password(given_pass):
                session['user'] = query.id
                app.logger.warning('%s: logged in successfully', query.name)
                return redirect(url_for('index'))
            else:
                app.logger.error('%s: attempted login with incorrect password', query.name)
                message = str("Incorrect password for " + given_email + ": If you've forgotten it please create a new account")

    # handle signup form
    if form2.validate_on_submit():
        given_email = form2.email.data.lower()
        given_name = form2.name.data
        given_pass = form2.password.data
        # add new record with given data
        newUser = User(given_email, given_name, given_pass)
        app.logger.warning('%s :created account', newUser.name)
        message = str("Account Created! - Now please log in...")
        db.session.add(newUser)
        db.session.commit()
        return render_template('entry.html', title='Login', form1=form1, form2=form2, message=message)

    return render_template('entry.html', title='Login', form1=form1, form2=form2, message=message)


@app.route('/logout', )
def logout():
    sessionId = session.get('user')
    user = User.query.filter_by(id=sessionId).first()
    app.logger.warning('%s: logged out', user.name)
    session.pop('user', None)
    session.pop('basket', None)
    return redirect(url_for('entry'))

@app.route('/storeinfo', methods=['GET', 'POST'])
def storeinfo():
    sessionId = session.get('user')
    user = User.query.filter_by(id=sessionId).first()
    return render_template('storeinfo.html', title='Store Information', User=user.name)


@app.route('/changepass', methods=['GET', 'POST'])
def change():
    form1 = ChangePassword()
    form2 = ChangeName()
    sessionId = session.get('user')
    user = User.query.filter_by(id=sessionId).first()

    alertStatus = None
    # update password
    if form1.validate_on_submit():
        # get info from form
        given_oldpass = form1.oldpassword.data
        given_newpass = form1.password.data
        # check its correct and update if so
        if user.verify_password(given_oldpass):
            user.update_password(given_newpass)
            db.session.commit()
            alertStatus = 1
            app.logger.warning('%s: successful password update', user.name)
        else:
            app.logger.error('%s: successful password update', user.name)
            alertStatus = 0

        return render_template('changepass.html', title='Change Password', form1=form1, form2=form2, User=user.name, alert=alertStatus)

    elif form2.validate_on_submit():
        given_oldname = form2.oldname.data
        given_newname = form2.newname.data
        # check its correct and update if so
        if user.name == given_oldname:
            user.name = given_newname
            db.session.commit()
            alertStatus = 2
            app.logger.warning('%s: successful name update', user.name)
        else:
            app.logger.error('%s: unsuccessful name update', user.name)
            alertStatus = 3

        return render_template('changepass.html', title='Change Password', form1=form1, form2=form2, User=user.name, alert=alertStatus)

    return render_template('changepass.html', title='Change Password', form1=form1, form2=form2, User=user.name, alert=alertStatus)


@app.route('/index', methods=['GET', 'POST'])
def index():
    sessionId = session.get('user')
    newUser = session.get('newUser')

    user = User.query.filter_by(id=sessionId).first()

    # on homepage we want to just display all products
    data = models.Product.query.all()
    images = []
    for item in data:
        images.append(url_for('static', filename="/img/" + item.product_thumbnail))

    # ensure a basket is in the session
    if 'basket' not in session:
        basketArr = []
        session['basket'] = basketArr
    else:
        basketArr = session.get('basket')

    form = AddToBasket()
    if request.method == 'POST':
        # add given product to session basket
        product = request.form.get('basketer')
        basketArr.append(product)
        session['basket'] = basketArr
        app.logger.warning('%s: added item to basket', user.name)

    return render_template('index.html', title='Homepage', data=data, form=form, images=images, User=user.name)


@app.route('/basket', methods=['GET', 'POST'])
def basket():
    data = []
    alert = 0
    # get the basket from session
    basketArr = session.get('basket')
    if not basketArr:
        canOrder = False
    else:
        canOrder = True

    sessionId = session.get('user')
    user = User.query.filter_by(id=sessionId).first()

    basketArr.sort()

    # count occurances of each product in basket and return as a 2d array called data
    countedArr = Counter(basketArr)
    for key in countedArr:
        product = Product.query.filter_by(product_code=key).first()
        quantity = countedArr[key]
        data.append([product, quantity])

    # remove from basket
    if (request.method == 'POST') and ('remover' in request.form.to_dict().keys()):
        # remove given product from session basket
        product = request.form.get('remover')
        try:
            basketArr.remove(product)
        except ValueError:
            print("Error: trying to remove product not in basket")
            app.logger.error('%s: Error tried to remove item not in basket', user.name)

        basketArr.sort()
        session['basket'] = basketArr
        # update basket and data
        fillDatafromBasket(basketArr)
        app.logger.warning('%s: removed item from basket', user.name)
        return redirect(url_for('basket'))

    # go to users orders
    elif (request.method == 'POST') and ('gotoorders' in request.form.to_dict().keys()):
        return redirect(url_for('orders'))

    # place order
    elif (request.method == 'POST') and ('placeOrder' in request.form.to_dict().keys()):
        # check there are items in an order ( no point in ordering an empty order )
        if session['basket']:
            # create and fill order
            o = Order()
            o.user_id = user.id
            o.price = basketSummary(data)
            db.session.add(o)
            db.session.commit()
            for item in data:
                instance = NumProduct(o.id, item[0].id, item[0], item[1])
                db.session.add(instance)
            db.session.commit()
            # clear basket and data and set order alert
            session['basket'] = []
            data = []
            alert = 1
            canOrder = False
            app.logger.warning('%s: placed an order', user.name)
            return render_template('basket.html', title='Basket', data=data, total=basketSummary(data),
                                   User=user.name, alert=alert, canOrder=canOrder)
        else:
            alert = 2
            return render_template('basket.html', title='Basket', data=data, total=basketSummary(data),
                                   User=user.name, alert=alert, canOrder=canOrder)

    return render_template('basket.html', title='Basket', data=data, total=basketSummary(data),
                           User=user.name, alert=alert, canOrder=canOrder)

def basketSummary( data ):
    basketTotal = 0
    for item in data:
        basketTotal += item[0].price * item[1]
    return round(basketTotal, 2)

def fillDatafromBasket( basketArr):
    # recount amounts and clear data
    countedArr = Counter(basketArr)
    data = []
    # refill data
    for key in countedArr:
        product = Product.query.filter_by(product_code=key).first()
        quantity = countedArr[key]
        data.append([product, quantity])


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    sessionId = session.get('user')
    user = User.query.filter_by(id=sessionId).first()
    data = []
    for order in user.orders:
        data.append(order)

    return render_template('orders.html', title='Orders', data=data, User=user.name)
