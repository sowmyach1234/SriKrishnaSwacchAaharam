from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)


from models import AdminActivity



activity = Blueprint(

    "activity",

    __name__,

    url_prefix="/admin/activity"

)




@activity.route("/")
def activity_log():


    if not session.get(
        "admin_logged_in"
    ):


        return redirect(
            url_for(
                "admin.login"
            )
        )



    activities = AdminActivity.query.order_by(

        AdminActivity.created_at.desc()

    ).all()



    return render_template(

        "admin/activity_log.html",

        activities=activities

    )