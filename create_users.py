from quiz_app.models import User
from app import app
from quiz_app.extentions import db

def create_user(name: str = "bittu", id: int = None, password: str = "devbittu", is_admin: bool = False):
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
        ).first()
        if u is not None:
            print(f"User with name '{name}' already exists")
            return
        else:
            user = User(
                id=id,
                name=name,
                is_admin=is_admin
            ) if id is None else User(
                name=name,
                is_admin=is_admin
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"User with name '{name}' created successfully")
        return User

def create_user_bulk(users: list, hashed=False):
    '''Creates users in bulk
    Paramter:
      - users: list 
    Return:
      - None
    Example:
      >>> users = [{"id": 1, "name": "bittu", "password": "devbittu"}, {"name": "anyuser", "password": "mypassword"}]
      >>> create_user_bulk(users)
    '''
    with app.app_context():
        for user in users:
            try:
                u = User(**user)
                u.set_password(user["password"])
                db.session.add(u)
                db.session.commit()
                print(user, u.password)
            except Exception as e:
                print(f"Error, while adding user {user}\n{e}")

if __name__ == "__main__":
    create_user(
        name="admin", 
        password="devbittu", 
        id=100, 
        is_admin=True
    )
    #create_user_bulk()
