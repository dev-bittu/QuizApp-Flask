from create_app import create_app, login_manager
from quiz_app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
