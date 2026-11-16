
import csv
import io

from flask import (
    Blueprint,
    render_template,
    request,
    make_response
)

from app.routes.requests import requests_data
from app.routes.parts import parts_data
from app.routes.work_catalog import work_data

reports_bp = Blueprint(
    "reports",
    __name__,
    url_prefix="/reports"
)


@reports_bp.route("/")
def index():
    total_requests = len(requests_data)

    completed = sum(
        1 for item in requests_data
        if item["status"] in ["Готово", "Выдано", "Закрыто"]
    )

    active = sum(
        1 for item in requests_data
        if item["status"] in [
            "Новая",
            "На диагностике",
            "Ожидает согласования",
            "Согласована",
            "В работе"
        ]
    )

    cancelled = sum(
        1 for item in requests_data
        if item["status"] == "Отменена"
    )

    status_stats = {}

    for item in requests_data:
        status = item["status"]
        status_stats[status] = status_stats.get(status, 0) + 1

    low_stock = [
        part for part in parts_data
        if part["quantity"] <= part["min_quantity"]
    ]

    total_stock_value = sum(
        part["quantity"] * part["purchase_price"]
        for part in parts_data
    )

    popular_works = sorted(
        work_data,
        key=lambda item: item["price"],
        reverse=True
    )[:5]

    # Демонстрационная выручка.
    # Позже будет рассчитываться по фактически закрытым заявкам.
    revenue = 485000

    return render_template(
        "reports.html",
        total_requests=total_requests,
        completed=completed,
        active=active,
        cancelled=cancelled,
        status_stats=status_stats,
        low_stock=low_stock,
        total_stock_value=total_stock_value,
        popular_works=popular_works,
        revenue=revenue
    )


@reports_bp.route("/export")
def export():
    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")

    writer.writerow([
        "Номер заявки",
        "Клиент",
        "Автомобиль",
        "Дата",
        "Статус"
    ])

    for item in requests_data:
        writer.writerow([
            item["id"],
            item["client"],
            item["car"],
            item["date"],
            item["status"]
        ])

    response = make_response("\ufeff" + output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = (
        "attachment; filename=autoprofi_requests.csv"
    )

    return response
