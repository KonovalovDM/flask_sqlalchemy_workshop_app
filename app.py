#!/usr/bin/env python

import os

from flask import Flask
from flask import render_template

from database import db, Employee, Department
from flask import request, jsonify

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
db.init_app(app)

@app.route('/')
def index():
    # Получаем последние 15 книг по порядку убывания времени создания
    books = Book.query.order_by(Book.created_at.desc()).limit(15).all()
    return render_template('index.html', books=books)

@app.route('/genres/<int:genre_id>')
def show_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    books_in_genre = Book.query.filter_by(genre_id=genre_id).all()
    return render_template('genre_books.html', genre=genre, books=books_in_genre)

@app.route('/mark_as_read', methods=['POST'])
def mark_book_as_read():
    book_id = int(request.form['book_id'])
    is_read = bool(int(request.form['is_read']))
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Книга не найдена"}), 404
    book.is_read = is_read
    db.session.commit()
    return jsonify({"message": "Статус книги обновлен"})

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
