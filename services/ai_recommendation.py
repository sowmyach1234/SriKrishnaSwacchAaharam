"""
=====================================================
Sri Krishna Swacch Aaharam ERP

AI Recommendation Engine

Stage 15.3

Purpose:
Customer purchase recommendation system

=====================================================
"""


from models.product import Product
from models.customer import Customer





# =====================================================
# PRODUCT RECOMMENDATION ENGINE
# =====================================================


def recommend_products(customer):

    """
    Generate product recommendations
    based on customer behaviour
    """



    recommendations = []



    if not customer:


        return {

            "products": [],

            "reason":
            "No customer data available"

        }





    # ==============================================
    # PREMIUM CUSTOMER LOGIC
    # ==============================================


    if customer.segment in [

        "Premium",

        "Premium Customer"

    ]:



        products = Product.query.filter(

            Product.category.in_(

                [

                    "A2 Cow Ghee",

                    "Cold Pressed Oils",

                    "Dry Fruits"

                ]

            )

        ).limit(3).all()





        reason = (

            "Customer shows premium buying behaviour. "

            "Recommended high-value organic products."

        )





    # ==============================================
    # REGULAR CUSTOMER LOGIC
    # ==============================================


    elif customer.segment in [

        "Regular",

        "Regular Customer"

    ]:



        products = Product.query.filter(

            Product.category.in_(

                [

                    "Organic Millets",

                    "Millet Rice",

                    "Healthy Snacks"

                ]

            )

        ).limit(3).all()




        reason = (

            "Customer purchases frequently. "

            "Recommended regular consumption products."

        )






    # ==============================================
    # NEW CUSTOMER LOGIC
    # ==============================================


    else:



        products = Product.query.order_by(

            Product.created_at.desc()

        ).limit(3).all()



        reason = (

            "New customer detected. "

            "Recommended popular products."

        )






    for product in products:


        recommendations.append(

            {

                "name":
                product.product_name,


                "category":
                product.category,


                "price":
                product.price


            }

        )






    return {


        "products":
        recommendations,


        "reason":
        reason


    }









# =====================================================
# CUSTOMER BUYING INSIGHT
# =====================================================


def generate_customer_recommendation(customer):


    if not customer:


        return {


            "message":
            "Customer information unavailable"

        }





    recommendation = recommend_products(

        customer

    )





    return {


        "customer":
        customer.name,


        "recommendations":
        recommendation["products"],


        "insight":
        recommendation["reason"]


    }