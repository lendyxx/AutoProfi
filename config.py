
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv(
        "FLASK_SECRET_KEY",
        "temporary-development-key"
    )

    FIREBASE_CREDENTIALS = os.getenv(
        "FIREBASE_CREDENTIALS",
        "firebase/serviceAccountKey.json"
    )
