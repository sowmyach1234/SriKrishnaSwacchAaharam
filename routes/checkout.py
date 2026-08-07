from flask import Blueprint, render_template, request, redirect, url_for, flash

from models import db

from models.order import Order
from models.customer import Customer
from models.cart import Cart
from models.order_item import OrderItem



checkout = Blueprint(
    "checkout",
    __name__
)



# ==========================================
# CHECKOUT PAGE
# ==========================================

@checkout.route(
    "/checkout",
    methods=["GET", "POST"]
)
def checkout_page():


    cart_items = Cart.query.all()



    # Calculate total

    total_amount = sum(
        item.product.price * item.quantity
        for item in cart_items
        if item.product
    )



    if request.method == "POST":


        if not cart_items:

            flash(
                "Your cart is empty",
                "warning"
            )

            return redirect(
                url_for("cart.view_cart")
            )



        # SAFE FORM READING

        name = request.form.get(
            "name"
        )

        phone = request.form.get(
            "phone"
        )

        email = request.form.get(
            "email",
            ""
        )

        address = request.form.get(
            "address"
        )



        # ==============================
        # CUSTOMER
        # ==============================


        customer = Customer.query.filter_by(
            phone=phone
        ).first()



        if customer:


            customer.total_orders += 1

            customer.total_spent += total_amount

            customer.email = email

            customer.address = address



        else:


            customer = Customer(

                name=name,

                phone=phone,

                email=email,

                address=address,

                total_orders=1,

                total_spent=total_amount

            )


            db.session.add(customer)

            db.session.flush()



        # ==============================
        # CREATE ORDER
        # ==============================


        order = Order(

            customer_id=customer.id,

            customer_name=name,

            customer_phone=phone,

            customer_address=address,

            total_amount=total_amount,

            status="Pending"

        )


        db.session.add(order)

        db.session.flush()



        # ==============================
        # ORDER ITEMS
        # ==============================


        for item in cart_items:


            if item.product:


                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product.id,
                    product_name=item.product.product_name,
                    quantity=item.quantity,
                    price=item.product.price
                )


                db.session.add(order_item)



        # ==============================
        # CLEAR CART
        # ==============================


        for item in cart_items:

            db.session.delete(item)



        db.session.commit()



        return redirect(

            url_for(

                "checkout.order_success",

                order_id=order.id

            )

        )





    return render_template(

        "checkout.html",

        cart_items=cart_items,

        total_amount=total_amount

    )





# ==========================================
# ORDER SUCCESS
# ==========================================

@checkout.route(
    "/order-success/<int:order_id>"
)
def order_success(order_id):


    order = Order.query.get_or_404(
        order_id
    )


    return render_template(

        "order_success.html",

        order=order

    )