from flask import Blueprint, request, redirect, url_for, flash

from models import db

from models.product import Product

from models.stock_history import StockHistory

from models.inventory_transaction import InventoryTransaction



inventory_actions = Blueprint(
    "inventory_actions",
    __name__,
    url_prefix="/admin/inventory"
)





@inventory_actions.route(
    "/update/<int:product_id>",
    methods=["POST"]
)
def update_stock(product_id):


    product = Product.query.get_or_404(
        product_id
    )



    # ===============================
    # GET NEW STOCK VALUE
    # ===============================

    quantity = request.form.get("stock")



    if quantity is None or quantity.strip() == "":


        flash(
            "Please enter stock quantity",
            "danger"
        )


        return redirect(
            url_for("admin_inventory.inventory_dashboard")
        )




    quantity = int(quantity)





    # ===============================
    # OLD STOCK
    # ===============================

    old_stock = product.stock or 0





    # Difference

    change = quantity - old_stock





    # ===============================
    # UPDATE PRODUCT STOCK
    # ===============================

    product.stock = quantity





    # ===============================
    # SAVE STOCK HISTORY
    # ===============================


    history = StockHistory(

        product_id=product.id,

        product_name=product.product_name,

        old_stock=old_stock,

        new_stock=quantity,

        change=change

    )


    db.session.add(history)







    # ===============================
    # SAVE INVENTORY TRANSACTION
    # ===============================


    transaction_type = "IN"


    if change < 0:

        transaction_type = "OUT"





    transaction = InventoryTransaction(

        product_id=product.id,

        transaction_type=transaction_type,

        quantity=abs(change),

        previous_stock=old_stock,

        new_stock=quantity,

        created_by="Admin"

    )




    db.session.add(transaction)





    # ===============================
    # COMMIT DATABASE
    # ===============================


    db.session.commit()





    flash(

        "Stock updated successfully",

        "success"

    )





    return redirect(

        url_for("admin_inventory.inventory_dashboard")

    )