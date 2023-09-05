from create_users import create_user_bulk
from csv import reader

def extract_users(csv_file):
    users = []
    with open(csv_file, "r") as f:
        rows = reader(f)
        for i in rows:
            users.append({
                "id": i[0],
                "name": i[1],
                "password": i[2]
            })
    return users

if __name__ == "__main__":
    users = extract_users("utils/users.csv")
    create_user_bulk(users)

