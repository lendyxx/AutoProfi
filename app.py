
from flask import Flask, render_template, session, redirect, url_for, request, abort

from config import Config

from app.routes.requests import requests_bp
from app.routes.clients import clients_bp
from app.routes.vehicles import vehicles_bp
from app.routes.work_catalog import work_catalog_bp
from app.routes.parts import parts_bp
from app.routes.employees import employees_bp
from app.routes.reports import reports_bp
from app.routes.auth import auth_bp


# Создание приложения
app = Flask(__name__)
app.config.from_object(Config)


# Регистрация разделов
app.register_blueprint(requests_bp)
app.register_blueprint(clients_bp)
app.register_blueprint(vehicles_bp)
app.register_blueprint(work_catalog_bp)
app.register_blueprint(parts_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(auth_bp)


# Доступ по ролям
ROLE_ACCESS = {
    "admin": {
        "requests",
        "clients",
        "vehicles",
        "work_catalog",
        "parts",
        "employees",
        "reports"
    },

    "receptionist": {
        "requests",
        "clients",
        "vehicles"
    },

    "mechanic": {
        "requests",
        "work_catalog"
    },

    "storekeeper": {
        "parts"
    },

    "director": {
        "requests",
        "clients",
        "vehicles",
        "work_catalog",
        "parts",
        "employees",
        "reports"
    }
}


# Проверка авторизации и прав доступа
@app.before_request
def require_login():

    allowed_endpoints = {
        "auth.login",
        "auth.create_session",
        "auth.logout",
        "static"
    }

    endpoint = request.endpoint

    if endpoint is None:
        return None

    if endpoint in allowed_endpoints:
        return None

    # Проверка авторизации
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    # Проверка доступа к разделу
    if "." in endpoint:

        section = endpoint.split(".", 1)[0]
        role = session.get("role")

        if section in ROLE_ACCESS:
            if section not in ROLE_ACCESS.get(role, set()):
                abort(403)

    return None


# Страница запрета доступа
@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403


# Главная страница
@app.route("/")
def dashboard():

    stats = {
        "total_requests": 128,
        "in_progress": 18,
        "waiting": 7,
        "revenue": 485000
    }

    requests = [
        {
            "id": "1024",
            "client": "Александр Иванов",
            "car": "Toyota Camry",
            "date": "16.11.2026",
            "status": "В работе"
        }
    ]

    return render_template(
        "dashboard.html",
        stats=stats,
        requests=requests
    )


# Запуск сервера
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
