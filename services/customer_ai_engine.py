"""
=====================================================

SRI KRISHNA SWACCH AAHARAM ERP

CUSTOMER AI INTELLIGENCE ENGINE

Stage 15.4.1

Features:
- Customer Lifetime Value Prediction
- Behaviour Score
- Churn Prediction
- AI Customer Segmentation

=====================================================
"""


from datetime import datetime



class CustomerAIEngine:



    # ==========================================
    # CUSTOMER BEHAVIOUR SCORE
    # ==========================================

    @staticmethod
    def calculate_behaviour_score(customer):


        score = 0



        total_orders = (
            customer.total_orders or 0
        )


        total_spent = (
            customer.total_spent or 0
        )



        # Purchase frequency

        if total_orders >= 10:

            score += 40


        elif total_orders >= 5:

            score += 30


        elif total_orders > 0:

            score += 20





        # Spending behaviour


        if total_spent >= 10000:

            score += 40


        elif total_spent >= 5000:

            score += 30


        elif total_spent > 0:

            score += 20






        # Existing loyalty

        if getattr(
            customer,
            "segment",
            None
        ) in [

            "Premium",
            "Premium Customer"

        ]:

            score += 20





        return min(
            score,
            100
        )






    # ==========================================
    # CUSTOMER LIFETIME VALUE
    # ==========================================


    @staticmethod
    def calculate_clv(customer):


        total_spent = (
            customer.total_spent or 0
        )


        total_orders = (
            customer.total_orders or 1
        )



        average_order_value = (

            total_spent /
            total_orders

        )



        loyalty_factor = 1



        if total_orders >= 10:

            loyalty_factor = 3


        elif total_orders >= 5:

            loyalty_factor = 2






        lifetime_value = (

            average_order_value *
            total_orders *
            loyalty_factor

        )



        return round(
            lifetime_value,
            2
        )







    # ==========================================
    # CHURN PREDICTION
    # ==========================================


    @staticmethod
    def predict_churn(customer):


        total_orders = (
            customer.total_orders or 0
        )


        total_spent = (
            customer.total_spent or 0
        )



        behaviour_score = (

            CustomerAIEngine
            .calculate_behaviour_score(
                customer
            )

        )





        if behaviour_score >= 70:


            return {

                "status":
                "Active",


                "risk":
                "Low",


                "message":
                "Customer is highly engaged"

            }




        elif behaviour_score >= 40:


            return {

                "status":
                "Risk",


                "risk":
                "Medium",


                "message":
                "Customer engagement is decreasing"

            }





        else:


            return {

                "status":
                "Churn Risk",


                "risk":
                "High",


                "message":
                "Customer requires retention strategy"

            }








    # ==========================================
    # AI CUSTOMER SEGMENT
    # ==========================================


    @staticmethod
    def predict_segment(customer):


        clv = (

            CustomerAIEngine
            .calculate_clv(
                customer
            )

        )



        behaviour = (

            CustomerAIEngine
            .calculate_behaviour_score(
                customer
            )

        )





        if (

            clv >= 30000

            and

            behaviour >= 70

        ):


            return "VIP Customer"





        elif behaviour >= 50:


            return "Loyal Customer"





        elif behaviour >= 25:


            return "Potential Customer"





        else:


            return "At Risk Customer"








    # ==========================================
    # COMPLETE CUSTOMER AI PROFILE
    # ==========================================


    @staticmethod
    def generate_customer_intelligence(customer):


        churn = (

            CustomerAIEngine
            .predict_churn(
                customer
            )

        )



        return {


            "behaviour_score":

            CustomerAIEngine
            .calculate_behaviour_score(
                customer
            ),



            "customer_lifetime_value":

            CustomerAIEngine
            .calculate_clv(
                customer
            ),



            "segment":

            CustomerAIEngine
            .predict_segment(
                customer
            ),



            "churn":

            churn

        }