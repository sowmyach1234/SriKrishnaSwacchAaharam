from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from models import db
from models.product import Product

import os

from werkzeug.utils import secure_filename

from flask import current_app



UPLOAD_FOLDER = "static/images/products"



admin_products = Blueprint(
    "admin_products",
    __name__,
    url_prefix="/admin/products"
)



# ============================
# PRODUCT LIST
# ============================

@admin_products.route("/")
def product_list():

    search = request.args.get(
        "search"
    )


    category = request.args.get(
        "category"
    )



    query = Product.query



    if search:

        query = query.filter(
            Product.product_name.ilike(
                f"%{search}%"
            )
        )


    if category:

        query = query.filter(
            Product.category == category
        )


    products = query.all()



    categories = db.session.query(
        Product.category
    ).distinct().all()



    return render_template(
        "admin/products.html",
        products=products,
        categories=categories
    )

    search = request.args.get(
        "search"
    )


    category = request.args.get(
        "category"
    )



    query = Product.query



    if search:

        query = query.filter(
            Product.product_name.ilike(
                f"%{search}%"
            )
        )


    if category:

        query = query.filter(
            Product.category == category
        )


    products = query.all()



    categories = db.session.query(
        Product.category
    ).distinct().all()



    return render_template(
        "admin/products.html",
        products=products,
        categories=categories
    )

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin.login")
        )


    products = Product.query.order_by(
        Product.created_at.desc()
    ).all()


    return render_template(
        "admin/products.html",
        products=products
    )





# ============================
# ADD PRODUCT
# ============================

@admin_products.route("/add", methods=["GET","POST"])
def add_product():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("admin.login")
        )



    if request.method == "POST":


        image_file = request.files["image"]


        filename = None


        if image_file.filename:


            filename = secure_filename(
                image_file.filename
            )


            image_path = os.path.join(
                UPLOAD_FOLDER,
                filename
            )


            image_file.save(
                image_path
            )




        product = Product(

            product_name=request.form["product_name"],

            category=request.form["category"],

            description=request.form["description"],

            price=float(
                request.form["price"]
            ),

            stock=int(
                request.form["stock"]
            ),

            image=filename,

            organic=True
        )


        db.session.add(product)

        db.session.commit()



        return redirect(
            url_for(
                "admin_products.product_list"
            )
        )



    return render_template(
        "admin/add_product.html"
    )

@admin_products.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    product = Product.query.get_or_404(product_id)

    if request.method == "POST":

        product.product_name = request.form["product_name"]
        product.category = request.form["category"]
        product.description = request.form["description"]
        product.price = float(request.form["price"])
        product.stock = int(request.form["stock"])

        image = request.files.get("image")

        if image and image.filename:

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    filename
                )
            )

            product.image = filename

        db.session.commit()

        return redirect(
            url_for("admin_products.product_list")
        )

    return render_template(
        "admin/edit_product.html",
        product=product
    )

@admin_products.route("/delete/<int:product_id>", methods=["GET", "POST"])
def delete_product(product_id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    product = Product.query.get_or_404(product_id)

    if request.method == "POST":

        # Delete image if it exists
        if product.image:

            image_path = os.path.join(
                UPLOAD_FOLDER,
                product.image
            )

            if os.path.exists(image_path):
                os.remove(image_path)

        db.session.delete(product)

        db.session.commit()

        flash(
            "Product deleted successfully.",
            "success"
        )

        return redirect(
            url_for("admin_products.product_list")
        )

    return render_template(
        "admin/delete_product.html",
        product=product
    )