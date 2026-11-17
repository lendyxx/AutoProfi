
from app.firebase import db

# Создаём тестовый документ
test_ref = db.collection("system").document("connection_test")

test_ref.set({
    "status": "connected",
    "application": "АвтоПрофи-Сервис"
})

# Читаем документ
document = test_ref.get()

if document.exists:
    print("Firestore работает!")
    print(document.to_dict())
else:
    print("Документ не найден")
