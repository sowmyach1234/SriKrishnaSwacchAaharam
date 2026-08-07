from models import db


class Cart(db.Model):

    __tablename__ = "cart"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )


    quantity = db.Column(
        db.Integer,
        default=1
    )


    weight = db.Column(
        db.String(20),
        default="500g"
    )


    product = db.relationship(
        "Product",
        backref="cart_items"
    )



    # =====================================
    # WEIGHT MULTIPLIER
    # =====================================

    @property
    def weight_multiplier(self):

        if self.weight == "1kg":

            return 2


        elif self.weight == "2kg":

            return 4


        return 1




    # =====================================
    # ITEM SUBTOTAL
    # =====================================

    @property
    def subtotal(self):

        if self.product:

            return (
                self.product.price
                *
                self.weight_multiplier
                *
                self.quantity
            )


        return 0