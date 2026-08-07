from flask import Flask
from config import Config

# Database
from models import db

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
# CREATE DATABASE
# =====================================

with app.app_context():
    db.create_all()

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