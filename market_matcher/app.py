from flask import Flask
from models import db, Product  # to run sql migrations use -> .models
from flask_migrate import Migrate
from flask import render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market_matcher.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
# Only use the following if you're NOT using Flask-Migrate.
# Otherwise, use migration commands to manage your database.
"""
# with app.app_context():
#     db.create_all()  # This line creates the tables.

    # Commented out section since products are already added
    
    tomato = Product(name='Tomato', market='Market A', price=2.99)
    tomato2 = Product(name='Tomato', market='Market A', price=3.50)
    milk = Product(name='Milk', market='Market B', price=1.49)
    milk2 = Product(name='Milk', market='Market C', price=2.49)

    db.session.add(tomato)
    db.session.add(milk)
    db.session.add(tomato2)
    db.session.add(milk2)
    db.session.commit()
    """

@app.route("/")
def home():
    return "hello, worlds"

@app.route("/products")
def list_products():
    products = Product.query.all()  # retrieve all products
    return render_template("products.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)

