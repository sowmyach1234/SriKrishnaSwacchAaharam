def executive_summary(
    total_revenue,
    total_orders,
    total_customers,
    healthy_stock,
    low_stock,
    out_of_stock,
    business_health_score,
    best_seller
):

    recommendations = []

    if low_stock > 0:
        recommendations.append(
            {
                "icon":"📦",
                "title":"Restock Inventory",
                "message":f"{low_stock} products need replenishment."
            }
        )

    if out_of_stock > 0:
        recommendations.append(
            {
                "icon":"🚨",
                "title":"Out of Stock",
                "message":f"{out_of_stock} products are unavailable."
            }
        )

    if total_orders < 20:
        recommendations.append(
            {
                "icon":"📣",
                "title":"Increase Sales",
                "message":"Run promotions to improve order volume."
            }
        )

    if total_customers > 0:
        recommendations.append(
            {
                "icon":"👥",
                "title":"Customer Loyalty",
                "message":"Reward repeat customers with exclusive offers."
            }
        )

    recommendations.append(
        {
            "icon":"🏆",
            "title":"Best Seller",
            "message":f"{best_seller} continues to lead sales."
        }
    )

    return {
        "score": business_health_score,
        "revenue": total_revenue,
        "orders": total_orders,
        "customers": total_customers,
        "recommendations": recommendations
    }