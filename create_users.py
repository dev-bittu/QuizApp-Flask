from quiz_app.models import User
from app import app


def create_user(name: str="bittu", password: str="devbittu", is_admin: bool=False):
    '''Create user
    Parameter:
      - name: str = "bittu"
      - password: str = "devbittu"
      - is_admin: bool = False
    Return:
      - user: User
    '''
    with app.app_context():
        u = User.query.filter_by(
            name=name
        )
        if u is not None:
            print(f"User with name '{name}' already exists")
            return
        else:
            user = User(
                name=name,
                password=password,
                is_admin=is_admin
            )
            db.session.add(user)
            db.session.commit()
            print(f"User with name '{name}' created successfully")
        return User

def create_user_bulk(users: list):
    '''Creates users in bulk
    Paramter:
      - users: list 
    Return:
      - None
    Example:
      >>> users = [{"name": "bittu", "password": "devbittu"}, {"name": "anyuser", "password": "mypassword"}]
      >>> create_user_bulk(users)
    '''
    with app.app_context():
        for user in users:
            try:
                db.session.add(User(**user))
                db.session.commit()
            except Exception as e:
                print(f"Error, while adding user {user}\n{e}")

if __name__ == "__main__":
    create_user("admin", "devbittu")
    create_user_bulk()
