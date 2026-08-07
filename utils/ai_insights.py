def generate_business_insights(
    total_revenue,
    total_orders,
    total_customers,
    low_stock,
    out_of_stock,
    health_score,
    best_seller
):

    insights = []


    # SALES INTELLIGENCE

    if total_revenue > 0:

        insights.append(
            {
                "title":
                "Revenue Intelligence",

                "icon":
                "💰",

                "message":
                f"Business generated ₹{round(total_revenue,2)} revenue from current orders."
            }
        )

    else:

        insights.append(
            {
                "title":
                "Revenue Alert",

                "icon":
                "⚠️",

                "message":
                "No revenue recorded yet. Start promoting products."
            }
        )



    # CUSTOMER INTELLIGENCE

    if total_customers > 0:

        insights.append(
            {
                "title":
                "Customer Behaviour",

                "icon":
                "👥",

                "message":
                f"{total_customers} customers are registered. Focus on retention strategies."
            }
        )



    # INVENTORY INTELLIGENCE


    if low_stock > 0:

        insights.append(
            {
                "title":
                "Inventory Warning",

                "icon":
                "📦",

                "message":
                f"{low_stock} products require stock attention."
            }
        )


    else:

        insights.append(
            {
                "title":
                "Inventory Health",

                "icon":
                "🌱",

                "message":
                "Inventory levels are healthy."
            }
        )




    # PRODUCT INTELLIGENCE


    insights.append(
        {
            "title":
            "Top Product",

            "icon":
            "🏆",

            "message":
            f"Best performing product: {best_seller}"
        }
    )




    # BUSINESS SCORE


    if health_score >= 75:

        status="Excellent"

    elif health_score >=50:

        status="Good"

    else:

        status="Needs Improvement"



    insights.append(
        {
            "title":
            "AI Business Health",

            "icon":
            "🤖",

            "message":
            f"Business health score is {health_score}%. Status: {status}"
        }
    )


    return insights