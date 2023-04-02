#!/usr/bin/env python

import os

from flask import Flask
from flask import render_template

from database import db, Employee, Department

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
db.init_app(app)


with app.app_context():
    db.drop_all()
    db.create_all()

    # fill DB with testing data(fixtures)
    engineering = Department(name="Разработка")
    db.session.add(engineering)
    hr = Department(name="Рекрутинг")
    db.session.add(hr)

    alex = Employee(fullname="Александр Иванов", department=engineering)
    db.session.add(alex)
    daria = Employee(fullname="Дарья Петрова", department=engineering)
    db.session.add(daria)
    petr = Employee(fullname="Петр Сидоров", department=hr)
    db.session.add(petr)

    db.session.commit()


@app.route("/")
def all_employees():
    employees = Employee.query.all()
    return render_template("all_employees.html", employees=employees)


@app.route("/department/<int:department_id>")
def employees_by_department(department_id):
    department = Department.query.get_or_404(department_id)
    return render_template(
        "employees_by_department.html",
        department_name=department.name,
        employees=department.employees,
    )


if __name__ == '__main__':
    app.run()
