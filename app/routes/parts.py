
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

parts_bp = Blueprint(
    "parts",
    __name__,
    url_prefix="/parts"
)

parts_data = [
    {
        "id": 1,
        "name": "Масляный фильтр",
        "article": "OF-1001",
        "category": "Фильтры",
        "quantity": 25,
        "min_quantity": 5,
        "purchase_price": 450,
        "sale_price": 750
    },
    {
        "id": 2,
        "name": "Тормозные колодки передние",
        "article": "BR-2045",
        "category": "Тормозная система",
        "quantity": 3,
        "min_quantity": 5,
        "purchase_price": 1800,
        "sale_price": 2600
    },
    {
        "id": 3,
        "name": "Воздушный фильтр",
        "article": "AF-3012",
        "category": "Фильтры",
        "quantity": 18,
        "min_quantity": 5,
        "purchase_price": 500,
        "sale_price": 850
    },
    {
        "id": 4,
        "name": "Свеча зажигания",
        "article": "SP-4020",
        "category": "Двигатель",
        "quantity": 4,
        "min_quantity": 8,
        "purchase_price": 350,
        "sale_price": 600
    },
    {
        "id": 5,
        "name": "Тормозная жидкость",
        "article": "BF-5010",
        "category": "Тормозная система",
        "quantity": 12,
        "min_quantity": 3,
        "purchase_price": 650,
        "sale_price": 950
    }
]

parts_categories = [
    "Фильтры",
    "Тормозная система",
    "Двигатель",
    "Подвеска",
    "Электрика",
    "Трансмиссия",
    "Расходные материалы",
    "Другое"
]

stock_movements = []


def add_movement(part, movement_type, quantity, comment):
    stock_movements.insert(0, {
        "id": len(stock_movements) + 1,
        "part_name": part["name"],
        "article": part["article"],
        "type": movement_type,
        "quantity": quantity,
        "comment": comment,
        "date": "16.11.2026"
    })


@parts_bp.route("/")
def index():
    search = request.args.get("search", "").strip().lower()
    selected_category = request.args.get("category", "")
    stock_filter = request.args.get("stock", "")

    filtered = parts_data

    if search:
        filtered = [
            part for part in filtered
            if search in part["name"].lower()
            or search in part["article"].lower()
        ]

    if selected_category:
        filtered = [
            part for part in filtered
            if part["category"] == selected_category
        ]

    if stock_filter == "low":
        filtered = [
            part for part in filtered
            if part["quantity"] <= part["min_quantity"]
        ]
    elif stock_filter == "available":
        filtered = [
            part for part in filtered
            if part["quantity"] > part["min_quantity"]
        ]

    return render_template(
        "parts.html",
        parts=filtered,
        categories=parts_categories,
        selected_category=selected_category,
        stock_filter=stock_filter,
        search=search,
        movements=stock_movements[:10],
        total_parts=len(parts_data),
        low_stock=sum(
            1 for part in parts_data
            if part["quantity"] <= part["min_quantity"]
        ),
        total_quantity=sum(part["quantity"] for part in parts_data)
    )


@parts_bp.route("/create", methods=["POST"])
def create():
    name = request.form.get("name", "").strip()
    article = request.form.get("article", "").strip().upper()
    category = request.form.get("category", "")
    quantity = request.form.get("quantity", type=int)
    min_quantity = request.form.get("min_quantity", type=int)
    purchase_price = request.form.get("purchase_price", type=int)
    sale_price = request.form.get("sale_price", type=int)

    if (
        not name or not article or not category
        or quantity is None or min_quantity is None
        or purchase_price is None or sale_price is None
    ):
        flash("Заполните все обязательные поля", "danger")
        return redirect(url_for("parts.index"))

    if category not in parts_categories:
        flash("Выберите корректную категорию", "danger")
        return redirect(url_for("parts.index"))

    if (
        quantity < 0 or min_quantity < 0
        or purchase_price <= 0 or sale_price <= 0
    ):
        flash("Проверьте количество и стоимость", "danger")
        return redirect(url_for("parts.index"))

    if any(part["article"] == article for part in parts_data):
        flash("Запчасть с таким артикулом уже существует", "danger")
        return redirect(url_for("parts.index"))

    new_part = {
        "id": max((part["id"] for part in parts_data), default=0) + 1,
        "name": name,
        "article": article,
        "category": category,
        "quantity": quantity,
        "min_quantity": min_quantity,
        "purchase_price": purchase_price,
        "sale_price": sale_price
    }

    parts_data.append(new_part)

    if quantity > 0:
        add_movement(
            new_part,
            "Поступление",
            quantity,
            "Начальный остаток при добавлении запчасти"
        )

    flash("Запчасть успешно добавлена", "success")
    return redirect(url_for("parts.index"))


@parts_bp.route("/<int:part_id>/movement", methods=["POST"])
def movement(part_id):
    part = next(
        (item for item in parts_data if item["id"] == part_id),
        None
    )

    if part is None:
        return "Запчасть не найдена", 404

    movement_type = request.form.get("type", "")
    quantity = request.form.get("quantity", type=int)
    comment = request.form.get("comment", "").strip()

    if movement_type not in ["Поступление", "Списание"]:
        flash("Неизвестный тип операции", "danger")
        return redirect(url_for("parts.index"))

    if quantity is None or quantity <= 0:
        flash("Количество должно быть больше нуля", "danger")
        return redirect(url_for("parts.index"))

    if movement_type == "Списание" and quantity > part["quantity"]:
        flash("Недостаточно запчастей на складе", "danger")
        return redirect(url_for("parts.index"))

    if movement_type == "Поступление":
        part["quantity"] += quantity
    else:
        part["quantity"] -= quantity

    add_movement(
        part,
        movement_type,
        quantity,
        comment or "Без комментария"
    )

    flash("Складская операция успешно выполнена", "success")
    return redirect(url_for("parts.index"))
