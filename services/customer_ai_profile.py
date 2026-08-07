"""
=====================================================
Sri Krishna Swacch Aaharam ERP

AI Customer Profile Engine

Stage 15.3.3

=====================================================
"""


def calculate_loyalty_score(customer):


    score = 0



    # Spending behaviour

    if customer.total_spent >= 10000:

        score += 40


    elif customer.total_spent >= 5000:

        score += 25


    else:

        score += 10





    # Purchase frequency


    if customer.total_orders >= 10:

        score += 35


    elif customer.total_orders >= 5:

        score += 20


    else:

        score += 10






    # Segment value


    if customer.segment in [

        "Premium",

        "Premium Customer"

    ]:

        score += 25



    elif customer.segment in [

        "Regular",

        "Regular Customer"

    ]:

        score += 15



    else:

        score += 5





    return min(score,100)









def generate_customer_ai_profile(customer):


    loyalty_score = calculate_loyalty_score(customer)





    if loyalty_score >= 80:


        behaviour = (

            "High Value Loyal Customer"

        )


        suggestion = (

            "Maintain engagement with premium "

            "offers and personalized packages."

        )




    elif loyalty_score >= 50:


        behaviour = (

            "Growing Customer"

        )


        suggestion = (

            "Encourage repeat purchases through "

            "combo offers."

        )




    else:


        behaviour = (

            "New / Low Engagement Customer"

        )


        suggestion = (

            "Improve retention with introductory "

            "offers."

        )





    return {


        "customer_name":

            customer.name,


        "segment":

            customer.segment,


        "loyalty_score":

            loyalty_score,


        "behaviour":

            behaviour,


        "suggestion":

            suggestion

    }