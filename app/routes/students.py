"""Student CRUD endpoints."""

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from app.errors import error_response
from app.extensions import db
from app.models import Student
from app.validators import validate_student_payload

students_bp = Blueprint("students", __name__)


def get_student_or_404(student_id):
    student = db.session.get(Student, student_id)
    if student is None:
        return None, error_response("Student not found.", 404)
    return student, None


@students_bp.get("")
@students_bp.get("/")
def list_students():
    students = db.session.execute(db.select(Student).order_by(Student.id)).scalars()
    return {"data": [student.to_dict() for student in students]}, 200


@students_bp.post("")
@students_bp.post("/")
def create_student():
    payload = request.get_json(silent=True)
    data, errors = validate_student_payload(payload)
    if errors:
        return error_response("Validation failed.", 400, errors)

    student = Student(**data)
    db.session.add(student)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error_response("A student with that email already exists.", 409)
    return {"data": student.to_dict()}, 201


@students_bp.get("/<int:student_id>")
def get_student(student_id):
    student, error = get_student_or_404(student_id)
    if error:
        return error
    return {"data": student.to_dict()}, 200


@students_bp.put("/<int:student_id>")
@students_bp.patch("/<int:student_id>")
def update_student(student_id):
    student, error = get_student_or_404(student_id)
    if error:
        return error

    payload = request.get_json(silent=True)
    data, errors = validate_student_payload(payload, partial=request.method == "PATCH")
    if errors:
        return error_response("Validation failed.", 400, errors)
    if not data:
        return error_response("At least one student field must be supplied.", 400)

    for field, value in data.items():
        setattr(student, field, value)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error_response("A student with that email already exists.", 409)
    return {"data": student.to_dict()}, 200


@students_bp.delete("/<int:student_id>")
def delete_student(student_id):
    student, error = get_student_or_404(student_id)
    if error:
        return error
    db.session.delete(student)
    db.session.commit()
    return "", 204
