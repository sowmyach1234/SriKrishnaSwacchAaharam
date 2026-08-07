from flask import Blueprint, render_template

from models.customer import Customer
from models.order import Order
from models import db

from sqlalchemy import func

from services.ai_recommendation import generate_customer_recommendation

from services.customer_ai_profile import generate_customer_ai_profile



customers = Blueprint(
    "customers",
    __name__,
    url_prefix="/admin/customers"
)





# =====================================================
# CUSTOMER INTELLIGENCE CENTER
# STAGE 15.2.1.1
# CLV + RFM FOUNDATION
# =====================================================


@customers.route("/")
def customer_list():



    # =================================================
    # CUSTOMER LIST
    # =================================================


    customers_data = Customer.query.order_by(

        Customer.total_spent.desc()

    ).all()


    # ===============================================
# AI CUSTOMER RECOMMENDATION
# ===============================================


    ai_recommendations = []


    for customer in customers_data[:5]:

        recommendation = generate_customer_recommendation(
            customer
        )


        ai_recommendations.append(
            recommendation
        )





    # =================================================
    # BASIC KPI
    # =================================================


    total_customers = Customer.query.count()



    total_revenue = db.session.query(

        func.sum(
            Customer.total_spent
        )

    ).scalar()



    total_revenue = total_revenue or 0






    repeat_customers = Customer.query.filter(

        Customer.total_orders > 1

    ).count()





    average_spending = 0


    if total_customers > 0:

        average_spending = (

            total_revenue /
            total_customers

        )





    # =================================================
    # CUSTOMER LIFETIME VALUE (CLV)
    # =================================================


    customer_lifetime_value = average_spending






    # =================================================
    # PURCHASE FREQUENCY
    # =================================================


    purchase_frequency = 0


    if total_customers > 0:


        total_orders = db.session.query(

            func.sum(
                Customer.total_orders
            )

        ).scalar()



        total_orders = total_orders or 0



        purchase_frequency = (

            total_orders /
            total_customers

        )






    # =================================================
    # RETENTION ANALYTICS
    # =================================================


    retention_rate = 0



    if total_customers > 0:


        retention_rate = (

            repeat_customers /
            total_customers

        ) * 100







    # =================================================
    # RFM CUSTOMER SEGMENTATION
    # =================================================


    champions = Customer.query.filter(

        Customer.total_orders >= 5,

        Customer.total_spent >= 10000

    ).count()





    loyal_customers = Customer.query.filter(

        Customer.total_orders > 1

    ).count()





    new_customers = Customer.query.filter(

        Customer.total_orders <= 1

    ).count()





    at_risk_customers = Customer.query.filter(

        Customer.total_orders == 0

    ).count()






    # =================================================
    # CUSTOMER SEGMENT CHART
    # =================================================


    segment_labels = [

        "Champions",

        "Loyal",

        "New",

        "At Risk"

    ]




    segment_values = [

        champions,

        loyal_customers,

        new_customers,

        at_risk_customers

    ]






    # =================================================
    # TOP CUSTOMER SPENDING
    # =================================================


    top_customers = Customer.query.order_by(

        Customer.total_spent.desc()

    ).limit(5).all()



    spending_labels = []

    spending_values = []



    for customer in top_customers:


        spending_labels.append(

            customer.name

        )


        spending_values.append(

            float(
                customer.total_spent or 0
            )

        )







    # =================================================
    # CUSTOMER VALUE DISTRIBUTION
    # =================================================


    high_value_customers = Customer.query.filter(

        Customer.total_spent >= 10000

    ).count()



    medium_value_customers = Customer.query.filter(

        Customer.total_spent.between(
            3000,
            9999
        )

    ).count()



    low_value_customers = Customer.query.filter(

        Customer.total_spent < 3000

    ).count()



    value_labels = [

        "High Value",

        "Medium Value",

        "Low Value"

    ]



    value_values = [

        high_value_customers,

        medium_value_customers,

        low_value_customers

    ]






    # =================================================
    # CUSTOMER INSIGHTS
    # =================================================


    highest_customer = Customer.query.order_by(

        Customer.total_spent.desc()

    ).first()



    if highest_customer:


        highest_customer_name = highest_customer.name


        highest_customer_amount = highest_customer.total_spent


    else:


        highest_customer_name = "No Data"


        highest_customer_amount = 0






    loyal_customer = Customer.query.order_by(

        Customer.total_orders.desc()

    ).first()



    if loyal_customer:


        loyal_customer_name = loyal_customer.name


        loyal_customer_orders = loyal_customer.total_orders


    else:


        loyal_customer_name = "No Data"


        loyal_customer_orders = 0







    # =================================================
    # CUSTOMER VALUE SCORE
    # =================================================


    customer_value_score = 0



    if total_revenue > 0:

        customer_value_score += 40



    if repeat_customers > 0:

        customer_value_score += 30



    if retention_rate > 50:

        customer_value_score += 30





    # =================================================
    # SEND DATA
    # =================================================


    return render_template(

        "admin/customers.html",



        customers=customers_data,



        total_customers=total_customers,


        total_revenue=round(
            total_revenue,
            2
        ),



        repeat_customers=repeat_customers,


        average_spending=round(
            average_spending,
            2
        ),




        # Stage 15.2.1 Metrics


        customer_lifetime_value=round(
            customer_lifetime_value,
            2
        ),



        purchase_frequency=round(
            purchase_frequency,
            2
        ),



        retention_rate=round(
            retention_rate,
            2
        ),



        customer_value_score=customer_value_score,





        # RFM


        champions=champions,


        loyal_customers=loyal_customers,


        new_customers=new_customers,


        at_risk_customers=at_risk_customers,



        segment_labels=segment_labels,


        segment_values=segment_values,




        # Spending Chart


        spending_labels=spending_labels,


        spending_values=spending_values,


        ai_recommendations=ai_recommendations,




        # Value Distribution


        value_labels=value_labels,


        value_values=value_values,




        # Insights


        highest_customer_name=highest_customer_name,


        highest_customer_amount=highest_customer_amount,


        loyal_customer_name=loyal_customer_name,


        loyal_customer_orders=loyal_customer_orders

    )

@customers.route("/profile/<int:id>")
def customer_profile(id):


    customer = Customer.query.get_or_404(id)


    orders = Order.query.filter_by(
        customer_id=id
    ).order_by(
        Order.created_at.desc()
    ).all()



    ai_profile = generate_customer_ai_profile(
        customer
    )

    # ==================================
# STAGE 15.4.3 AI PROFILE EXTENSION
# ==================================

    ai_summary = {

        "customer_type":
            "VIP Loyal Customer"
            if customer.total_spent >= 10000
            else "Growing Customer",


        "purchase_probability":
            min(
                95,
                int(
                    (customer.total_orders or 0)
                    * 10
                )
            ),


        "next_purchase":
            "A2 Cow Ghee",


        "risk_level":
            "Low Risk"
            if customer.total_orders > 2
            else "Medium Risk",


        "behaviour":
            "Frequent Buyer"
            if customer.total_orders > 5
            else "Occasional Buyer"

    }



    return render_template(

        "admin/customer_profile.html",

        customer=customer,

        orders=orders,

        ai_profile=ai_profile,

        ai_summary=ai_summary

    )