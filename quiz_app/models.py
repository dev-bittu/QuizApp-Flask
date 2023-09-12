from .extentions import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    questions = db.relationship("Question", backref="creator")
    is_admin = db.Column(db.Boolean, default=False)
    result = db.relationship("Result", backref="user")
    question_set = db.Column(db.Integer, db.ForeignKey("questionset.id"), nullable=True)

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def __repr__(self):
        return f"User({self.id}, '{self.name}')"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, unique=False, nullable=False)
    option1 = db.Column(db.String, nullable=False)
    option2 = db.Column(db.String, nullable=False)
    option3 = db.Column(db.String, nullable=False)
    option4 = db.Column(db.String, nullable=False)
    correct_option = db.Column(db.CHAR, nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    question_set_id = db.Column(db.Integer, db.ForeignKey("questionset.id"), nullable=True)

    def __repr__(self):
        return f"Question({self.id}, '{self.question}', {self.creator})"

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_number = db.Column(db.Integer, nullable=False)
    correct = db.Column(db.Integer, default=0, nullable=False)
    not_attempt = db.Column(db.Integer, default=0, nullable=False)
    incorrect = db.Column(db.Integer, default=0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Result({self.id}, {self.correct}/{self.total_number})"

class QuestionSet(db.Model):
    __tablename__ = 'questionset'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True)
    questions = db.relationship("Question", backref="qset")
    user_id = db.relationship("User", backref="qset")

    def __repr__(self):
        return f"QuestionSet({self.id}, {[i.id for i in self.questions]})"

