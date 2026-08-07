from flask import (
    Blueprint,
    render_template,
    request
)

from sqlalchemy import func

from models import db

from models.product import Product




admin_inventory = Blueprint(

    "admin_inventory",

    __name__,

    url_prefix="/admin/inventory"

)






# ===================================
# INVENTORY DASHBOARD
# ===================================


@admin_inventory.route("/")
def inventory_dashboard():


    search = request.args.get(
        "search",
        ""
    )


    filter_type = request.args.get(
        "filter",
        ""
    )



    query = Product.query




    if search:


        query = query.filter(

            Product.product_name.ilike(
                f"%{search}%"
            )

        )





    if filter_type == "low":


        query = query.filter(

            Product.stock <= 10

        )






    products = query.order_by(

        Product.stock.asc()

    ).all()





    total_products = Product.query.count()



    total_stock = sum(

        product.stock or 0

        for product in Product.query.all()

    )





    low_stock = Product.query.filter(

        Product.stock <= 10

    ).count()





    out_of_stock = Product.query.filter(

        Product.stock == 0

    ).count()






    return render_template(

        "admin/inventory.html",


        products=products,


        total_products=total_products,


        total_stock=total_stock,


        low_stock=low_stock,


        out_of_stock=out_of_stock,


        search=search,


        filter_type=filter_type

    )









# ===================================
# INVENTORY ANALYTICS DASHBOARD
# ===================================


@admin_inventory.route("/analytics")
def inventory_analytics():



    products = Product.query.all()





    # -------------------------------
    # BASIC KPI
    # -------------------------------


    total_products = len(products)



    total_stock = sum(

        p.stock or 0

        for p in products

    )






    inventory_value = sum(

        (p.stock or 0) *
        (p.price or 0)

        for p in products

    )






    # -------------------------------
    # STOCK STATUS CHART
    # -------------------------------


    available = Product.query.filter(

        Product.stock > 10

    ).count()




    low_stock = Product.query.filter(

        Product.stock <= 10,

        Product.stock > 0

    ).count()




    out_stock = Product.query.filter(

        Product.stock == 0

    ).count()





    stock_status = {


        "available":
            available,


        "low_stock":
            low_stock,


        "out_stock":
            out_stock


    }





    # -------------------------------
    # CATEGORY STOCK CHART
    # -------------------------------


    category_data = db.session.query(

        Product.category,

        func.sum(Product.stock)

    ).group_by(

        Product.category

    ).all()





    categories = []


    category_stock = []




    for category, stock in category_data:


        categories.append(
            category
        )


        category_stock.append(
            int(stock or 0)
        )







    # -------------------------------
    # HIGH VALUE PRODUCTS
    # -------------------------------


    valuable_products = sorted(

        products,

        key=lambda x:

        (x.stock or 0) *
        (x.price or 0),

        reverse=True

    )[:10]







    # -------------------------------
    # REORDER PRODUCTS
    # -------------------------------


    reorder_products = Product.query.filter(

        Product.stock <= 10

    ).all()







    return render_template(

        "admin/inventory_analytics.html",



        total_products=
        total_products,



        total_stock=
        total_stock,



        inventory_value=
        inventory_value,



        stock_status=
        stock_status,



        categories=
        categories,



        category_stock=
        category_stock,



        valuable_products=
        valuable_products,



        reorder_products=
        reorder_products,



        low_stock_products=
        len(reorder_products)

    )