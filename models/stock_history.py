from datetime import datetime

from models import db


class StockHistory(db.Model):

    __tablename__ = "stock_history"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )


    product_name = db.Column(
        db.String(200)
    )


    old_stock = db.Column(
        db.Integer
    )


    new_stock = db.Column(
        db.Integer
    )


    change = db.Column(
        db.Integer
    )


    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    product = db.relationship(
        "Product",
        backref="stock_history"
    )