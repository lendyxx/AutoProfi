
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.routes.clients import clients_data

vehicles_bp = Blueprint(
    "vehicles",
    __name__,
    url_prefix="/vehicles"
)

vehicles_data = [
    {
        "id": 1,
        "client_id": 1,
        "brand": "Toyota",
        "model": "Camry",
        "year": 2018,
        "plate": "А123АА39",
        "vin": "JTNB11HK303012345"
    },
    {
        "id": 2,
        "client_id": 2,
        "brand": "BMW",
        "model": "3 Series",
        "year": 2020,
        "plate": "В456ВВ39",
        "vin": "WBA8E9G50GNU12345"
    },
    {
        "id": 3,
        "client_id": 3,
        "brand": "Volkswagen",
        "model": "Polo",
        "year": 2016,
        "plate": "С789СС39",
        "vin": "WVWZZZ6RZGY123456"
    }
]


@vehicles_bp.route("/")
def index():
    search = request.args.get("search", "").strip().lower()

    filtered = []

    for vehicle in vehicles_data:
        client = next(
            (c for c in clients_data if c["id"] == vehicle["client_id"]),
            None
        )

        vehicle_view = {
            **vehicle,
            "owner": client["name"] if client else "Клиент не найден"
        }

        searchable = [
            vehicle["brand"],
            vehicle["model"],
            vehicle["plate"],
            vehicle["vin"],
            vehicle_view["owner"]
        ]

        if not search or any(
            search in str(value).lower() for value in searchable
        ):
            filtered.append(vehicle_view)

    return render_template(
        "vehicles.html",
        vehicles=filtered,
        clients=clients_data,
        search=search
    )


@vehicles_bp.route("/create", methods=["POST"])
def create():
    client_id = request.form.get("client_id", type=int)
    brand = request.form.get("brand", "").strip()
    model = request.form.get("model", "").strip()
    year = request.form.get("year", type=int)
    plate = request.form.get("plate", "").strip().upper()
    vin = request.form.get("vin", "").strip().upper()

    client = next(
        (c for c in clients_data if c["id"] == client_id),
        None
    )

    if not all([client, brand, model, year, plate, vin]):
        flash("Заполните все обязательные поля", "danger")
        return redirect(url_for("vehicles.index"))

    if year < 1900 or year > 2026:
        flash("Укажите корректный год выпуска", "danger")
        return redirect(url_for("vehicles.index"))

    if any(v["plate"] == plate for v in vehicles_data):
        flash("Автомобиль с таким госномером уже существует", "danger")
        return redirect(url_for("vehicles.index"))

    if any(v["vin"] == vin for v in vehicles_data):
        flash("Автомобиль с таким VIN уже существует", "danger")
        return redirect(url_for("vehicles.index"))

    new_vehicle = {
        "id": max((v["id"] for v in vehicles_data), default=0) + 1,
        "client_id": client_id,
        "brand": brand,
        "model": model,
        "year": year,
        "plate": plate,
        "vin": vin
    }

    vehicles_data.append(new_vehicle)

    if not any(
        car == f"{brand} {model}" for car in client["cars"]
    ):
        client["cars"].append(f"{brand} {model}")

    flash("Автомобиль успешно добавлен", "success")
    return redirect(url_for("vehicles.index"))
