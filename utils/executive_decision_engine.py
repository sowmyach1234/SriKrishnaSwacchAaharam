def generate_decisions(
    revenue,
    orders,
    customers,
    healthy_stock,
    low_stock,
    out_stock,
    best_seller
):

    decisions = []

    if out_stock > 0:

        decisions.append({

            "priority":"High",

            "icon":"🚨",

            "title":"Critical Inventory",

            "message":
            f"{out_stock} products are out of stock."

        })

    if low_stock > 0:

        decisions.append({

            "priority":"Medium",

            "icon":"📦",

            "title":"Restock Soon",

            "message":
            f"{low_stock} products are below minimum stock."

        })

    if revenue > 0:

        decisions.append({

            "priority":"Low",

            "icon":"💰",

            "title":"Revenue",

            "message":
            f"Current revenue ₹{revenue:,.0f}."

        })

    decisions.append({

        "priority":"Info",

        "icon":"🏆",

        "title":"Best Seller",

        "message":
        best_seller

    })

    confidence = 92

    if out_stock > 5:
        confidence = 84

    elif low_stock > 10:
        confidence = 88

    return decisions, confidence