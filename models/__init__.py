from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


from models.product import Product
from models.order import Order
from models.order_item import OrderItem
from models.customer import Customer
from models.stock_history import StockHistory



from models.inventory_transaction import InventoryTransaction


from models.admin_activity import AdminActivity