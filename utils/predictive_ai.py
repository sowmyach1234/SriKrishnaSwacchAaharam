from math import ceil


def predict_business(
    total_revenue,
    total_orders,
    total_customers,
    total_stock,
    low_stock,
    best_seller
):

    predictions = []


    # Revenue Prediction

    predicted_revenue = round(
        total_revenue * 1.12,
        2
    )

    predictions.append({

        "title":"Next Month Revenue",

        "icon":"📈",

        "value":f"₹ {predicted_revenue:,.2f}",

        "description":"Estimated 12% business growth."

    })


    # Customer Growth

    predicted_customers = ceil(
        total_customers * 1.08
    )

    predictions.append({

        "title":"Expected Customers",

        "icon":"👥",

        "value":predicted_customers,

        "description":"Predicted customer increase."

    })


    # Inventory Demand

    demand = ceil(
        total_orders * 1.15
    )

    predictions.append({

        "title":"Expected Product Demand",

        "icon":"📦",

        "value":demand,

        "description":"Estimated units required next month."

    })


    # Fast Moving Product

    predictions.append({

        "title":"Fast Moving Product",

        "icon":"🔥",

        "value":best_seller,

        "description":"Likely to continue leading sales."

    })


    # Inventory Risk

    if low_stock > 10:

        risk = "High"

    elif low_stock > 5:

        risk = "Medium"

    else:

        risk = "Low"


    predictions.append({

        "title":"Inventory Risk",

        "icon":"⚠",

        "value":risk,

        "description":"Current stock health assessment."

    })

    return predictions