from models import db
from datetime import datetime


class Order(db.Model):

    __tablename__ = "orders"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id")
    )


    customer_name = db.Column(
        db.String(100)
    )


    customer_phone = db.Column(
        db.String(20)
    )


    customer_address = db.Column(
        db.Text
    )


    total_amount = db.Column(
        db.Float,
        default=0
    )


    status = db.Column(
        db.String(50),
        default="Pending"
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    items = db.relationship(
        "OrderItem",
        backref="order",
        lazy=True,
        cascade="all, delete-orphan"
    )


    status_history = db.relationship(
        "OrderStatus",
        back_populates="order",
        lazy=True,
        cascade="all, delete-orphan"
    )