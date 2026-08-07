from flask import Blueprint, render_template

from models.product import Product



home = Blueprint(
    "home",
    __name__
)





# =====================================================
# HOME PAGE
# =====================================================


@home.route("/")
def index():


    # ==============================================
    # BEST SELLER PRODUCTS
    # ==============================================

    best_sellers = Product.query.filter(
        Product.stock > 0
    ).order_by(
        Product.created_at.desc()
    ).limit(4).all()



    return render_template(

        "home/index.html",

        best_sellers=best_sellers

    )