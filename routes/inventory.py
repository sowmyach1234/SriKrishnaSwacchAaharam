from flask import Blueprint, render_template, request, send_file
from models.product import Product
from models.stock_history import StockHistory

from models import db

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

import csv
import os



inventory = Blueprint(
    "inventory",
    __name__,
    url_prefix="/admin/inventory"
)



# ================================
# INVENTORY DASHBOARD
# ================================


@inventory.route("/")
def dashboard():

    products = Product.query.all()

    total_products = len(products)

    total_stock = sum(
        product.stock
        for product in products
    )


    low_stock = Product.query.filter(
        Product.stock <= 10
    ).count()


    return render_template(
        "admin/inventory.html",
        products=products,
        total_products=total_products,
        total_stock=total_stock,
        low_stock=low_stock
    )




# =================================
# DOWNLOAD INVENTORY PDF
# =================================


@inventory.route("/download/pdf")
def download_inventory_pdf():

    file_path = "inventory_report.pdf"


    pdf = SimpleDocTemplate(
        file_path,
        pagesize=A4
    )


    elements=[]

    styles=getSampleStyleSheet()



    elements.append(

        Paragraph(
            """
            <b>
            Sri Krishna Swacch Aaharam
            </b>
            <br/>
            Inventory Report
            """,
            styles["Title"]
        )

    )


    elements.append(
        Spacer(1,20)
    )



    data=[

        [
            "Product",
            "Category",
            "Stock",
            "Price"
        ]

    ]


    products=Product.query.all()



    for product in products:

        data.append(

            [

                product.product_name,

                product.category,

                str(product.stock),

                f"₹ {product.price}"

            ]

        )



    table=Table(data)



    table.setStyle(

        TableStyle(

            [

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
                    (-1,0),
                    colors.lightgrey
                )

            ]

        )

    )


    elements.append(table)


    pdf.build(elements)



    return send_file(

        file_path,

        as_attachment=True

    )






# =================================
# DOWNLOAD STOCK HISTORY PDF
# =================================


@inventory.route("/stock-history/pdf")
def stock_history_pdf():


    file_path="stock_history_report.pdf"



    pdf=SimpleDocTemplate(
        file_path,
        pagesize=A4
    )


    elements=[]

    styles=getSampleStyleSheet()



    elements.append(

        Paragraph(

            """
            <b>
            Stock Movement Report
            </b>
            """,

            styles["Title"]

        )

    )


    elements.append(
        Spacer(1,20)
    )



    data=[

        [
            "Product",
            "Old Stock",
            "New Stock",
            "Change"
        ]

    ]


    history=StockHistory.query.all()



    for item in history:


        data.append(

            [

                item.product_name,

                item.old_stock,

                item.new_stock,

                item.change

            ]

        )



    table=Table(data)


    table.setStyle(

        TableStyle(

            [

                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    .5,
                    colors.grey
                )

            ]

        )

    )


    elements.append(table)



    pdf.build(elements)



    return send_file(

        file_path,

        as_attachment=True

    )






# =================================
# CSV EXPORT
# =================================


@inventory.route("/download/csv")
def download_inventory_csv():


    file_path="inventory.csv"



    products=Product.query.all()



    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:


        writer=csv.writer(file)


        writer.writerow(

            [

                "Product",
                "Category",
                "Stock",
                "Price"

            ]

        )


        for product in products:


            writer.writerow(

                [

                    product.product_name,

                    product.category,

                    product.stock,

                    product.price

                ]

            )



    return send_file(

        file_path,

        as_attachment=True

    )