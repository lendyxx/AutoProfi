
from app.firebase import db, firebase_auth, firebase_app

email = "n.gurov123@gmail.com"

user = firebase_auth.get_user_by_email(email)
uid = user.uid

print("Проект:", firebase_app.project_id)
print("UID:", uid)

print("\n--- ПРОВЕРКА КОЛЛЕКЦИИ USERS ---")

users = db.collection("users").stream()

found = False

for document in users:
    print("Найден документ:", document.id)

    if document.id == uid:
        found = True
        print("Данные:", document.to_dict())

print("\nДокумент найден:", found)

print("\n--- ПРОВЕРКА ДОКУМЕНТА ПО UID ---")

document = db.collection("users").document(uid).get()

print("Существует:", document.exists)

if document.exists:
    print("Содержимое:", document.to_dict())
