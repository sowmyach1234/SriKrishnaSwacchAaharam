from flask import Blueprint, send_file, make_response

from models.order import Order
from models.product import Product

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

import os


# ==============================
# BLUEPRINT
# ==============================

export = Blueprint(
    "export",
    __name__
)



# ==============================
# INVOICE PDF EXPORT
# ==============================

@export.route("/invoice/<int:order_id>")
def invoice(order_id):

    order = Order.query.get_or_404(order_id)


    file_path = f"invoice_{order.id}.pdf"


    pdf = SimpleDocTemplate(
        file_path,
        pagesize=A4
    )


    elements = []

    styles = getSampleStyleSheet()



    # ==========================
    # LOGO
    # ==========================

    logo_path = os.path.join(
        "static",
        "logo",
        "logo.png"
    )


    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=80,
            height=80
        )

        elements.append(logo)



    elements.append(
        Spacer(1,15)
    )



    # ==========================
    # HEADER
    # ==========================

    elements.append(

        Paragraph(

            """
            <b>
            Sri Krishna Swacch Aaharam
            </b>
            <br/>
            Organic & Traditional Food Store
            """,

            styles["Title"]

        )

    )


    elements.append(
        Spacer(1,20)
    )



    # ==========================
    # CUSTOMER DETAILS
    # ==========================

    customer_data = [

        [
            "Invoice No",
            f"#{order.id}"
        ],

        [
            "Customer",
            order.customer_name or ""
        ],

        [
            "Phone",
            order.customer_phone or ""
        ],

        [
            "Address",
            order.customer_address or ""
        ],

        [
            "Status",
            order.status or ""
        ]

    ]


    customer_table = Table(
        customer_data,
        colWidths=[120,300]
    )


    customer_table.setStyle(

        TableStyle([

            (
                "GRID",
                (0,0),
                (-1,-1),
                0.5,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0,0),
                (0,-1),
                colors.lightgrey
            )

        ])

    )


    elements.append(
        customer_table
    )


    elements.append(
        Spacer(1,25)
    )



    # ==========================
    # PRODUCT DETAILS
    # ==========================


    product_data = [

        [
            "Product",
            "Quantity",
            "Price"
        ]

    ]



    for item in order.items:

        product_data.append(

            [

                item.product_name,

                str(item.quantity),

                f"₹ {item.price}"

            ]

        )



    product_table = Table(
        product_data,
        colWidths=[250,80,100]
    )


    product_table.setStyle(

        TableStyle([

            (
                "GRID",
                (0,0),
                (-1,-1),
                0.5,
                colors.black
            ),

            (
                "BACKGROUND",
                (0,0),
                (-1,0),
                colors.lightgrey
            )

        ])

    )


    elements.append(
        product_table
    )


    elements.append(
        Spacer(1,25)
    )



    # ==========================
    # TOTAL
    # ==========================

    elements.append(

        Paragraph(

            f"""
            <b>
            Total Amount : ₹ {order.total_amount}
            </b>
            """,

            styles["Heading2"]

        )

    )


    elements.append(
        Spacer(1,30)
    )



    elements.append(

        Paragraph(

            """
            Thank you for shopping with us 🌿
            <br/>
            Sri Krishna Swacch Aaharam
            <br/>
            Fresh • Natural • Traditional
            """,

            styles["Normal"]

        )

    )



    pdf.build(elements)



    return send_file(

        file_path,

        as_attachment=True

    )





# ==============================
# ANALYTICS REPORT EXPORT
# ==============================


@export.route("/analytics-report")
def export_analytics():


    orders = Order.query.all()

    products = Product.query.all()



    revenue = sum(

        order.total_amount

        for order in orders

    )



    report = f"""

Sri Krishna Swacch Aaharam

Business Analytics Report


==============================


Total Orders : {len(orders)}

Total Products : {len(products)}

Total Revenue : ₹{revenue}



==============================

"""



    response = make_response(report)


    response.headers["Content-Disposition"] = (

        "attachment; filename=analytics_report.txt"

    )


    response.headers["Content-Type"] = (

        "text/plain"

    )


    return response