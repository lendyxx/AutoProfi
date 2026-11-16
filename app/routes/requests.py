
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

requests_bp = Blueprint(
    "requests",
    __name__,
    url_prefix="/requests"
)

# Демонстрационные данные заявок
requests_data = [
    {
        "id": 1024,
        "client": "Александр Иванов",
        "phone": "+7 900 123-45-67",
        "car": "Toyota Camry",
        "plate": "А123АА39",
        "problem": "Посторонний шум в двигателе",
        "date": "16.11.2026",
        "status": "В работе",
        "mechanic": "Андрей Соколов",
        "diagnosis": "Требуется дополнительная проверка двигателя."
    },
    {
        "id": 1023,
        "client": "Дмитрий Смирнов",
        "phone": "+7 900 222-33-44",
        "car": "BMW 3 Series",
        "plate": "В456ВВ39",
        "problem": "Проверка ходовой части",
        "date": "15.11.2026",
        "status": "Ожидает согласования",
        "mechanic": "",
        "diagnosis": ""
    },
    {
        "id": 1022,
        "client": "Сергей Петров",
        "phone": "+7 900 333-44-55",
        "car": "Volkswagen Polo",
        "plate": "С789СС39",
        "problem": "Замена масла",
        "date": "15.11.2026",
        "status": "Готово",
        "mechanic": "Иван Петров",
        "diagnosis": "Неисправностей не обнаружено."
    }
]


# Список заявок
@requests_bp.route("/")
def index():
    search = request.args.get("search", "").strip().lower()
    status = request.args.get("status", "")

    filtered = requests_data

    if search:
        filtered = [
            item for item in filtered
            if search in str(item["id"]).lower()
            or search in item["client"].lower()
            or search in item["car"].lower()
            or search in item["plate"].lower()
        ]

    if status:
        filtered = [
            item for item in filtered
            if item["status"] == status
        ]

    return render_template(
        "requests.html",
        requests=filtered,
        search=search,
        selected_status=status
    )


# Создание новой заявки
@requests_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        new_request = {
            "id": max(item["id"] for item in requests_data) + 1,
            "client": request.form.get("client", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "car": request.form.get("car", "").strip(),
            "plate": request.form.get("plate", "").strip(),
            "problem": request.form.get("problem", "").strip(),
            "date": "16.11.2026",
            "status": "Новая",
            "mechanic": "",
            "diagnosis": ""
        }

        if not all([
            new_request["client"],
            new_request["phone"],
            new_request["car"],
            new_request["problem"]
        ]):
            flash("Заполните все обязательные поля", "danger")
            return render_template("request_create.html")

        requests_data.append(new_request)

        flash("Заявка успешно создана", "success")

        return redirect(url_for("requests.index"))

    return render_template("request_create.html")


# Просмотр карточки заявки
@requests_bp.route("/<int:request_id>")
def detail(request_id):
    item = next(
        (r for r in requests_data if r["id"] == request_id),
        None
    )

    if item is None:
        return "Заявка не найдена", 404

    return render_template(
        "request_detail.html",
        item=item
    )


# Обновление заявки
@requests_bp.route("/<int:request_id>/update", methods=["POST"])
def update(request_id):
    item = next(
        (r for r in requests_data if r["id"] == request_id),
        None
    )

    if item is None:
        return "Заявка не найдена", 404

    allowed_statuses = [
        "Новая",
        "На диагностике",
        "Ожидает согласования",
        "Согласована",
        "В работе",
        "Готово",
        "Выдано",
        "Отменена"
    ]

    new_status = request.form.get("status", "")
    
    if new_status in allowed_statuses:
        item["status"] = new_status

    item["mechanic"] = request.form.get(
        "mechanic", ""
    ).strip()

    item["diagnosis"] = request.form.get(
        "diagnosis", ""
    ).strip()

    flash("Изменения заявки сохранены", "success")

    return redirect(
        url_for("requests.detail", request_id=request_id)
    )
