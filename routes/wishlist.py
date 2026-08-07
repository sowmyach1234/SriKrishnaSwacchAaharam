from flask import (
    Blueprint,
    render_template,
    jsonify,
    redirect,
    url_for
)

from models import db
from models.wishlist import Wishlist



wishlist = Blueprint(
    "wishlist",
    __name__
)





# =====================================================
# ADD PRODUCT TO WISHLIST
# =====================================================


@wishlist.route(
    "/add-wishlist/<int:product_id>",
    methods=["POST"]
)
def add_wishlist(product_id):


    existing = Wishlist.query.filter_by(
        product_id=product_id
    ).first()



    if existing:


        return jsonify({

            "success": False,

            "message":
            "Already in wishlist",

            "wishlist_count":
            Wishlist.query.count()

        })





    item = Wishlist(

        product_id=product_id

    )



    db.session.add(item)

    db.session.commit()





    wishlist_count = Wishlist.query.count()



    return jsonify({

        "success": True,

        "message":
        "Product added to wishlist",

        "wishlist_count":
        wishlist_count

    })









# =====================================================
# VIEW WISHLIST PAGE
# =====================================================


@wishlist.route(
    "/wishlist"
)
def wishlist_page():



    items = Wishlist.query.order_by(
        Wishlist.id.desc()
    ).all()



    return render_template(

        "wishlist.html",

        wishlist_items=items,

        wishlist_count=len(items)

    )









# =====================================================
# REMOVE SINGLE WISHLIST PRODUCT (AJAX)
# =====================================================


@wishlist.route(
    "/remove-wishlist/<int:id>"
)
def remove_wishlist(id):



    item = Wishlist.query.get_or_404(
        id
    )



    db.session.delete(
        item
    )


    db.session.commit()





    return jsonify({

        "success": True,

        "message":
        "Removed from wishlist",

        "wishlist_count":
        Wishlist.query.count()

    })









# =====================================================
# CLEAR COMPLETE WISHLIST (AJAX)
# =====================================================


@wishlist.route(
    "/clear-wishlist"
)
def clear_wishlist():



    Wishlist.query.delete()



    db.session.commit()




    return jsonify({

        "success": True,

        "message":
        "Wishlist cleared",

        "wishlist_count":
        0

    })