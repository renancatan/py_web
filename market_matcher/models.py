from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(20), nullable=True)
    market = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(200), nullable=True)
    market_group = db.Column(db.String(20), nullable=True)


