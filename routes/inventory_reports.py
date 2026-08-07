from flask import Blueprint, send_file
from models import db
from models.product import Product

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from openpyxl import Workbook

from io import BytesIO

from datetime import datetime




inventory_reports = Blueprint(
    "inventory_reports",
    __name__,
    url_prefix="/admin/inventory"
)





# =========================================
# PDF INVENTORY REPORT
# =========================================


@inventory_reports.route("/report/pdf")
def inventory_pdf():

    products = Product.query.all()


    buffer = BytesIO()


    doc = SimpleDocTemplate(
        buffer
    )


    elements = []


    styles = getSampleStyleSheet()


    title = Paragraph(
        "Sri Krishna Swacch Aaharam<br/>Inventory Report",
        styles["Title"]
    )


    elements.append(title)

    elements.append(
        Spacer(1,20)
    )



    data = [

        [
            "Product",
            "Category",
            "Stock",
            "Price",
            "Value"
        ]

    ]



    for product in products:


        data.append(

            [

                product.product_name,

                product.category,

                str(product.stock),

                f"₹{product.price}",

                f"₹{product.stock * product.price}"

            ]

        )





    table = Table(data)



    table.setStyle(

        TableStyle(

            [

                ("GRID",(0,0),(-1,-1),0.5,None),

                ("BACKGROUND",(0,0),(-1,0),None)

            ]

        )

    )



    elements.append(table)



    elements.append(

        Spacer(1,20)

    )



    elements.append(

        Paragraph(

            f"Generated Date: {datetime.now().strftime('%d-%m-%Y')}",

            styles["Normal"]

        )

    )



    doc.build(elements)



    buffer.seek(0)



    return send_file(

        buffer,

        as_attachment=True,

        download_name="inventory_report.pdf",

        mimetype="application/pdf"

    )







# =========================================
# EXCEL INVENTORY REPORT
# =========================================



@inventory_reports.route("/report/excel")
def inventory_excel():


    products = Product.query.all()



    workbook = Workbook()


    sheet = workbook.active


    sheet.title = "Inventory Report"




    sheet.append(

        [

            "Product",

            "Category",

            "Stock",

            "Price",

            "Total Value"

        ]

    )





    for product in products:


        sheet.append(

            [

                product.product_name,

                product.category,

                product.stock,

                product.price,

                product.stock * product.price

            ]

        )





    output = BytesIO()


    workbook.save(output)


    output.seek(0)



    return send_file(

        output,

        as_attachment=True,

        download_name="inventory_report.xlsx",

        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )








# =========================================
# LOW STOCK REPORT
# =========================================



@inventory_reports.route("/report/low-stock")
def low_stock_report():


    products = Product.query.filter(

        Product.stock <= 10

    ).all()



    workbook = Workbook()



    sheet = workbook.active


    sheet.title="Low Stock"



    sheet.append(

        [

            "Product",

            "Current Stock"

        ]

    )



    for product in products:


        sheet.append(

            [

                product.product_name,

                product.stock

            ]

        )




    output = BytesIO()


    workbook.save(output)


    output.seek(0)



    return send_file(

        output,

        as_attachment=True,

        download_name="low_stock_report.xlsx",

        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )