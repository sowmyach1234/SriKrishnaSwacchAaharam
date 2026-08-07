from flask import Blueprint, render_template

from models.customer import Customer
from models.order import Order
from models.order_item import OrderItem

from sqlalchemy import func
from collections import Counter

from services.customer_ai_profile import generate_customer_ai_profile


customer = Blueprint(
    "customer",
    __name__,
    url_prefix="/admin/customers"
)



# ==================================
# CUSTOMER LIST
# ==================================

@customer.route("/")
def customer_list():

    customers = Customer.query.order_by(

        Customer.total_spent.desc()

    ).all()



    total_customers = Customer.query.count()



    total_sales = sum(

        customer.total_spent or 0

        for customer in customers

    )



    return render_template(

        "admin/customers.html",

        customers=customers,

        total_customers=total_customers,

        total_sales=total_sales

    )





# ==================================
# CUSTOMER PROFILE + AI INSIGHTS
# ==================================

@customer.route(
    "/<int:customer_id>"
)
def customer_profile(customer_id):


    customer = Customer.query.get_or_404(
        customer_id
    )


    orders = Order.query.filter_by(
        customer_id=customer.id
    ).order_by(
        Order.created_at.desc()
    ).all()




        # ==================================
    # CUSTOMER BEHAVIOUR ANALYTICS
    # ==================================


    total_orders = len(orders)


    total_spent = customer.total_spent or 0



    # Average Order Value

    average_order_value = 0


    if total_orders > 0:

        average_order_value = round(
            total_spent / total_orders,
            2
        )





    # Last Purchase

    last_purchase = "No Purchase"


    if orders:

        last_purchase = orders[0].created_at.strftime(
            "%d %b %Y"
        )






    # Purchase Frequency

    if total_orders >= 10:

        purchase_frequency = "High"

    elif total_orders >= 5:

        purchase_frequency = "Medium"

    else:

        purchase_frequency = "Low"







    # Repeat Purchase Probability

    repeat_probability = min(
        total_orders * 8,
        95
    )







    # Customer Segment

    if total_spent >= 10000:

        customer_segment = "Premium Organic Buyer"

    elif total_spent >= 5000:

        customer_segment = "Regular Organic Buyer"

    else:

        customer_segment = "New Customer"






    # ==================================
    # CATEGORY PREFERENCE ANALYSIS
    # ==================================


    category_counter = Counter()



    for order in orders:


        print("ORDER:", order.id)


        items = OrderItem.query.filter_by(
            order_id=order.id
        ).all()


        for item in items:

            print(
                "ITEM:",
                item.product_name,
                "PRODUCT ID:",
                item.product_id,
                "PRODUCT:",
                item.product
            )



        

            if item.product:

                category_counter[
                item.product.category
                ] += item.quantity


        else:

            category_counter[
                item.product_name
            ] += item.quantity




            category_labels = list(
                category_counter.keys()
            )


            category_values = list(
                category_counter.values()
            )

            print("CATEGORY LABELS:", category_labels)
            print("CATEGORY VALUES:", category_values)






            # ==================================
            # MONTHLY PURCHASE TREND
            # ==================================


            monthly_counter = Counter()



            for order in orders:


                month = order.created_at.strftime(
                    "%b"
                )


                monthly_counter[month] += (
                    order.total_amount or 0
                )




            monthly_labels = list(
                monthly_counter.keys()
            )


            monthly_values = list(
                monthly_counter.values()
            )



            # ==============================
            # AI CUSTOMER PROFILE
            # ==============================

            ai_profile = generate_customer_ai_profile(
                customer
            )



            # ==============================
            # AI SUMMARY
            # ==============================

            ai_summary = {

                "next_purchase":
                    ai_profile.get(
                        "next_purchase",
                        "Based on previous buying pattern"
                    ),


                "customer_type":
                    ai_profile.get(
                        "customer_type",
                        "Regular Customer"
                    ),


                "recommendation":
                    ai_profile.get(
                        "recommendation",
                        "Continue personalized offers"
                    ),


                "risk":
                    ai_profile.get(
                        "risk",
                        "Low"
                    )

            }



            return render_template(

            "admin/customer_profile.html",

            customer=customer,

            orders=orders,

            ai_profile=ai_profile,

            ai_summary=ai_summary,


            # Behaviour Analytics

            purchase_frequency=purchase_frequency,

            repeat_probability=repeat_probability,

            customer_segment=customer_segment,

            last_purchase=last_purchase,

            average_order_value=average_order_value,


            # Charts

            category_labels=category_labels,

            category_values=category_values,

            monthly_labels=monthly_labels,

            monthly_values=monthly_values

        )