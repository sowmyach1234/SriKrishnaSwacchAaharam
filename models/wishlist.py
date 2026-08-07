from models import db
from datetime import datetime



class Wishlist(db.Model):

    __tablename__="wishlist"


    id=db.Column(
        db.Integer,
        primary_key=True
    )


    product_id=db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )


    created_at=db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



    product=db.relationship(
        "Product"
    )