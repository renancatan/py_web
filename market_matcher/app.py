from flask import Flask, render_template, request
from models import db, Product  # to run sql migrations use -> .models
from flask_migrate import Migrate
from sqlalchemy import or_

COLUMN_PRODUCT_NAME = "product_name"
COLUMN_MARKET = "market"
COLUMN_PRICE = "price"
PAGINATION_SIZE = 20

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


@app.route('/products', methods=['GET'])
def list_products():
    # products = Product.query.all()
    # return render_template('products.html', products=products)

    # Get the page number from the request, default to 1 if not found
    page = request.args.get('page', 1, type=int)

    # Instead of using .all(), use paginate()
    pagination = Product.query.paginate(page=page, per_page=PAGINATION_SIZE, error_out=False)
    products = pagination.items

    return render_template('products.html', products=products, pagination=pagination)


@app.route('/search', methods=['GET'])
def search_products():
    search_term = request.args.get('search')
    page = request.args.get('page', 1, type=int)

    # This becomes True if search_term is not None or empty.
    search_performed = bool(search_term)

    if search_performed:
        # Searching for matching products.
        pagination = Product.query.filter(
            or_(
                getattr(Product, COLUMN_PRODUCT_NAME).contains(search_term),
                getattr(Product, COLUMN_MARKET).contains(search_term)
            )
        ).paginate(page=page, per_page=PAGINATION_SIZE)

        products = pagination.items
        matches_count = len(products)

    else:
        # If no search term provided, retrieve all products (or as per other default behavior you might define)
        pagination = Product.query.paginate(page=page, per_page=PAGINATION_SIZE)
        products = pagination.items
        matches_count = None  # No count is provided if no search was performed.

    return render_template('products.html',
                           products=products,
                           matches_count=matches_count,
                           pagination=pagination,
                           search_performed=search_performed)


if __name__ == "__main__":
    app.run(debug=True)
