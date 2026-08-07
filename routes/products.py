from flask import Blueprint, render_template, request, abort

from models import db
from models.product import Product


products = Blueprint("products", __name__)


# ==========================================
# PRODUCTS PAGE
# ==========================================

@products.route("/products")
def product_list():

    category = request.args.get("category")
    search = request.args.get("search")

    query = Product.query

    if category:
        query = query.filter(Product.category == category)

    if search:

        query = query.filter(
        db.or_(
            Product.product_name.ilike(f"%{search}%"),
            Product.category.ilike(f"%{search}%"),
            Product.description.ilike(f"%{search}%")
        )
    )

    all_products = query.all()

    return render_template(
        "products.html",
        products=all_products
    )


# ==========================================
# PRODUCT DETAILS PAGE
# ==========================================

@products.route("/product/<int:product_id>")
def product_details(product_id):

    product = Product.query.get(product_id)

    if product is None:
        abort(404)

    related_products = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id
    ).limit(4).all()

    return render_template(
        "product_details.html",
        product=product,
        related_products=related_products
    )