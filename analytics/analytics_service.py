from models import db

from models.order import Order
from models.order_item import OrderItem
from models.product import Product

from sqlalchemy import func





def get_total_orders():

    return Order.query.count()






def get_total_revenue():

    revenue = db.session.query(
        func.sum(Order.total_amount)
    ).scalar()


    return revenue or 0







def get_total_customers():

    return db.session.query(
        Order.customer_name
    ).distinct().count()






def get_total_products():

    return Product.query.count()







def get_best_products():


    return db.session.query(

        OrderItem.product_name,

        func.sum(

            OrderItem.quantity *
            OrderItem.price

        ).label("sold")


    ).group_by(

        OrderItem.product_name

    ).order_by(

        func.sum(

            OrderItem.quantity *
            OrderItem.price

        ).desc()

    ).limit(5).all()







def get_category_sales():


    category_sales = db.session.query(

        Product.category,

        func.sum(
            OrderItem.quantity *
            OrderItem.price
        )

    ).join(

        OrderItem,

        Product.id == OrderItem.product_id

    ).group_by(

        Product.category

    ).all()



    # =====================================
    # FALLBACK FOR OLD ORDERS
    # WITHOUT PRODUCT_ID
    # =====================================


    if not category_sales:


        category_sales = db.session.query(

            OrderItem.product_name,

            func.sum(

                OrderItem.quantity *
                OrderItem.price

            )

        ).group_by(

            OrderItem.product_name

        ).all()



    return category_sales








def get_customer_orders():


    return db.session.query(

        Order.customer_name,

        func.count(Order.id).label(
            "orders"
        ),

        func.sum(
            Order.total_amount
        ).label(
            "spent"
        )


    ).group_by(

        Order.customer_name

    ).all()







def get_sales_trend():


    return db.session.query(

        Order.created_at,

        Order.total_amount


    ).order_by(

        Order.created_at

    ).all()