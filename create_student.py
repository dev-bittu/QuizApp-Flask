from random import randint as r

d = ['sneha', 'ayush', 'piyush', 'saniya', 'priya', 'abhinav', 'ritu', 'renu', 'shubham', 'devika', 'madhur', 'rishabh', 'aman', 'bittu', 'nikki', 'prem', 'nikhil', 'rishav', 'rohit', 'deepali', 'vansh', 'sneha2', 'rehan', 'rahul', 'anjali']

a = "1234567890@#()qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM,."

data = []

for i, index in zip(d, range(len(d))):
    pwd = ""
    for _ in range(5):
        pwd = pwd+a[r(0, len(a)-1)]
    data.append({
        "id": index+1,
        "name": i,
        "password": pwd
    })

from app import app
from quiz_app.models import *
from quiz_app.extentions import db

with app.app_context():
    for i in data:
        user = User(**i)
        user.set_password(i["password"])
        db.session.add(user)
        print(i, user.password)
    db.session.commit()
