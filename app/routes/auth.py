
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
    current_app
)

from firebase_admin import auth, firestore
from app.firebase import db, firebase_app


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# Страница входа
@auth_bp.route("/login")
def login():

    if session.get("user_id"):
        return redirect(url_for("dashboard"))

    return render_template("login.html")


# Регистрация нового пользователя
@auth_bp.route("/register", methods=["POST"])
def register():

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
        email = decoded_token.get("email", "")

        user_record = auth.get_user(
            uid,
            app=firebase_app
        )

        name = user_record.display_name or "Новый пользователь"

        user_ref = db.collection("users").document(uid)
        user_doc = user_ref.get()

        # Не перезаписываем существующую учётную запись
        if user_doc.exists:
            return jsonify({
                "error": "Пользователь уже зарегистрирован"
            }), 409

        user_ref.set({
            "uid": uid,
            "name": name,
            "email": email,
            "role": "user",
            "active": True,
            "created_at": firestore.SERVER_TIMESTAMP
        })

        return jsonify({
            "success": True,
            "message": "Регистрация прошла успешно"
        }), 201

    except Exception:
        current_app.logger.exception(
            "Ошибка регистрации пользователя"
        )

        return jsonify({
            "error": "Не удалось зарегистрировать пользователя"
        }), 500


# Создание Flask-сессии после входа
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

        user_document = (
            db.collection("users")
            .document(uid)
            .get()
        )

        if not user_document.exists:
            return jsonify({
                "error": "Профиль пользователя не найден"
            }), 403

        user_data = user_document.to_dict()

        if user_data.get("active") is not True:
            return jsonify({
                "error": "Учётная запись отключена"
            }), 403

        role = user_data.get("role")

        allowed_roles = {
            "admin",
            "receptionist",
            "mechanic",
            "storekeeper",
            "director",
            "user"
        }

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
        current_app.logger.exception(
            "Ошибка создания пользовательской сессии"
        )

        return jsonify({
            "error": "Не удалось проверить авторизацию"
        }), 401


# Выход из системы
@auth_bp.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return redirect(url_for("auth.login"))
