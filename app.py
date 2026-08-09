from flask import Flask
from config import Config

# Database
from models import db
# Product Model
from models.product import Product

# Models
from models.cart import Cart
from models.wishlist import Wishlist
from models.order import Order
from models.order_item import OrderItem
from models.order_status import OrderStatus
from models.inventory_transaction import InventoryTransaction

# ==========================
# CUSTOMER ROUTES
# ==========================
from routes.home import home
from routes.products import products
from routes.categories import categories
from routes.about import about
from routes.blog import blog
from routes.contact import contact
from routes.cart import cart
from routes.wishlist import wishlist
from routes.checkout import checkout

# ==========================
# ADMIN ROUTES
# ==========================
from routes.admin import admin
from routes.admin_products import admin_products
from routes.admin_orders import admin_orders
from routes.admin_customers import customers
from routes.customer import customer

from routes.admin_settings import settings

from routes.admin_activity import activity

# ==========================
# ANALYTICS
# ==========================
from routes.admin_analytics import analytics
from routes.export import export

# ==========================
# INVENTORY
# ==========================
from routes.admin_inventory import admin_inventory
from routes.inventory_actions import inventory_actions
from routes.stock_history import stock_history
from routes.inventory_analytics import inventory_analytics
from routes.inventory_reports import inventory_reports

# ==========================
# INVOICE
# ==========================
from routes.invoice import invoice


from routes.executive import executive

app = Flask(__name__)

app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

db.init_app(app)

# =====================================
# REGISTER BLUEPRINTS
# =====================================

# Customer
app.register_blueprint(home)
app.register_blueprint(products)
app.register_blueprint(cart)
app.register_blueprint(categories)
app.register_blueprint(about)
app.register_blueprint(blog)
app.register_blueprint(contact)
app.register_blueprint(wishlist)
app.register_blueprint(checkout)

# Admin
app.register_blueprint(admin)
app.register_blueprint(admin_products)
app.register_blueprint(admin_orders)
app.register_blueprint(customers)
app.register_blueprint(customer)

app.register_blueprint(settings)
app.register_blueprint(activity)

# Inventory
app.register_blueprint(admin_inventory)
app.register_blueprint(inventory_actions)
app.register_blueprint(stock_history)
app.register_blueprint(inventory_analytics)
app.register_blueprint(inventory_reports)

# Analytics
app.register_blueprint(analytics)
app.register_blueprint(export)

# Invoice
app.register_blueprint(invoice)


app.register_blueprint(executive)

# =====================================
# CREATE DATABASE + SEED PRODUCTS
# =====================================

with app.app_context():

    db.create_all()

    # ---------------------------------
    # ADD DEFAULT PRODUCTS IF DATABASE
    # IS EMPTY
    # ---------------------------------

    if Product.query.count() == 0:

        products = [

            # ==========================
            # COLD PRESSED OILS
            # ==========================

            {
                "name": "Groundnut Oil",
                "category": "Cold Pressed Oils",
                "description": "Traditional wooden pressed groundnut oil with natural nutrients.",
                "price": 450,
                "stock": 50,
                "image": "groundnut_oil.jpg"
            },

            {
                "name": "Sesame Oil",
                "category": "Cold Pressed Oils",
                "description": "Pure cold pressed sesame oil prepared naturally.",
                "price": 520,
                "stock": 40,
                "image": "sesame_oil.jpg"
            },

            {
                "name": "Coconut Oil",
                "category": "Cold Pressed Oils",
                "description": "Fresh coconut oil extracted using traditional methods.",
                "price": 600,
                "stock": 30,
                "image": "coconut_oil.jpg"
            },


            # ==========================
            # TRADITIONAL PICKLES
            # ==========================

            {
                "name": "Mango Pickle",
                "category": "Traditional Pickles",
                "description": "Authentic Andhra style mango pickle.",
                "price": 250,
                "stock": 60,
                "image": "mango_pickle.jpg"
            },

            {
                "name": "Gongura Pickle",
                "category": "Traditional Pickles",
                "description": "Traditional homemade gongura pickle.",
                "price": 280,
                "stock": 45,
                "image": "gongura_pickle.jpg"
            },


            # ==========================
            # ORGANIC MILLETS
            # ==========================

            {
                "name": "Foxtail Millet",
                "category": "Organic Millets",
                "description": "Healthy organic foxtail millet rich in nutrition.",
                "price": 180,
                "stock": 70,
                "image": "foxtail_millet.jpg"
            },

            {
                "name": "Little Millet",
                "category": "Organic Millets",
                "description": "Natural little millet for healthy lifestyle.",
                "price": 200,
                "stock": 50,
                "image": "little_millet.jpg"
            },


            # ==========================
            # A2 COW GHEE
            # ==========================

            {
                "name": "A2 Cow Ghee",
                "category": "A2 Cow Ghee",
                "description": "Pure A2 cow ghee prepared traditionally.",
                "price": 900,
                "stock": 25,
                "image": "a2_ghee.jpg"
            },


            # ==========================
            # DRY FRUITS
            # ==========================

            {
                "name": "California Almonds",
                "category": "Dry Fruits",
                "description": "Premium quality almonds.",
                "price": 750,
                "stock": 35,
                "image": "almonds.jpg"
            },


            # ==========================
            # ORGANIC SWEETS
            # ==========================

            {
                "name": "Millet Chikki",
                "category": "Organic Sweets",
                "description": "Healthy millet sweet made with jaggery.",
                "price": 150,
                "stock": 80,
                "image": "millet_chikki.jpg"
            }

        ]


        for item in products:

            product = Product(

                product_name=item["name"],

                category=item["category"],

                description=item["description"],

                price=item["price"],

                stock=item["stock"],

                image=item["image"],

                organic=True

            )

            db.session.add(product)


        db.session.commit()

        print("Default products inserted successfully.")

# =====================================
# CART COUNT
# =====================================

@app.context_processor
def cart_counter():

    cart_count = db.session.query(
        db.func.sum(Cart.quantity)
    ).scalar()

    if cart_count is None:
        cart_count = 0

    return {
        "cart_count": cart_count
    }

# =====================================
# ERROR PAGE
# =====================================

@app.errorhandler(404)
def page_not_found(error):
    return "Page Not Found", 404

if __name__ == "__main__":
    app.run()