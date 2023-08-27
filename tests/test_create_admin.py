from quiz_app.models import User
from app import app
from quiz_app.extentions import db


name = "admin"  # Username of administrator
password = "Dev-Bittu@admin"  # Password for administrator

def test_create_admin():
    with app.app_context():
        u = User.query.filter_by(
            name=name
        ).first()  # Check if any user already exists

        assert u is None, f"User with name '{name}' already exists"

        user = User(
            name=name,
            password=password,
            is_admin=True
        )
        db.session.add(user)
        db.session.commit()

        assert user == User.query.filter_by(
            name=name,
            password=password,
            is_admin=True
        ).first(), "User not created.."
