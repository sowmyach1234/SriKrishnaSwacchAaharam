from models import db



class OrderItem(db.Model):


    __tablename__="order_items"



    id=db.Column(
        db.Integer,
        primary_key=True
    )



    order_id=db.Column(
        db.Integer,
        db.ForeignKey(
            "orders.id"
        ),
        nullable=False
    )



    product_id=db.Column(
        db.Integer,
        db.ForeignKey(
            "products.id"
        )
    )



    product_name=db.Column(
        db.String(100)
    )



    quantity=db.Column(
        db.Integer
    )



    price=db.Column(
        db.Float
    )



    weight=db.Column(
        db.String(20)
    )



    product=db.relationship(
        "Product"
    )