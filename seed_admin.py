from app import app
from models import db
from models.admin import Admin

with app.app_context():

    if not Admin.query.filter_by(username="admin").first():

        admin = Admin(
            username="admin",
            password="admin123",
            full_name="Administrator",
            email="admin@srikrishna.com"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin Created Successfully")

    else:
        print("Admin Already Exists")