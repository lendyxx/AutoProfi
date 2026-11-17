
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for
)

from firebase_admin import auth
from app.firebase import db, firebase_app


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login")
def login():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@auth_bp.route("/session", methods=["POST"])
def create_session():
    authorization = request.headers.get("Authorization", "")

    if not authorization.startswith("Bearer "):
        return jsonify({
            "error": "Отсутствует токен авторизации"
        }), 401

    token = authorization.split(" ", 1)[1]

    try:
        decoded_token = auth.verify_id_token(
            token,
            app=firebase_app
        )

        uid = decoded_token["uid"]

        user_document = db.collection("users").document(uid).get()

        if not user_document.exists:
            return jsonify({
                "error": "Пользователь не зарегистрирован в системе"
            }), 403

        user_data = user_document.to_dict()

        if user_data.get("active") is not True:
            return jsonify({
                "error": "Учётная запись отключена"
            }), 403

        role = user_data.get("role")

        allowed_roles = [
            "admin",
            "receptionist",
            "mechanic",
            "storekeeper",
            "director"
        ]

        if role not in allowed_roles:
            return jsonify({
                "error": "Роль пользователя не настроена"
            }), 403

        session.clear()

        session["user_id"] = uid
        session["email"] = decoded_token.get("email", "")
        session["name"] = user_data.get("name", "")
        session["role"] = role

        return jsonify({
            "success": True,
            "role": role
        })

    except Exception:
        return jsonify({
            "error": "Не удалось проверить авторизацию"
        }), 401


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
