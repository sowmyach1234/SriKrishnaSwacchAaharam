from flask import Blueprint, render_template

from models.product import Product

from sqlalchemy import func



inventory_analytics = Blueprint(

    "inventory_analytics",

    __name__,

    url_prefix="/admin/inventory"

)





# ==========================================
# INVENTORY ANALYTICS DASHBOARD
# ==========================================


@inventory_analytics.route("/analytics")
def inventory_dashboard_analytics():



    products = Product.query.all()



    # --------------------------------------
    # BASIC METRICS
    # --------------------------------------


    total_products = len(products)



    total_stock = sum(

        product.stock

        for product in products

    )



    inventory_value = sum(

        product.stock * product.price

        for product in products

    )



    low_stock_products = Product.query.filter(

        Product.stock <= Product.minimum_stock

    ).count()



    out_of_stock_products = Product.query.filter(

        Product.stock == 0

    ).count()







    # --------------------------------------
    # STOCK STATUS CHART
    # --------------------------------------


    available = Product.query.filter(

        Product.stock > Product.minimum_stock

    ).count()



    low_stock = Product.query.filter(

        Product.stock <= Product.minimum_stock,

        Product.stock > 0

    ).count()



    out_stock = Product.query.filter(

        Product.stock == 0

    ).count()





    stock_status = {


        "available": available,

        "low_stock": low_stock,

        "out_stock": out_stock

    }








    # --------------------------------------
    # CATEGORY ANALYSIS
    # --------------------------------------


    category_data = (


        Product.query

        .with_entities(

            Product.category,

            func.sum(Product.stock)

        )

        .group_by(Product.category)

        .all()

    )




    categories = []

    category_stock = []



    for category, stock in category_data:


        categories.append(category)


        category_stock.append(stock)









    # --------------------------------------
    # TOP VALUE PRODUCTS
    # --------------------------------------


    valuable_products = sorted(

        products,

        key=lambda x:

        x.stock * x.price,

        reverse=True

    )[:5]







    # --------------------------------------
    # REORDER PRODUCTS
    # --------------------------------------


    reorder_products = Product.query.filter(

        Product.stock <= Product.minimum_stock

    ).order_by(

        Product.stock.asc()

    ).all()







    return render_template(

        "admin/inventory_analytics.html",


        total_products=total_products,


        total_stock=total_stock,


        inventory_value=inventory_value,


        low_stock_products=low_stock_products,


        out_of_stock_products=out_of_stock_products,



        stock_status=stock_status,


        categories=categories,


        category_stock=category_stock,


        valuable_products=valuable_products,


        reorder_products=reorder_products


    )