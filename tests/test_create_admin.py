from quiz_app.models import User
from app import app
from quiz_app.extentions import db
from pytest import mark


@mark.parametrize(
    "name,password",
    [
        ("admin", "DevBittu@admin")
    ]
)
def test_create_admin(name, password):
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
