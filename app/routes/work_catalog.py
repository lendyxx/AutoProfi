
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

work_catalog_bp = Blueprint(
    "work_catalog",
    __name__,
    url_prefix="/work-catalog"
)

work_data = [
    {
        "id": 1,
        "name": "Замена моторного масла",
        "category": "Двигатель",
        "description": "Слив старого и залив нового моторного масла",
        "price": 1500,
        "duration": 1.0
    },
    {
        "id": 2,
        "name": "Замена тормозных колодок",
        "category": "Тормозная система",
        "description": "Замена передних или задних тормозных колодок",
        "price": 2500,
        "duration": 1.5
    },
    {
        "id": 3,
        "name": "Диагностика подвески",
        "category": "Ходовая часть",
        "description": "Проверка состояния элементов подвески",
        "price": 1200,
        "duration": 1.0
    },
    {
        "id": 4,
        "name": "Компьютерная диагностика",
        "category": "Электрика",
        "description": "Считывание и анализ ошибок электронных систем",
        "price": 1800,
        "duration": 1.0
    },
    {
        "id": 5,
        "name": "Замена воздушного фильтра",
        "category": "Двигатель",
        "description": "Демонтаж старого и установка нового фильтра",
        "price": 700,
        "duration": 0.5
    },
    {
        "id": 6,
        "name": "Развал-схождение",
        "category": "Ходовая часть",
        "description": "Проверка и регулировка углов установки колёс",
        "price": 3000,
        "duration": 1.5
    }
]

categories = [
    "Двигатель",
    "Тормозная система",
    "Ходовая часть",
    "Электрика",
    "Трансмиссия",
    "Кузовные работы",
    "Другое"
]


@work_catalog_bp.route("/")
def index():
    search = request.args.get("search", "").strip().lower()
    selected_category = request.args.get("category", "")

    filtered = work_data

    if search:
        filtered = [
            work for work in filtered
            if search in work["name"].lower()
            or search in work["description"].lower()
        ]

    if selected_category:
        filtered = [
            work for work in filtered
            if work["category"] == selected_category
        ]

    return render_template(
        "work_catalog.html",
        works=filtered,
        categories=categories,
        selected_category=selected_category,
        search=search
    )


@work_catalog_bp.route("/create", methods=["POST"])
def create():
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "")
    description = request.form.get("description", "").strip()
    price = request.form.get("price", type=int)
    duration = request.form.get("duration", type=float)

    if not all([name, category, description, price, duration]):
        flash("Заполните все обязательные поля", "danger")
        return redirect(url_for("work_catalog.index"))

    if category not in categories:
        flash("Выберите корректную категорию", "danger")
        return redirect(url_for("work_catalog.index"))

    if price <= 0 or duration <= 0:
        flash("Цена и время выполнения должны быть больше нуля", "danger")
        return redirect(url_for("work_catalog.index"))

    new_work = {
        "id": max((work["id"] for work in work_data), default=0) + 1,
        "name": name,
        "category": category,
        "description": description,
        "price": price,
        "duration": duration
    }

    work_data.append(new_work)

    flash("Услуга успешно добавлена", "success")
    return redirect(url_for("work_catalog.index"))
