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


