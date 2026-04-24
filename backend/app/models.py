from __future__ import annotations

from datetime import date, datetime

from .extensions import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_no = db.Column(db.String(32), unique=True, nullable=False, index=True)
    name = db.Column(db.String(64), nullable=False, index=True)
    gender = db.Column(db.String(16), nullable=True)  # "男"/"女"/"其他"
    birth_date = db.Column(db.Date, nullable=True)

    grade = db.Column(db.String(32), nullable=True, index=True)
    class_name = db.Column(db.String(32), nullable=True, index=True)

    phone = db.Column(db.String(32), nullable=True)
    email = db.Column(db.String(128), nullable=True)
    address = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        def _date(d: date | None):
            return d.isoformat() if d else None

        return {
            "id": self.id,
            "student_no": self.student_no,
            "name": self.name,
            "gender": self.gender,
            "birth_date": _date(self.birth_date),
            "grade": self.grade,
            "class_name": self.class_name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

