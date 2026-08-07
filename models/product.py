from datetime import datetime

from models import db



class Product(db.Model):

    __tablename__ = "products"



    # ==========================
    # PRIMARY KEY
    # ==========================

    id = db.Column(
        db.Integer,
        primary_key=True
    )



    # ==========================
    # PRODUCT INFORMATION
    # ==========================

    product_name = db.Column(
        db.String(200),
        nullable=False
    )


    category = db.Column(
        db.String(100),
        nullable=False
    )


    description = db.Column(
        db.Text
    )


    image = db.Column(
        db.String(200)
    )



    # ==========================
    # PRICE & STOCK
    # ==========================

    price = db.Column(
        db.Float,
        nullable=False
    )


    stock = db.Column(
        db.Integer,
        default=0
    )


    # Minimum quantity before alert

    minimum_stock = db.Column(
        db.Integer,
        default=5
    )



    # ==========================
    # PRODUCT TYPE
    # ==========================

    organic = db.Column(
        db.Boolean,
        default=True
    )



    # ==========================
    # INVENTORY TRACKING
    # ==========================

    last_updated = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )



    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



    # ==========================
    # HELPER FUNCTIONS
    # ==========================

    @property
    def stock_status(self):

        if self.stock == 0:

            return "Out of Stock"


        elif self.stock <= self.minimum_stock:

            return "Low Stock"


        else:

            return "Available"



    def __repr__(self):

        return f"<Product {self.product_name}>"