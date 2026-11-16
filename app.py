
from flask import Flask, render_template

from app.routes.requests import requests_bp
from app.routes.clients import clients_bp
from app.routes.vehicles import vehicles_bp
from app.routes.work_catalog import work_catalog_bp
from app.routes.parts import parts_bp
from app.routes.employees import employees_bp
from app.routes.reports import reports_bp

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"

app.register_blueprint(requests_bp)
app.register_blueprint(clients_bp)
app.register_blueprint(vehicles_bp)
app.register_blueprint(work_catalog_bp)
app.register_blueprint(parts_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(reports_bp)


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


if __name__ == "__main__":
    app.run(debug=True)
