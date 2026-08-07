from flask import Blueprint, send_file
from models.order import Order

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from io import BytesIO

from datetime import datetime



invoice = Blueprint(
    "invoice",
    __name__
)




@invoice.route(
    "/invoice/<int:order_id>"
)
def generate_invoice(order_id):


    order = Order.query.get_or_404(
        order_id
    )



    buffer = BytesIO()



    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )



    elements = []



    styles = getSampleStyleSheet()



    # =========================
    # LOGO
    # =========================


    logo_path = (
        "static/logo/logo.png"
    )


    logo = Image(
        logo_path,
        width=80,
        height=80
    )


    elements.append(logo)



    elements.append(
        Spacer(1,20)
    )



    elements.append(

        Paragraph(
            "Sri Krishna Swacch Aaharam",
            styles["Title"]
        )

    )



    elements.append(

        Paragraph(
            "100% Natural • Organic • Traditional",
            styles["Normal"]
        )

    )



    elements.append(
        Spacer(1,20)
    )





    # =========================
    # ORDER DETAILS
    # =========================


    elements.append(

        Paragraph(
            f"Invoice ID : #{order.id}",
            styles["Heading3"]
        )

    )


    elements.append(

        Paragraph(
            f"Date : {order.created_at.strftime('%d-%m-%Y')}",
            styles["Normal"]
        )

    )


    elements.append(
        Spacer(1,20)
    )






    # =========================
    # CUSTOMER DETAILS
    # =========================


    customer_data = [

        [
            "Customer",
            order.customer_name
        ],

        [
            "Phone",
            order.customer_phone
        ],

        [
            "Address",
            order.customer_address
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
            )

        ])

    )


    elements.append(
        customer_table
    )


    elements.append(
        Spacer(1,25)
    )





    # =========================
    # PRODUCTS
    # =========================


    product_data = [

        [
            "Product",
            "Qty",
            "Price",
            "Total"
        ]

    ]



    for item in order.items:


        product_data.append(

            [

                item.product_name,

                str(item.quantity),

                f"₹ {item.price}",

                f"₹ {item.price * item.quantity}"

            ]

        )




    product_table = Table(
        product_data
    )



    product_table.setStyle(

        TableStyle([


            (
            "BACKGROUND",
            (0,0),
            (-1,0),
            colors.green
            ),



            (
            "TEXTCOLOR",
            (0,0),
            (-1,0),
            colors.white
            ),



            (
            "GRID",
            (0,0),
            (-1,-1),
            0.5,
            colors.grey
            )


        ])

    )



    elements.append(
        product_table
    )



    elements.append(
        Spacer(1,25)
    )






    elements.append(

        Paragraph(

            f"Total Amount : ₹ {order.total_amount}",

            styles["Heading2"]

        )

    )



    elements.append(

        Spacer(1,20)

    )



    elements.append(

        Paragraph(

            "Thank you for supporting natural farming 🌿",

            styles["Normal"]

        )

    )



    pdf.build(
        elements
    )



    buffer.seek(0)



    return send_file(

        buffer,

        as_attachment=True,

        download_name=
        f"invoice_{order.id}.pdf",

        mimetype=
        "application/pdf"

    )