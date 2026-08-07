from flask import Blueprint, render_template, request, redirect, url_for

from models import db
from models.order import Order



admin_orders = Blueprint(
    "admin_orders",
    __name__,
    url_prefix="/admin/orders"
)





# ==========================================
# ORDER LIST + SEARCH + FILTER
# ==========================================


@admin_orders.route("/")
def order_list():


    search = request.args.get(
        "search",
        ""
    )


    status_filter = request.args.get(
        "status",
        ""
    )



    query = Order.query



    # SEARCH

    if search:


        query = query.filter(

            db.or_(

                Order.customer_name.ilike(
                    f"%{search}%"
                ),


                Order.customer_phone.ilike(
                    f"%{search}%"
                ),


                Order.id.like(
                    f"%{search}%"
                )

            )

        )





    # STATUS FILTER

    if status_filter:


        query = query.filter(

            Order.status == status_filter

        )




    orders = query.order_by(

        Order.created_at.desc()

    ).all()





    # KPI COUNTS


    total_orders = Order.query.count()



    pending_orders = Order.query.filter_by(

        status="Pending"

    ).count()



    confirmed_orders = Order.query.filter_by(

        status="Confirmed"

    ).count()



    shipped_orders = Order.query.filter_by(

        status="Shipped"

    ).count()



    delivered_orders = Order.query.filter_by(

        status="Delivered"

    ).count()





    return render_template(

        "admin/orders.html",


        orders=orders,


        total_orders=total_orders,


        pending_orders=pending_orders,


        confirmed_orders=confirmed_orders,


        shipped_orders=shipped_orders,


        delivered_orders=delivered_orders,


        search=search,


        status_filter=status_filter

    )









# ==========================================
# ORDER DETAILS
# ==========================================


@admin_orders.route(
    "/<int:order_id>"
)
def order_details(order_id):


    order = Order.query.get_or_404(
        order_id
    )



    return render_template(

        "admin/order_details.html",

        order=order

    )









# ==========================================
# UPDATE STATUS
# ==========================================


@admin_orders.route(
    "/update-status/<int:order_id>",
    methods=["POST"]
)
def update_status(order_id):


    order = Order.query.get_or_404(
        order_id
    )



    status = request.form.get(
        "status"
    )



    order.status = status



    db.session.commit()



    return redirect(

        url_for(

            "admin_orders.order_details",

            order_id=order.id

        )

    )