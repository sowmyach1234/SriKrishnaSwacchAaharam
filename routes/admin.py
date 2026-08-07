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

import calendar

from sqlalchemy import func, extract

from models import (
    db,
    Product,
    Order,
    Customer,
    OrderItem,
    AdminActivity
)
from utils.ai_insights import generate_business_insights
from utils.predictive_ai import predict_business


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

        username = request.form.get("username")

        password = request.form.get("password")


        saved_password = session.get(
            "admin_password",
            "admin123"
        )

        if (
            username == "admin"
            and password == saved_password
        ):

            session["admin_logged_in"] = True
            activity = AdminActivity(

            action="Admin Login",

            description="Administrator logged into dashboard",

            status="Success"

            )


            db.session.add(activity)

            db.session.commit()

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
# BUSINESS INTELLIGENCE DASHBOARD
# ==================================================

@admin.route("/dashboard")
def dashboard():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for(
                "admin.login"
            )
        )



    # ==================================================
    # BASIC KPI
    # ==================================================

    total_products = db.session.query(
        Product.id
    ).count()


    total_orders = db.session.query(
        Order.id
    ).count()


    total_customers = db.session.query(
        Customer.id
    ).count()



    total_revenue = db.session.query(
        func.coalesce(
            func.sum(
                Order.total_amount
            ),
            0
        )
    ).scalar()

    average_order_value = (

    total_revenue / total_orders

    if total_orders > 0

    else 0

    )


    # ==================================================
    # ORDER STATUS
    # ==================================================

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



    if total_stock is None:

        total_stock = 0



    low_stock_products = Product.query.filter(
        Product.stock <= Product.minimum_stock
    ).all()



    healthy_stock = Product.query.filter(
        Product.stock > Product.minimum_stock
    ).count()



    low_stock = Product.query.filter(
        Product.stock <= Product.minimum_stock,
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



    if best_seller_data:

        best_seller = best_seller_data[0]

    else:

        best_seller = "No Sales Yet"





    # ==================================================
    # REVENUE TREND CHART (DYNAMIC 12 MONTH)
    # ==================================================

    current_year = datetime.now().year


    monthly_sales = db.session.query(

        func.strftime(
            "%m",
            Order.created_at
        ),

        func.sum(
            Order.total_amount
        )

    ).filter(

        func.strftime(
            "%Y",
            Order.created_at
        ) == str(current_year)

    ).group_by(

        func.strftime(
            "%m",
            Order.created_at
        )

    ).all()



    sales_dict = {

        int(month): float(revenue or 0)

        for month, revenue in monthly_sales

    }



    sales_labels = []

    sales_values = []



    for month in range(1,13):


        sales_labels.append(

            calendar.month_abbr[month]

        )


        sales_values.append(

            sales_dict.get(
                month,
                0
            )

        )




    # ==================================================
    # CATEGORY SALES CHART (FIXED)
    # ==================================================

    category_sales = db.session.query(

        Product.category,

        func.sum(

            OrderItem.quantity *
            OrderItem.price

        )

    ).join(

        OrderItem,

        Product.id == OrderItem.product_id

    ).group_by(

        Product.category

    ).all()



    category_labels = []

    category_values = []


    for category, amount in category_sales:

        if category:

            category_labels.append(
                category
            )

            category_values.append(
                round(
                    float(amount or 0),
                    2
                )
            )



    # Sort highest revenue first

    category_data = sorted(

        zip(
            category_labels,
            category_values
        ),

        key=lambda x:x[1],

        reverse=True

    )



    category_labels = [

        item[0]

        for item in category_data

    ]


    category_values = [

        item[1]

        for item in category_data

    ]


    category_percentage = []


    total_category_sales = sum(
        category_values
    )



    for value in category_values:

        if total_category_sales > 0:

            percentage = (

                value /
                total_category_sales

            ) * 100


        else:

            percentage = 0



        category_percentage.append(

            round(
                percentage,
                1
            )

        )





    # fallback for old orders without product_id

    if not category_labels:


        old_sales = db.session.query(

            OrderItem.product_name,

            func.sum(

                OrderItem.quantity *
                OrderItem.price

            )

        ).group_by(

            OrderItem.product_name

        ).all()



        for name, amount in old_sales:


            category_labels.append(
                name
            )


            category_values.append(

                float(
                    amount or 0
                )

            )



    if not category_labels:


        category_labels = [

            "No Sales"

        ]


        category_values = [

            0

        ]




# ==================================================
# TOP SELLING PRODUCTS BY REVENUE
# ==================================================

    top_products = db.session.query(

        OrderItem.product_name,

        func.sum(
            OrderItem.quantity *
            OrderItem.price
        )

    ).group_by(

        OrderItem.product_name

    ).order_by(

        func.sum(
            OrderItem.quantity *
            OrderItem.price
        ).desc()

    ).limit(5).all()



    top_product_names = []

    top_product_sales = []



    for name, revenue in top_products:

        top_product_names.append(
            name
        )


        top_product_sales.append(

            float(
                revenue or 0
            )

        )



    if not top_product_names:

        top_product_names = [

            "No Sales"

        ]


        top_product_sales = [

            0

        ]

    # ==================================================
    # CUSTOMER SEGMENTS
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

        Customer.segment == "New Customer"

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
    # ADVANCED BI
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
        ) == current_month

    ).scalar()



    previous_month_revenue = db.session.query(

        func.sum(
            Order.total_amount
        )

    ).filter(

        extract(
            "month",
            Order.created_at
        ) == previous_month

    ).scalar()



    current_month_revenue = current_month_revenue or 0

    previous_month_revenue = previous_month_revenue or 0




    if previous_month_revenue > 0:


        revenue_growth = (

            (
                current_month_revenue -
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



    average_product_price = average_product_price or 0



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
    # AI INSIGHTS
    # ==================================================

    business_insights = generate_business_insights(

        total_revenue,

        total_orders,

        total_customers,

        low_stock,

        out_of_stock,

        business_health_score,

        best_seller

    )



    predictions = predict_business(

        total_revenue=total_revenue,

        total_orders=total_orders,

        total_customers=total_customers,

        total_stock=total_stock,

        low_stock=low_stock,

        best_seller=best_seller

    )





    return render_template(

        "admin/dashboard.html",


        total_products=total_products,

        total_orders=total_orders,

        total_customers=total_customers,

        total_revenue=round(
            total_revenue,
            2
        ),


        average_order_value=round(
            average_order_value,
            2
        ),


        pending_orders=pending_orders,


        total_stock=total_stock,


        low_stock_products=low_stock_products,


        recent_products=recent_products,


        best_seller=best_seller,


        total_categories=total_categories,


        sales_labels=sales_labels,

        sales_values=sales_values,


        category_labels=category_labels,

        category_values=category_values,

        category_percentage=category_percentage,


        inventory_labels=inventory_labels,

        inventory_values=inventory_values,


        top_product_names=top_product_names,

        top_product_sales=top_product_sales,


        customer_labels=customer_labels,

        customer_values=customer_values,


        premium_customers=premium_customers,

        regular_customers=regular_customers,

        new_customers=new_customers,


        business_insights=business_insights,

        predictions=predictions,


        revenue_growth=round(
            revenue_growth,
            2
        ),


        current_month_revenue=round(
            current_month_revenue,
            2
        ),


        previous_month_revenue=round(
            previous_month_revenue,
            2
        ),


        inventory_value=round(
            inventory_value,
            2
        ),


        business_health_score=business_health_score

    )


    # ==================================================
    # ANALYTICS PAGE
    # ==================================================

@admin.route("/analytics")
def analytics():

    if not session.get("admin_logged_in"):

            return redirect(
                url_for("admin.login")
            )


    total_products = Product.query.count()

    total_orders = Order.query.count()

    total_customers = Customer.query.count()


    total_revenue = db.session.query(
            func.sum(Order.total_amount)
        ).scalar() or 0



                # ==========================
        # REVENUE TREND
        # ==========================


    current_year = datetime.now().year


    monthly_sales = db.session.query(

            func.strftime(
                "%m",
                Order.created_at
            ),

            func.sum(
                Order.total_amount
            )

        ).filter(

            func.strftime(
                "%Y",
                Order.created_at
            ) == str(current_year)

        ).group_by(

            func.strftime(
                "%m",
                Order.created_at
            )

        ).all()



    sales_dict = {

            int(month): float(revenue or 0)

            for month, revenue in monthly_sales

        }



    sales_labels = []

    sales_values = []



    for month in range(1,13):


            sales_labels.append(

                calendar.month_abbr[month]

            )


            sales_values.append(

                sales_dict.get(
                    month,
                    0
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





        # ==========================
        # CATEGORY PERFORMANCE FIX
        # ==========================


    category_labels = []

    category_values = []



        # First try using product_id

    category_sales = db.session.query(

            Product.category,

            func.sum(
                OrderItem.quantity *
                OrderItem.price
            )

        ).join(

            OrderItem,

            Product.id == OrderItem.product_id

        ).group_by(

            Product.category

        ).all()



    for category, amount in category_sales:

            if category:

                category_labels.append(
                    category
                )

                category_values.append(
                    float(amount or 0)
                )





        # Backup for existing old orders

        # where product_id is empty

    if not category_labels:


            old_sales = db.session.query(

                OrderItem.product_name,

                func.sum(
                    OrderItem.quantity *
                    OrderItem.price
                )

            ).group_by(

                OrderItem.product_name

            ).all()



            for name, amount in old_sales:


                category_labels.append(
                    name
                )


                category_values.append(

                    float(
                        amount or 0
                    )

                )




    if not category_labels:


            category_labels = [
                "No Sales"
            ]

            category_values = [
                1
            ]





    print(
            "ANALYTICS CATEGORY:",
            category_labels,
            category_values
        )



    return render_template(

        "admin/analytics.html",

        total_products=total_products,

        total_orders=total_orders,

        total_customers=total_customers,


        total_revenue=round(
            total_revenue,
            2
        ),


        sales_labels=sales_labels,

        sales_values=sales_values,


        category_labels=category_labels,

        category_values=category_values

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