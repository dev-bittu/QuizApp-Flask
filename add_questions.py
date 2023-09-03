from csv import reader
from quiz_app.extentions import db
from quiz_app.models import *
from app import app


def load_questions(file) -> dict:
    '''Load questions from csv file and serialize them
    Argument:
        file - csv_file
    Return:
        questions: dict - qbank of questions
        ex: {name: [{q: question, o: options, co: correct_option}]}
    '''
    qbank, questions = [], {}

    with open(file, "r") as f:
        rows = reader(f)
        for row in rows:
            qbank.append(row)

    qbank = qbank[1:]

    for row in qbank:
        roll_no, data = row[3], row[4:]
        total_questions = len(data) // 3
        qs = []
        for i in range(0, len(data), 3):
            q, o, co = data[i], data[i+1].split("\n"), data[i+2]
            if (n:=len(o)) != 4:
                print(f"\ninstead of filling 4 option RollNo:{roll_no} has filled {n} options.!!!\n".upper())
            else:
                qs.append({
                    "q": q,
                    "o": tuple(o),
                    "co": co
                })
        questions = questions | {roll_no: qs}

    return questions 


def add_to_db(qbank: dict) -> int:
    '''Add questions to db
    Argument:
        qbank: dict - question bank
    Return:
        questions_added: int
    '''
    questions_added = 0
    
    with app.app_context():
        for id, qs in qbank.items():
            u = User.query.filter_by(id=id).first()
            if u is not None:
                for q in qs:
                    q = Question(
                        question=q["q"],
                        option1=q["o"][0],
                        option2=q["o"][1],
                        option3=q["o"][2],
                        option4=q["o"][3],
                        correct_option=q["co"],
                        creator_id=u.id
                    )
                    db.session.add(q)
                    questions_added += 1
                    print(f"Total Questions Added: {questions_added}", end="\r")
            else:
                print(f"\nuser doesn't exists with id {id}\n".upper())
            db.session.commit()
    return questions_added

if __name__ == "__main__":
    qbank = load_questions("questions.csv")
    q_added = add_to_db(qbank)
    print(f"\nQuestion Added: {q_added}")
