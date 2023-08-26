from flask import (
    Blueprint,
    render_template as render,
    flash,
    redirect,
    url_for,
    request
)
from . import models
from .extentions import db
from flask_login import (
    logout_user,
    login_required,
    login_user,
    current_user
)


main = Blueprint("main", __name__)
ADD_QUESTIONS = 3

@main.route("/")
def index():
    return render("index.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if not current_user.is_anonymous:
        flash("You are already logged in, logout to login with another account", "info")
        return redirect(url_for("main.index"))
    if request.method == "POST":
        data = request.form.to_dict()
        if "is_admin" in data.keys():
            user = models.User.query.filter_by(
                name=data["name"],
                password=data["password"],
                is_admin=True
            ).first()
        else:
            user = models.User.query.filter_by(
                name=data["name"],
                password=data["password"],
                is_admin=False
            ).first()
        if user is not None:
            login_user(user)
            flash("logged in successfully", "success")
            return redirect(url_for("main.index"))
        else:
            flash("User's name or password is wrong", "warning")
    return render("login.html")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("logged out", "info")
    return redirect(url_for("main.index"))
    

@main.route("/register", methods=["GET", "POST"])
def register():
    if not current_user.is_anonymous:
        flash("You are already logged in, logout to login with another account", "info")
        return redirect(url_for('main.index'))
    if request.method == "POST":
        data = request.form.to_dict()
        name = data["name"]
        password = data["password"]
        user = models.User(name=name, password=password)
        db.session.add(user)
        db.session.commit()
        flash("register complete", "success")
        return redirect(url_for("main.login"))
    return render("register.html")

@main.route("/add", methods=["GET", "POST"])
@login_required
def add_questions():
    if request.method == "POST":
        data = request.form.to_dict()
        for i in range(1, ADD_QUESTIONS+1):
            question = models.Question(
                question=data[f"q{i}"],
                option1=data[f"q{i}o1"],
                option2=data[f"q{i}o2"],
                option3=data[f"q{i}o3"],
                option4=data[f"q{i}o4"],
                correct_option=data[f"q{i}c"][0].upper(),
                creator_id=current_user.id
            )
            db.session.add(question)
            db.session.commit()
        else:
            flash("your questions added successfully", "success")
    return render("add_questions.html", questions=ADD_QUESTIONS)

@main.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    if request.method == "POST":
        data = request.form.to_dict()
        total_questions = len(models.Question.query.all())
        result = models.Result(
            total_number=total_questions,
            correct=0,
            not_attempt=0,
            incorrect=0,
            user_id=current_user.id
        )
        for i in range(1, total_questions+1):
            q, o = data.get(f"q{i}", None), data.get(f"q{i}o", None)
            question = models.Question.query.filter_by(
                id=q,
                correct_option=o
            ).first()
            if question is not None:
                result.correct += 1
            else:
                result.incorrect += 1
        result.not_attempt = result.total_number-(result.correct+result.incorrect)
        db.session.add(result)
        db.session.commit()
        flash("quiz complete", "success")
        return redirect(url_for("main.result"))
    return render(
        "quiz.html",
        questions=models.Question.query.all(),
        zip=zip,
        show=True if models.Result.query.filter_by(user_id=current_user.id).first() is None else False
    )

@main.route("/result")
@login_required
def result():
    res = models.Result.query.filter_by(
        user_id=current_user.id
    )
    if res is not None:
        return render(
            "result.html", 
            results=res, 
            user=current_user
        )
    else:
        return render(
            "result.html",
            results=models.Result(
                user_id=current_user.id,
                total_number=0,
                correct=0,
                incorrect=0,
                not_attempt=0
            ), user=current_user
        )


@main.route("/admin")
@login_required
def admin():
    if current_user.is_admin:
        res = models.Result.query.all()
        return render("admin.html", results=res)
    else:
        flash("You are not an admin, so you can't access this portal", "warning")
        return redirect(url_for('main.index'))

@main.route('/favicon.ico')
def favicon():
    print("fkkfjd")
    return url_for('static', filename='image/favicon.ico')
