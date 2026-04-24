from __future__ import annotations

from datetime import date

from flask import Blueprint, jsonify, request
from sqlalchemy import func, or_

from .extensions import db
from .models import Student

api_bp = Blueprint("api", __name__)


def _parse_int(value: str | None, default: int, min_value: int | None = None, max_value: int | None = None):
    try:
        v = int(value) if value is not None else default
    except Exception:
        v = default
    if min_value is not None:
        v = max(v, min_value)
    if max_value is not None:
        v = min(v, max_value)
    return v


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except Exception:
        return None


@api_bp.get("/students")
def list_students():
    page = _parse_int(request.args.get("page"), 1, min_value=1)
    page_size = _parse_int(request.args.get("page_size"), 10, min_value=1, max_value=100)
    q = (request.args.get("q") or "").strip()
    grade = (request.args.get("grade") or "").strip()
    class_name = (request.args.get("class_name") or "").strip()

    query = Student.query
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Student.name.like(like), Student.student_no.like(like)))
    if grade:
        query = query.filter(Student.grade == grade)
    if class_name:
        query = query.filter(Student.class_name == class_name)

    query = query.order_by(Student.id.desc())
    pagination = query.paginate(page=page, per_page=page_size, error_out=False)

    return jsonify(
        {
            "items": [s.to_dict() for s in pagination.items],
            "page": page,
            "page_size": page_size,
            "total": pagination.total,
        }
    )


@api_bp.get("/students/<int:student_id>")
def get_student(student_id: int):
    s = Student.query.get_or_404(student_id)
    return jsonify(s.to_dict())


@api_bp.post("/students")
def create_student():
    data = request.get_json(silent=True) or {}

    student_no = (data.get("student_no") or "").strip()
    name = (data.get("name") or "").strip()
    if not student_no or not name:
        return jsonify({"message": "student_no 和 name 必填"}), 400

    if Student.query.filter_by(student_no=student_no).first():
        return jsonify({"message": "student_no 已存在"}), 409

    s = Student(
        student_no=student_no,
        name=name,
        gender=(data.get("gender") or None),
        birth_date=_parse_date(data.get("birth_date")),
        grade=(data.get("grade") or None),
        class_name=(data.get("class_name") or None),
        phone=(data.get("phone") or None),
        email=(data.get("email") or None),
        address=(data.get("address") or None),
    )
    db.session.add(s)
    db.session.commit()
    return jsonify(s.to_dict()), 201


@api_bp.put("/students/<int:student_id>")
def update_student(student_id: int):
    s = Student.query.get_or_404(student_id)
    data = request.get_json(silent=True) or {}

    if "student_no" in data:
        new_no = (data.get("student_no") or "").strip()
        if not new_no:
            return jsonify({"message": "student_no 不能为空"}), 400
        exists = Student.query.filter(Student.student_no == new_no, Student.id != s.id).first()
        if exists:
            return jsonify({"message": "student_no 已存在"}), 409
        s.student_no = new_no

    if "name" in data:
        new_name = (data.get("name") or "").strip()
        if not new_name:
            return jsonify({"message": "name 不能为空"}), 400
        s.name = new_name

    if "gender" in data:
        s.gender = data.get("gender") or None
    if "birth_date" in data:
        s.birth_date = _parse_date(data.get("birth_date"))
    if "grade" in data:
        s.grade = data.get("grade") or None
    if "class_name" in data:
        s.class_name = data.get("class_name") or None
    if "phone" in data:
        s.phone = data.get("phone") or None
    if "email" in data:
        s.email = data.get("email") or None
    if "address" in data:
        s.address = data.get("address") or None

    db.session.commit()
    return jsonify(s.to_dict())


@api_bp.delete("/students/<int:student_id>")
def delete_student(student_id: int):
    s = Student.query.get_or_404(student_id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({"deleted": True})


@api_bp.get("/overview")
def overview():
    """仪表盘 / 班级页用的汇总数据（一次请求）。"""
    total = Student.query.count()

    by_grade = [
        {"grade": g or "未填写", "count": int(c)}
        for g, c in db.session.query(Student.grade, func.count(Student.id))
        .group_by(Student.grade)
        .order_by(Student.grade)
        .all()
    ]

    by_gender = [
        {"gender": g or "未填写", "count": int(c)}
        for g, c in db.session.query(Student.gender, func.count(Student.id))
        .group_by(Student.gender)
        .all()
    ]

    class_summary = [
        {
            "grade": row[0] or "未填写",
            "class_name": row[1] or "未填写",
            "count": int(row[2]),
        }
        for row in db.session.query(Student.grade, Student.class_name, func.count(Student.id))
        .group_by(Student.grade, Student.class_name)
        .order_by(Student.grade, Student.class_name)
        .all()
    ]

    return jsonify(
        {
            "total": total,
            "by_grade": by_grade,
            "by_gender": by_gender,
            "class_summary": class_summary,
        }
    )

