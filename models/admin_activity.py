from datetime import datetime

from models import db



class AdminActivity(db.Model):


    __tablename__ = "admin_activity"



    id = db.Column(
        db.Integer,
        primary_key=True
    )



    action = db.Column(
        db.String(200),
        nullable=False
    )



    description = db.Column(
        db.String(500)
    )



    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



    status = db.Column(
        db.String(50),
        default="Success"
    )