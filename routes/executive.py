from flask import Blueprint, render_template, session, redirect, url_for

from sqlalchemy import func

from models import (
    db,
    Product,
    Order,
    Customer,
    OrderItem
)

from utils.executive_ai import executive_summary


executive = Blueprint(
    "executive",
    __name__,
    url_prefix="/admin/executive"
)


@executive.route("/")
def dashboard():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    total_products = Product.query.count()

    total_orders = Order.query.count()

    total_customers = Customer.query.count()

    total_revenue = db.session.query(
        func.sum(Order.total_amount)
    ).scalar() or 0

    healthy_stock = Product.query.filter(
        Product.stock > Product.minimum_stock
    ).count()

    low_stock = Product.query.filter(
        Product.stock <= Product.minimum_stock,
        Product.stock > 0
    ).count()

    out_of_stock = Product.query.filter(
        Product.stock == 0
    ).count()

    best = db.session.query(
        OrderItem.product_name,
        func.sum(OrderItem.quantity)
    ).group_by(
        OrderItem.product_name
    ).order_by(
        func.sum(OrderItem.quantity).desc()
    ).first()

    if best:
        best_seller = best[0]
    else:
        best_seller = "No Sales Yet"

    score = 0

    if total_revenue > 0:
        score += 30

    if total_orders > 0:
        score += 25

    if total_customers > 0:
        score += 20

    if healthy_stock > low_stock:
        score += 25

    summary = executive_summary(
        total_revenue,
        total_orders,
        total_customers,
        healthy_stock,
        low_stock,
        out_of_stock,
        score,
        best_seller
    )

    return render_template(
        "admin/executive.html",

        summary=summary,

        total_products=total_products,

        healthy_stock=healthy_stock,

        low_stock=low_stock,

        out_of_stock=out_of_stock
    )