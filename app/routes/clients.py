
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

clients_bp = Blueprint(
    "clients",
    __name__,
    url_prefix="/clients"
)

clients_data = [
    {
        "id": 1,
        "name": "Александр Иванов",
        "phone": "+7 900 123-45-67",
        "email": "ivanov@mail.ru",
        "cars": ["Toyota Camry"],
        "date": "10.11.2026"
    },
    {
        "id": 2,
        "name": "Дмитрий Смирнов",
        "phone": "+7 900 222-33-44",
        "email": "smirnov@mail.ru",
        "cars": ["BMW 3 Series"],
        "date": "12.11.2026"
    },
    {
        "id": 3,
        "name": "Сергей Петров",
        "phone": "+7 900 333-44-55",
        "email": "petrov@mail.ru",
        "cars": ["Volkswagen Polo"],
        "date": "15.11.2026"
    }
]


@clients_bp.route("/")
def index():
    search = request.args.get("search", "").strip().lower()

    filtered = clients_data

    if search:
        filtered = [
            client for client in clients_data
            if search in client["name"].lower()
            or search in client["phone"].lower()
            or search in client["email"].lower()
        ]

    return render_template(
        "clients.html",
        clients=filtered,
        search=search
    )


@clients_bp.route("/create", methods=["POST"])
def create():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()

    if not name or not phone:
        flash("Укажите имя и телефон клиента", "danger")
        return redirect(url_for("clients.index"))

    clients_data.append({
        "id": max((c["id"] for c in clients_data), default=0) + 1,
        "name": name,
        "phone": phone,
        "email": email,
        "cars": [],
        "date": "16.11.2026"
    })

    flash("Клиент успешно добавлен", "success")
    return redirect(url_for("clients.index"))
