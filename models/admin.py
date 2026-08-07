from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    session,
    flash
)

from datetime import datetime

from sqlalchemy import func, extract

from models import (
    db,
    Product,
    Order,
    Customer,
    OrderItem
)


admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)



# ==================================================
# ADMIN LOGIN
# ==================================================

@admin.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        password = request.form.get(
            "password"
        )


        if (
            username == "admin"
            and password == "admin123"
        ):

            session["admin_logged_in"] = True


            return redirect(
                url_for(
                    "admin.dashboard"
                )
            )


        flash(
            "Invalid username or password",
            "error"
        )


    return render_template(
        "admin/login.html"
    )





# ==================================================
# DASHBOARD
# ==================================================

@admin.route("/dashboard")
def dashboard():


    if not session.get(
        "admin_logged_in"
    ):

        return redirect(
            url_for(
                "admin.login"
            )
        )



    # ==================================================
    # KPI ANALYTICS
    # ==================================================

    total_products = Product.query.count()


    total_orders = Order.query.count()


    total_customers = Customer.query.count()



    total_revenue = db.session.query(
        func.sum(
            Order.total_amount
        )
    ).scalar()


    total_revenue = (
        total_revenue
        if total_revenue
        else 0
    )



    average_order_value = (

        total_revenue / total_orders

        if total_orders > 0

        else 0

    )



    pending_orders = Order.query.filter(
        Order.status == "Pending"
    ).count()





    # ==================================================
    # INVENTORY
    # ==================================================

    total_stock = db.session.query(
        func.sum(
            Product.stock
        )
    ).scalar()



    total_stock = (
        total_stock
        if total_stock
        else 0
    )



    low_stock_products = Product.query.filter(
        Product.stock <= Product.minimum_stock
    ).all()



    recent_products = Product.query.order_by(
        Product.created_at.desc()
    ).limit(5).all()





    # ==================================================
    # BEST SELLER
    # ==================================================

    best_seller_data = db.session.query(

        OrderItem.product_name,

        func.sum(
            OrderItem.quantity
        )

    ).group_by(

        OrderItem.product_name

    ).order_by(

        func.sum(
            OrderItem.quantity
        ).desc()

    ).first()



    best_seller = (

        best_seller_data[0]

        if best_seller_data

        else "No Sales Yet"

    )





    # ==================================================
    # MONTHLY REVENUE CHART
    # ==================================================

    monthly_sales = db.session.query(

        func.strftime(
            "%m",
            Order.created_at
        ),

        func.sum(
            Order.total_amount
        )

    ).group_by(

        func.strftime(
            "%m",
            Order.created_at
        )

    ).all()



    sales_labels = []

    sales_values = []



    for month, revenue in monthly_sales:


        if month:


            sales_labels.append(

                datetime(
                    2026,
                    int(month),
                    1
                ).strftime("%b")

            )


            sales_values.append(

                float(
                    revenue or 0
                )

            )



    if not sales_labels:

        sales_labels = [
            "Jan",
            "Feb",
            "Mar",
            "Apr"
        ]


        sales_values = [
            0,
            0,
            0,
            0
        ]





    # ==================================================
    # CATEGORY SALES CHART
    # ==================================================

    category_sales = (

        db.session.query(

            Product.category,

            func.sum(

                OrderItem.quantity *
                OrderItem.price

            )

        )

        .join(

            OrderItem,

            Product.id ==
            OrderItem.product_id

        )

        .group_by(

            Product.category

        )

        .all()

    )



    category_labels = []

    category_values = []



    for category, amount in category_sales:


        category_labels.append(
            category
        )


        category_values.append(
            float(amount or 0)
        )



    if not category_labels:

        category_labels = [
            "No Data"
        ]


        category_values = [
            0
        ]





    # ==================================================
    # INVENTORY HEALTH CHART
    # ==================================================

    healthy_stock = Product.query.filter(

        Product.stock >
        Product.minimum_stock

    ).count()



    low_stock = Product.query.filter(

        Product.stock <=
        Product.minimum_stock,

        Product.stock > 0

    ).count()



    out_of_stock = Product.query.filter(

        Product.stock == 0

    ).count()



    inventory_labels = [

        "Healthy Stock",

        "Low Stock",

        "Out Of Stock"

    ]


    inventory_values = [

        healthy_stock,

        low_stock,

        out_of_stock

    ]

        # ==================================================
    # TOP SELLING PRODUCTS CHART
    # ==================================================

    top_products = (

        db.session.query(

            OrderItem.product_name,

            func.sum(
                OrderItem.quantity
            )

        )

        .group_by(

            OrderItem.product_name

        )

        .order_by(

            func.sum(
                OrderItem.quantity
            ).desc()

        )

        .limit(5)

        .all()

    )



    top_product_names = []

    top_product_sales = []



    for name, quantity in top_products:


        top_product_names.append(
            name
        )


        top_product_sales.append(
            int(quantity or 0)
        )



    if not top_product_names:


        top_product_names = [
            "No Sales"
        ]


        top_product_sales = [
            0
        ]





    # ==================================================
    # CUSTOMER SEGMENT ANALYTICS
    # ==================================================

    premium_customers = Customer.query.filter(

        Customer.segment.in_(
            [
                "Premium",
                "Premium Customer"
            ]
        )

    ).count()



    regular_customers = Customer.query.filter(

        Customer.segment.in_(
            [
                "Regular",
                "Regular Customer"
            ]
        )

    ).count()



    new_customers = Customer.query.filter(

        Customer.segment ==
        "New Customer"

    ).count()



    customer_labels = [

        "Premium",

        "Regular",

        "New"

    ]


    customer_values = [

        premium_customers,

        regular_customers,

        new_customers

    ]





    # ==================================================
    # CATEGORY COUNT
    # ==================================================

    total_categories = db.session.query(

        Product.category

    ).distinct().count()





    # ==================================================
    # ADVANCED BUSINESS INTELLIGENCE
    # ==================================================

    current_month = datetime.now().month


    previous_month = current_month - 1


    if previous_month == 0:

        previous_month = 12





    current_month_revenue = db.session.query(

        func.sum(
            Order.total_amount
        )

    ).filter(

        extract(
            "month",
            Order.created_at
        )
        ==
        current_month

    ).scalar()



    current_month_revenue = (

        current_month_revenue

        if current_month_revenue

        else 0

    )





    previous_month_revenue = db.session.query(

        func.sum(
            Order.total_amount
        )

    ).filter(

        extract(
            "month",
            Order.created_at
        )
        ==
        previous_month

    ).scalar()



    previous_month_revenue = (

        previous_month_revenue

        if previous_month_revenue

        else 0

    )





    if previous_month_revenue > 0:


        revenue_growth = (

            (

                current_month_revenue

                -

                previous_month_revenue

            )

            /

            previous_month_revenue

        ) * 100


    else:

        revenue_growth = 0






    # ==================================================
    # INVENTORY VALUE
    # ==================================================

    average_product_price = db.session.query(

        func.avg(
            OrderItem.price
        )

    ).scalar()



    average_product_price = (

        average_product_price

        if average_product_price

        else 0

    )



    inventory_value = (

        total_stock *

        average_product_price

    )





    # ==================================================
    # BUSINESS HEALTH SCORE
    # ==================================================

    business_health_score = 0



    if total_revenue > 0:

        business_health_score += 30



    if total_orders > 0:

        business_health_score += 25



    if total_customers > 0:

        business_health_score += 20



    if healthy_stock > low_stock:

        business_health_score += 25






    # ==================================================
    # DEBUG CHECK
    # ==================================================

    print(
        "========== DASHBOARD DATA =========="
    )


    print(
        "Sales:",
        sales_labels,
        sales_values
    )


    print(
        "Category:",
        category_labels,
        category_values
    )


    print(
        "Inventory:",
        inventory_labels,
        inventory_values
    )


    print(
        "Top Products:",
        top_product_names,
        top_product_sales
    )


    print(
        "===================================="
    )






    # ==================================================
    # SEND DATA TO TEMPLATE
    # ==================================================

    return render_template(

        "admin/dashboard.html",


        # KPI

        total_products=
        total_products,


        total_orders=
        total_orders,


        total_customers=
        total_customers,


        total_revenue=
        round(
            total_revenue,
            2
        ),


        average_order_value=
        round(
            average_order_value,
            2
        ),


        pending_orders=
        pending_orders,


        total_stock=
        total_stock,



        # Products

        low_stock_products=
        low_stock_products,


        recent_products=
        recent_products,



        # Insights

        best_seller=
        best_seller,


        total_categories=
        total_categories,



        # Charts

        sales_labels=
        sales_labels,


        sales_values=
        sales_values,


        category_labels=
        category_labels,


        category_values=
        category_values,


        inventory_labels=
        inventory_labels,


        inventory_values=
        inventory_values,


        top_product_names=
        top_product_names,


        top_product_sales=
        top_product_sales,



        # Customer analytics

        customer_labels=
        customer_labels,


        customer_values=
        customer_values,


        premium_customers=
        premium_customers,


        regular_customers=
        regular_customers,


        new_customers=
        new_customers,



        # BI

        revenue_growth=
        round(
            revenue_growth,
            2
        ),


        current_month_revenue=
        round(
            current_month_revenue,
            2
        ),


        previous_month_revenue=
        round(
            previous_month_revenue,
            2
        ),


        inventory_value=
        round(
            inventory_value,
            2
        ),


        business_health_score=
        business_health_score

    )






# ==================================================
# ADMIN LOGOUT
# ==================================================

@admin.route("/logout")
def logout():


    session.clear()


    flash(
        "Logged out successfully",
        "success"
    )


    return redirect(

        url_for(
            "admin.login"
        )

    )