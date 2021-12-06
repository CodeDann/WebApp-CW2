from app import db
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash

class NumProduct(db.Model):
    order_id = db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True)
    prod_id = db.Column('prod_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
    product = db.relationship("Product")
    quantity = db.Column(db.Integer)

    def __init__(self, order, prod_id, prod, quant):
        self.order_id = order
        self.prod_id = prod_id
        self.product = prod
        self.quantity = quant


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'))
    contents = db.relationship("NumProduct")
    price = db.Column(db.Float)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(500))
    product_code = db.Column(db.String(10))
    product_thumbnail = db.Column(db.String(10))
    price = db.Column(db.Float)
    available = db.Column(db.Integer)
    # inOrder = relationship("NumProduct")

    def __init__(self, title, product_code, product_thumbnail, price, available):
        self.title = title
        self.product_code = product_code
        self.product_thumbnail = product_thumbnail
        self.price = price
        self.available = available


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    name = db.Column(db.String(20))
    password = db.Column(db.String(20))
    orders = relationship("Order")

    def __init__(self, impemail, impname, imppass):
        self.email = impemail
        self.name = impname
        self.password = generate_password_hash(imppass)

    def verify_password(self, imppass):
        return check_password_hash(self.password, imppass)

    def update_password(self, imppass):
        self.password = generate_password_hash(imppass)
