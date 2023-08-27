from quiz_app.models import User
from app import app
from quiz_app.extentions import db


name = "admin"  # Username of administrator
password = "Dev-Bittu@admin"  # Password for administrator


with app.app_context():
    u = User.query.filter_by(
        name=name
    ).first()  # Check if any user already exists
    if u is None:
        user = User(
            name=name,
            password=password,
            is_admin=True
        )
        db.session.add(user)
        db.session.commit()
        print(
            f"Administer created successfully... {user}"
        )
    else:
        print(
            f"A user already exists with the name {name}",
        )

