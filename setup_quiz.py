from os import system, makedirs
from os.path import dirname, join
import pyzipper
import shutil

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

def remove_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print("Folder removed successfully!")
    except FileNotFoundError:
        print("Error: Folder not found.")
        exit()
    except OSError as e:
        print("Error:", str(e))
        exit()

def copy_file(source_file, destination_file):
    try:
        makedirs(dirname(destination_file), exist_ok=True)
        shutil.copy2(source_file, destination_file)
        print("File copied successfully!")
    except FileNotFoundError:
        print("Error: File not found.")
        exit()
    except shutil.SameFileError:
        print("Error: Source and destination are the same file.")
        exit()
    except OSError as e:
        print("Error:", str(e))
        exit()

remove_folder(join(BASE_DIR, "instance"))
copy_file(
    join(BASE_DIR, "utils", "db.sqlite"), join(BASE_DIR, "instance", "db.sqlite")
)
