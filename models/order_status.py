from models import db
from datetime import datetime



class OrderStatus(db.Model):

    __tablename__ = "order_status"



    id = db.Column(
        db.Integer,
        primary_key=True
    )


    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False
    )


    status = db.Column(
        db.String(50),
        nullable=False
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



    # Relationship

    order = db.relationship(
        "Order",
        back_populates="status_history"
    )