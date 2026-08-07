from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    jsonify,
    request
)

from models import db
from models.cart import Cart
from models.product import Product



cart = Blueprint(
    "cart",
    __name__
)





# ==========================================================
# ADD PRODUCT TO CART
# ==========================================================


@cart.route(
    "/add-to-cart/<int:product_id>",
    methods=["POST"]
)
def add_to_cart(product_id):


    product = Product.query.get_or_404(
        product_id
    )


    data = request.get_json(
        silent=True
    ) or {}



    quantity = int(
        data.get(
            "quantity",
            1
        )
    )



    if quantity < 1:

        quantity = 1




    # STOCK CHECK

    existing_quantity = 0


    existing_item = Cart.query.filter_by(
        product_id=product.id
    ).first()



    if existing_item:

        existing_quantity = existing_item.quantity




    if existing_quantity + quantity > product.stock:


        return jsonify({

            "success":False,

            "message":
            "Product is not available currently."

        })







    if existing_item:


        existing_item.quantity += quantity



    else:


        cart_item = Cart(

            product_id=product.id,

            quantity=quantity,

            weight="500g"

        )


        db.session.add(
            cart_item
        )





    db.session.commit()





    cart_count = db.session.query(
        db.func.sum(Cart.quantity)
    ).scalar() or 0




    cart_total = sum(

        item.subtotal

        for item in Cart.query.all()

    )




    return jsonify({


        "success":True,


        "message":
        "Product added to cart",


        "cart_count":
        cart_count,


        "cart_total":
        cart_total


    })









# ==========================================================
# VIEW CART
# ==========================================================


@cart.route("/cart")
def view_cart():


    cart_items = Cart.query.order_by(
        Cart.id.desc()
    ).all()



    total_items = sum(

        item.quantity

        for item in cart_items

    )



    grand_total = sum(

        item.subtotal

        for item in cart_items

    )



    return render_template(

        "cart.html",

        cart_items=cart_items,

        total_items=total_items,

        grand_total=grand_total

    )









# ==========================================================
# AJAX QUANTITY UPDATE
# ==========================================================


@cart.route(
    "/update-cart-quantity/<int:id>",
    methods=["POST"]
)
def update_cart_quantity(id):


    item = Cart.query.get_or_404(
        id
    )



    data = request.get_json(
        silent=True
    ) or {}



    quantity = int(
        data.get(
            "quantity",
            1
        )
    )



    if quantity < 1:

        quantity = 1






    product = item.product




    # STOCK VALIDATION


    if quantity > product.stock:


        return jsonify({

            "success":False,

            "message":
            "Only limited stock available."

        })






    item.quantity = quantity



    db.session.commit()





    subtotal = item.subtotal



    total_items = sum(

        cart.quantity

        for cart in Cart.query.all()

    )



    grand_total = sum(

        cart.subtotal

        for cart in Cart.query.all()

    )





    return jsonify({

        "success":True,

        "subtotal":
        subtotal,


        "total_items":
        total_items,


        "grand_total":
        grand_total

    })









# ==========================================================
# INCREASE QUANTITY
# ==========================================================


@cart.route(
    "/increase-cart/<int:id>"
)
def increase_cart(id):


    item = Cart.query.get_or_404(
        id
    )


    item.quantity += 1


    db.session.commit()



    return redirect(
        url_for(
            "cart.view_cart"
        )
    )










# ==========================================================
# DECREASE QUANTITY
# ==========================================================


@cart.route(
    "/decrease-cart/<int:id>"
)
def decrease_cart(id):


    item = Cart.query.get_or_404(
        id
    )


    if item.quantity > 1:


        item.quantity -= 1


    else:


        db.session.delete(
            item
        )



    db.session.commit()



    return redirect(
        url_for(
            "cart.view_cart"
        )
    )









# ==========================================================
# REMOVE ITEM
# ==========================================================


@cart.route(
    "/remove-cart/<int:id>"
)
def remove_cart(id):


    item = Cart.query.get_or_404(
        id
    )



    db.session.delete(
        item
    )


    db.session.commit()



    return redirect(
        url_for(
            "cart.view_cart"
        )
    )









# ==========================================================
# CLEAR CART
# ==========================================================


@cart.route(
    "/clear-cart"
)
def clear_cart():


    Cart.query.delete()


    db.session.commit()



    return redirect(
        url_for(
            "cart.view_cart"
        )
    )









# ==========================================================
# CART SUMMARY API
# ==========================================================


@cart.route(
    "/cart-summary"
)
def cart_summary():


    cart_items = Cart.query.all()



    total_items = sum(

        item.quantity

        for item in cart_items

    )



    grand_total = sum(

        item.subtotal

        for item in cart_items

    )



    return jsonify({


        "items":
        total_items,


        "total":
        grand_total


    })