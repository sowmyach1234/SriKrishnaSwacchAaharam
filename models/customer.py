from models import db
from datetime import datetime



class Customer(db.Model):

    __tablename__="customers"



    id=db.Column(
        db.Integer,
        primary_key=True
    )


    name=db.Column(
        db.String(100),
        nullable=False
    )


    phone=db.Column(
        db.String(20)
    )


    email=db.Column(
        db.String(100)
    )


    address=db.Column(
        db.Text
    )


    total_orders=db.Column(
        db.Integer,
        default=0
    )


    total_spent=db.Column(
        db.Float,
        default=0
    )


    segment=db.Column(
        db.String(50),
        default="New Customer"
    )


    created_at=db.Column(
        db.DateTime,
        default=datetime.utcnow
    )