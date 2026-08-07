from flask import Blueprint, render_template, request

from models.stock_history import StockHistory


stock_history = Blueprint(
    "stock_history",
    __name__,
    url_prefix="/admin/inventory"
)


@stock_history.route("/history")
def history():

    search = request.args.get("search", "")
    movement = request.args.get("type", "")


    query = StockHistory.query



    # Search product
    if search:

        query = query.filter(
            StockHistory.product_name.ilike(
                f"%{search}%"
            )
        )



    # Filter stock movement

    if movement == "IN":

        query = query.filter(
            StockHistory.change > 0
        )


    elif movement == "OUT":

        query = query.filter(
            StockHistory.change < 0
        )



    # IMPORTANT:
    # StockHistory model contains updated_at
    # NOT created_at

    histories = query.order_by(
        StockHistory.updated_at.desc()
    ).all()



    total_records = StockHistory.query.count()


    stock_in = StockHistory.query.filter(
        StockHistory.change > 0
    ).count()


    stock_out = StockHistory.query.filter(
        StockHistory.change < 0
    ).count()



    return render_template(
        "admin/stock_history.html",
        histories=histories,
        total_records=total_records,
        stock_in=stock_in,
        stock_out=stock_out,
        search=search,
        movement=movement
    )