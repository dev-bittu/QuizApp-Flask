from os.path import dirname, join
import pyzipper

BASE_DIR = dirname(__file__)

def get_string(msg: str):
    while True:
        inp = input(msg)
        if inp:
            return inp

def extract_zip_file(zip_file_path, password, output_path):
    try:
        with pyzipper.AESZipFile(zip_file_path) as zf:
            zf.extractall(
                pwd=password.encode(),
                path=output_path
            )
    except Exception:
        return False
    finally:
        return True

while True:
    zip_passwd = get_string(
        "Enter password of 'utils/sqlite_db.zip' file: "
    )
    if extract_zip_file(join(BASE_DIR, "utils", "sqlite_db.zip"), zip_passwd, join(BASE_DIR, "utils")):
        print("File extracted successfully")
        break
    else:
        print(f"Wrong password: {zip_passwd}")
