
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore, auth

from config import Config


# Определяем путь к ключу Firebase
BASE_DIR = Path(__file__).resolve().parent.parent

credentials_path = BASE_DIR / Config.FIREBASE_CREDENTIALS


# Проверяем наличие файла ключа
if not credentials_path.exists():
    raise FileNotFoundError(
        f"Не найден ключ Firebase: {credentials_path}"
    )


# Инициализируем Firebase
try:
    firebase_app = firebase_admin.get_app()
except ValueError:
    firebase_credentials = credentials.Certificate(
        str(credentials_path)
    )

    firebase_app = firebase_admin.initialize_app(
        firebase_credentials
    )


# Подключаем Firestore
db = firestore.client(app=firebase_app)

# Модуль Firebase Authentication
firebase_auth = auth
