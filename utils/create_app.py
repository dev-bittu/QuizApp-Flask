from flask import Flask
from quiz_app.routes import main
from quiz_app.extentions import db
from flask_login import LoginManager

login_manager = LoginManager()

def create_app(config_file:str="config.py") -> Flask:
    '''Create flask instance, set configuration from config_file.
    Paramaneter:
        - config_file: str
    Return:
        - app: Flask
    '''
    app = Flask(__name__)

    app.config["UPLOAD_FOLDER"] = "upload_files"
    app.config.from_pyfile(config_file)
    app.register_blueprint(main)
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "main.login"
    with app.app_context():
        db.create_all()

    return app
