from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash
)


import sys

import os

from datetime import datetime

from flask import send_file


from models import (
    Product,
    Order,
    Customer
)

from models import db, AdminActivity




settings = Blueprint(
    "settings",
    __name__,
    url_prefix="/admin/settings"
)





# =====================================
# SETTINGS PAGE
# =====================================


@settings.route("/")
def settings_page():


    if not session.get("admin_logged_in"):

        return redirect(
            url_for(
                "admin.login"
            )
        )



    # =====================================
    # SYSTEM INFORMATION
    # =====================================


    system_info = {


        "application":
        "Sri Krishna Swacch Aaharam",



        "framework":
        "Flask",



        "database":
        "SQLite",



        "python_version":
        sys.version.split()[0],



        "environment":
        "Development",



        "status":
        "Active",



        "products":
        Product.query.count(),



        "orders":
        Order.query.count(),



        "customers":
        Customer.query.count()


    }

    backup_info = {


    "database":
    "SQLite",


    "status":
    "Available",


    "last_backup":
    datetime.now().strftime(
        "%d-%m-%Y %H:%M"
    )


    }





    # =====================================
    # NOTIFICATION SETTINGS
    # =====================================


    notification_settings = {


        "low_stock":

        session.get(
            "low_stock_alerts",
            True
        ),



        "order_alerts":

        session.get(
            "order_alerts",
            True
        ),



        "customer_alerts":

        session.get(
            "customer_alerts",
            False
        )


    }




    return render_template(

        "admin/settings.html",



        # ADMIN PROFILE

        admin_username="admin",

        admin_role="Administrator",

        admin_status="Active",




        # STORE INFORMATION


        store_name=
        "Sri Krishna Swacch Aaharam",



        business_type=
        "Organic Food Retail",



        store_location=
        "Andhra Pradesh, India",



        store_contact=
        "+91 XXXXX XXXXX",



        store_email=
        "info@skswacchaaharam.com",




        # NOTIFICATIONS


        notification_settings=
        notification_settings,



        # SYSTEM


        system_info=
        system_info,


        backup_info=backup_info


    )









# =====================================
# CHANGE PASSWORD
# =====================================


@settings.route(
    "/change-password",
    methods=[
        "GET",
        "POST"
    ]
)

def change_password():


    if not session.get("admin_logged_in"):

        return redirect(
            url_for(
                "admin.login"
            )
        )




    if request.method == "POST":


        current_password = request.form.get(
            "current_password"
        )


        new_password = request.form.get(
            "new_password"
        )


        confirm_password = request.form.get(
            "confirm_password"
        )



        saved_password = session.get(
            "admin_password",
            "admin123"
        )



        if current_password != saved_password:


            flash(
                "Current password is incorrect",
                "error"
            )


            return redirect(
                url_for(
                    "settings.change_password"
                )
            )





        if new_password != confirm_password:


            flash(
                "New passwords do not match",
                "error"
            )


            return redirect(
                url_for(
                    "settings.change_password"
                )
            )






        session["admin_password"] = new_password



        flash(
            "Password changed successfully",
            "success"
        )



        return redirect(
            url_for(
                "settings.settings_page"
            )
        )






    return render_template(
        "admin/change_password.html"
    )









# =====================================
# NOTIFICATION UPDATE
# =====================================


@settings.route(
    "/notifications",
    methods=[
        "POST"
    ]
)

def update_notifications():



    if not session.get("admin_logged_in"):

        return redirect(
            url_for(
                "admin.login"
            )
        )




    session["low_stock_alerts"] = (

        True

        if request.form.get(
            "low_stock"
        )

        else False

    )





    session["order_alerts"] = (

        True

        if request.form.get(
            "order_alerts"
        )

        else False

    )





    session["customer_alerts"] = (

        True

        if request.form.get(
            "customer_alerts"
        )

        else False

    )





    flash(
        "Notification settings updated",
        "success"
    )



    activity = AdminActivity(

    action="Notification Settings Updated",

    description="Admin updated notification preferences",

    status="Success"

    )


    db.session.add(activity)

    db.session.commit()



    return redirect(
        url_for(
            "settings.settings_page"
        )
    )



# =====================================
# DATABASE BACKUP
# =====================================


@settings.route(
    "/backup"
)

def download_backup():


    if not session.get("admin_logged_in"):

        return redirect(
            url_for(
                "admin.login"
            )
        )



    database_path = os.path.join(
    os.getcwd(),
    "instance",
    "database.db"
    )



    if not os.path.exists(database_path):

        flash(
            "Database file not found",
            "error"
        )


        return redirect(
            url_for(
                "settings.settings_page"
            )
        )



    return send_file(

        database_path,

        as_attachment=True,

        download_name=
        "SriKrishna_Backup.db"

    )