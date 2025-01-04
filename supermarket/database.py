from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class UserDetails(db.Model):
    __tablename__ = 'user_details'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    contact_number = db.Column(db.String(30), nullable=False)
    email_id = db.Column(db.String(100), unique=True, nullable=False)
    normal_password = db.Column(db.String(255), nullable=False)
    encrypted_password = db.Column(db.String(255), nullable=False)

class StoreUserDetails(db.Model):
    __tablename__ = 'store_user_details'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    contact_number = db.Column(db.String(30), nullable=False)
    email_id = db.Column(db.String(100), nullable=False)
    normal_password = db.Column(db.String(255), nullable=False)
    encrypted_password = db.Column(db.String(255), nullable=False)
    designation = db.Column(db.String(20), nullable=False)  

class Products(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    rate = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Purchases(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_details.user_id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rate = db.Column(db.Float, nullable=False)

class Database:
    def __init__(self):
        self.db = db

    def add_user(self, data):
        user = UserDetails(
            first_name=data["first_name"],
            last_name=data["last_name"],
            age=data["age"],
            sex=data["sex"],
            contact_number=data["contact_number"],
            email_id=data["email_id"],
            normal_password=data["normal_password"],
            encrypted_password=data["encrypted_password"],
        )
        self.db.session.add(user)
        self.db.session.commit()


    def store_user(self, data):
        user = StoreUserDetails(**data)
        self.db.session.add(user)
        self.db.session.commit()

    def get_user_by_email(self, email_id):
        return UserDetails.query.filter_by(email_id=email_id).first()

    def add_product(self, data):
        product = Products(**data)
        self.db.session.add(product)
        self.db.session.commit()

    def delete_product(self, product_id):
        product = Products.query.get(product_id)
        if product:
            self.db.session.delete(product)
            self.db.session.commit()

    def update_product_rate(self, product_id, rate):
        product = Products.query.get(product_id)
        if product:
            product.rate = rate
            self.db.session.commit()

    def get_purchases(self, start_date, end_date):
        return Purchases.query.filter(Purchases.purchase_date.between(start_date, end_date)).all()

    def get_users_with_high_purchase(self):
        return db.session.query(
            UserDetails.first_name,
            UserDetails.last_name,
            db.func.sum(Purchases.quantity * Purchases.rate).label('total_purchase_amount')
        ).join(Purchases).group_by(
            UserDetails.first_name,
            UserDetails.last_name,
            db.func.date(Purchases.purchase_date)
        ).having(
            db.func.sum(Purchases.quantity * Purchases.rate) > 800
        ).all()

    def get_shampoo_sales(self):
        return db.session.query(db.func.sum(Purchases.quantity * Purchases.rate)).filter(Purchases.item_name == 'Shampoo').filter(Purchases.purchase_date >= datetime.now() - timedelta(days=10)).scalar()
