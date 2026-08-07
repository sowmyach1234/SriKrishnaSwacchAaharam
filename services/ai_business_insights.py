from models import db
from models.product import Product
from models.customer import Customer
from models.order import Order
from models.order_item import OrderItem

from sqlalchemy import func

from datetime import datetime


class AIBusinessInsights:

    @staticmethod
    def generate():

        insights = {}

        # ==========================================
        # BASIC COUNTS
        # ==========================================

        total_products = Product.query.count()
        total_customers = Customer.query.count()
        total_orders = Order.query.count()

        total_revenue = db.session.query(
            func.sum(Order.total_amount)
        ).scalar() or 0

        total_stock = db.session.query(
            func.sum(Product.stock)
        ).scalar() or 0

        # ==========================================
        # INVENTORY
        # ==========================================

        healthy_stock = Product.query.filter(
            Product.stock > Product.minimum_stock
        ).count()

        low_stock = Product.query.filter(
            Product.stock <= Product.minimum_stock,
            Product.stock > 0
        ).count()

        out_stock = Product.query.filter(
            Product.stock == 0
        ).count()

        # ==========================================
        # BEST SELLER
        # ==========================================

        best_product = db.session.query(

            OrderItem.product_name,

            func.sum(
                OrderItem.quantity
            ).label("qty")

        ).group_by(

            OrderItem.product_name

        ).order_by(

            func.sum(
                OrderItem.quantity
            ).desc()

        ).first()

        if best_product:
            best_seller = best_product.product_name
        else:
            best_seller = "No Sales Yet"

        # ==========================================
        # BEST CATEGORY
        # ==========================================

        best_category = db.session.query(

            Product.category,

            func.sum(
                OrderItem.quantity
            ).label("qty")

        ).join(

            OrderItem,
            Product.id == OrderItem.product_id

        ).group_by(

            Product.category

        ).order_by(

            func.sum(
                OrderItem.quantity
            ).desc()

        ).first()

        if best_category:
            top_category = best_category.category
        else:
            top_category = "No Data"

        # ==========================================
        # BUSINESS HEALTH SCORE
        # ==========================================

        score = 0

        if total_revenue > 0:
            score += 25

        if total_orders > 0:
            score += 20

        if total_customers > 0:
            score += 20

        if healthy_stock > low_stock:
            score += 20

        if total_products > 0:
            score += 15

        if score >= 90:
            health = "Excellent"

        elif score >= 75:
            health = "Very Good"

        elif score >= 60:
            health = "Good"

        elif score >= 40:
            health = "Average"

        else:
            health = "Needs Attention"

        # ==========================================
        # INVENTORY STATUS
        # ==========================================

        if out_stock > 10:
            inventory_status = "Critical"

        elif low_stock > 5:
            inventory_status = "Warning"

        else:
            inventory_status = "Healthy"

        # ==========================================
        # CUSTOMER STATUS
        # ==========================================

        if total_customers >= 100:
            customer_growth = "Excellent"

        elif total_customers >= 50:
            customer_growth = "Growing"

        elif total_customers >= 10:
            customer_growth = "Stable"

        else:
            customer_growth = "Early Stage"

        # ==========================================
        # AI RECOMMENDATIONS
        # ==========================================

        recommendations = []

        if low_stock > 0:
            recommendations.append(
                "Increase inventory for low-stock products."
            )

        if out_stock > 0:
            recommendations.append(
                "Restock out-of-stock products immediately."
            )

        if total_orders == 0:
            recommendations.append(
                "Focus on acquiring initial customers."
            )

        if total_customers > 20:
            recommendations.append(
                "Launch a customer loyalty program."
            )

        if total_revenue > 50000:
            recommendations.append(
                "Business is growing. Consider expanding inventory."
            )

        if best_seller != "No Sales Yet":
            recommendations.append(
                f"Promote your best seller: {best_seller}."
            )

        if top_category != "No Data":
            recommendations.append(
                f"Increase products in {top_category} category."
            )

        if not recommendations:
            recommendations.append(
                "Business is healthy. Continue monitoring performance."
            )

        # ==========================================
        # EXECUTIVE SUMMARY
        # ==========================================

        summary = (
            f"The business currently has "
            f"{total_products} products, "
            f"{total_customers} customers and "
            f"{total_orders} completed orders "
            f"with total revenue of ₹{round(total_revenue,2):,.2f}."
        )

        # ==========================================
        # RETURN
        # ==========================================

        insights["health_score"] = score
        insights["health"] = health
        insights["inventory_status"] = inventory_status
        insights["customer_growth"] = customer_growth
        insights["best_seller"] = best_seller
        insights["best_category"] = top_category
        insights["recommendations"] = recommendations
        insights["summary"] = summary
        insights["generated_at"] = datetime.now().strftime(
            "%d %b %Y %I:%M %p"
        )

        return insights