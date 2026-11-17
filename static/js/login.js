
import {
    auth,
    signInWithEmailAndPassword
} from "./firebase.js";

const form = document.getElementById("loginForm");
const button = document.getElementById("loginButton");
const errorMessage = document.getElementById("errorMessage");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    errorMessage.style.display = "none";
    button.disabled = true;
    button.textContent = "Выполняется вход...";

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    try {
        console.log("Шаг 1: Проверка Firebase");

        const result = await signInWithEmailAndPassword(
            auth,
            email,
            password
        );

        console.log("Шаг 2: Firebase принял пользователя");
        console.log("UID:", result.user.uid);

        const token = await result.user.getIdToken();

        console.log("Шаг 3: Отправка токена Flask");

        const response = await fetch("/auth/session", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await response.json();

        console.log("Ответ Flask:", response.status, data);

        if (!response.ok) {
            throw new Error(data.error || "Ошибка Flask");
        }

        window.location.href = "/";

    } catch (error) {
        console.error("ПОЛНАЯ ОШИБКА:", error);

        errorMessage.textContent =
            `${error.code || "Ошибка"}: ${error.message}`;

        errorMessage.style.display = "block";

        button.disabled = false;
        button.textContent = "Войти в систему";
    }
});
