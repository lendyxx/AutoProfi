
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

employees_bp = Blueprint(
    "employees",
    __name__,
    url_prefix="/employees"
)

roles = [
    "Администратор",
    "Приёмщик",
    "Механик",
    "Кладовщик",
    "Директор"
]

employees_data = [
    {
        "id": 1,
        "name": "Александр Иванов",
        "phone": "+7 900 111-22-33",
        "email": "admin@autoprofi.ru",
        "position": "Администратор",
        "status": "Активен"
    },
    {
        "id": 2,
        "name": "Андрей Соколов",
        "phone": "+7 900 222-33-44",
        "email": "mechanic@autoprofi.ru",
        "position": "Механик",
        "status": "Активен"
    },
    {
        "id": 3,
        "name": "Иван Петров",
        "phone": "+7 900 333-44-55",
        "email": "warehouse@autoprofi.ru",
        "position": "Кладовщик",
        "status": "Активен"
    },
    {
        "id": 4,
        "name": "Дмитрий Смирнов",
        "phone": "+7 900 444-55-66",
        "email": "manager@autoprofi.ru",
        "position": "Приёмщик",
        "status": "Активен"
    },
    {
        "id": 5,
        "name": "Сергей Петров",
        "phone": "+7 900 555-66-77",
        "email": "director@autoprofi.ru",
        "position": "Директор",
        "status": "Активен"
    }
]


@employees_bp.route("/")
def index():
    search = request.args.get("search", "").strip().lower()
    selected_role = request.args.get("role", "")
    selected_status = request.args.get("status", "")

    filtered = employees_data

    if search:
        filtered = [
            employee for employee in filtered
            if search in employee["name"].lower()
            or search in employee["phone"].lower()
            or search in employee["email"].lower()
        ]

    if selected_role:
        filtered = [
            employee for employee in filtered
            if employee["position"] == selected_role
        ]

    if selected_status:
        filtered = [
            employee for employee in filtered
            if employee["status"] == selected_status
        ]

    return render_template(
        "employees.html",
        employees=filtered,
        roles=roles,
        search=search,
        selected_role=selected_role,
        selected_status=selected_status,
        total_employees=len(employees_data),
        active_employees=sum(
            1 for employee in employees_data
            if employee["status"] == "Активен"
        )
    )


@employees_bp.route("/create", methods=["POST"])
def create():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    position = request.form.get("position", "")

    if not all([name, phone, position]):
        flash("Заполните обязательные поля", "danger")
        return redirect(url_for("employees.index"))

    if position not in roles:
        flash("Выберите корректную должность", "danger")
        return redirect(url_for("employees.index"))

    if any(
        employee["email"].lower() == email.lower()
        for employee in employees_data if email
    ):
        flash("Сотрудник с таким email уже существует", "danger")
        return redirect(url_for("employees.index"))

    employees_data.append({
        "id": max((e["id"] for e in employees_data), default=0) + 1,
        "name": name,
        "phone": phone,
        "email": email,
        "position": position,
        "status": "Активен"
    })

    flash("Сотрудник успешно добавлен", "success")
    return redirect(url_for("employees.index"))


@employees_bp.route("/<int:employee_id>/status", methods=["POST"])
def change_status(employee_id):
    employee = next(
        (e for e in employees_data if e["id"] == employee_id),
        None
    )

    if employee is None:
        return "Сотрудник не найден", 404

    new_status = request.form.get("status", "")

    if new_status not in ["Активен", "Неактивен"]:
        flash("Некорректный статус", "danger")
        return redirect(url_for("employees.index"))

    employee["status"] = new_status

    flash("Статус сотрудника обновлён", "success")
    return redirect(url_for("employees.index"))
