from datetime import datetime

from models import db



class InventoryTransaction(db.Model):

    __tablename__ = "inventory_transactions"



    id = db.Column(
        db.Integer,
        primary_key=True
    )


    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )


    transaction_type = db.Column(
        db.String(20),
        nullable=False
    )
    # IN / OUT



    quantity = db.Column(
        db.Integer,
        nullable=False
    )



    previous_stock = db.Column(
        db.Integer,
        nullable=False
    )



    new_stock = db.Column(
        db.Integer,
        nullable=False
    )



    created_by = db.Column(
        db.String(100),
        default="Admin"
    )



    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )





    # Relationship

    product = db.relationship(
        "Product",
        backref="inventory_transactions"
    )





    def __repr__(self):

        return f"<InventoryTransaction {self.id}>"