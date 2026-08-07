from flask import Blueprint, render_template

import calendar


from analytics.analytics_service import (

    get_total_orders,
    get_total_revenue,
    get_total_customers,
    get_total_products,
    get_best_products,
    get_category_sales,
    get_customer_orders,
    get_sales_trend

)



analytics = Blueprint(

    "analytics",
    __name__,
    url_prefix="/admin/analytics"

)





# ==================================================
# ANALYTICS DASHBOARD
# ==================================================

@analytics.route("/")
def analytics_dashboard():



    # ===============================
    # KPI DATA
    # ===============================

    total_orders = get_total_orders()

    total_revenue = get_total_revenue()

    total_customers = get_total_customers()

    total_products = get_total_products()



    # ===============================
    # PRODUCT ANALYTICS
    # ===============================

    best_products = get_best_products()


    if not best_products:

        best_products = []




    # ===============================
    # CATEGORY ANALYTICS
    # ===============================

    category_sales = get_category_sales()


    category_labels = []

    category_values = []



    for item in category_sales:


        category_labels.append(

            item[0]

        )


        category_values.append(

            float(

                item[1] or 0

            )

        )



    if not category_labels:


        category_labels = [

            "No Sales"

        ]


        category_values = [

            0

        ]





    # ===============================
    # CUSTOMER ANALYTICS
    # ===============================

    customer_orders = get_customer_orders()


    if not customer_orders:

        customer_orders = []





    # ===============================
    # REVENUE TREND
    # ===============================

    sales_trend = get_sales_trend()


    sales_labels = []

    sales_values = []



    for sale in sales_trend:


        sales_labels.append(

            sale.created_at.strftime(
                "%b %d"
            )

        )


        sales_values.append(

            float(
                sale.total_amount or 0
            )

        )



    if not sales_labels:


        sales_labels = [

            "No Data"

        ]


        sales_values = [

            0

        ]





    # ===============================
    # RENDER
    # ===============================


    return render_template(

        "admin/analytics.html",


        total_orders=total_orders,


        total_revenue=total_revenue,


        total_customers=total_customers,


        total_products=total_products,


        best_products=best_products,


        customer_orders=customer_orders,


        sales_labels=sales_labels,


        sales_values=sales_values,


        category_labels=category_labels,


        category_values=category_values

    )