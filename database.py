from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String, nullable=True)
    added = db.Column(db.DateTime, nullable=False, default=func.now())

    department_id = db.Column(db.Integer, db.ForeignKey("department.id", ondelete='SET NULL'))
    department = relationship("Department", back_populates="employees")

    def __repr__(self):
        return f"User(fullname={self.fullname!r})"


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    employees = relationship(
        "Employee", back_populates="department"
    )

class Book(db.Model):
    """Модель для книг"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = relationship("Genre", back_populates="books")
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())  # Поле для отслеживания времени добавления
    is_read = db.Column(db.Boolean, default=False)  # Дополнительное поле (для дополнительного задания)

    def __repr__(self):
        return f"<Book {self.title}>"


class Genre(db.Model):
    """Модель жанров книг"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    books = relationship("Book", back_populates="genre")  # Связь с книгами
