
import {
    auth,
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    updateProfile
} from "./firebase.js";

const form = document.getElementById("loginForm");
const button = document.getElementById("loginButton");
const errorMessage = document.getElementById("errorMessage");

const nameField = document.getElementById("nameField");
const nameInput = document.getElementById("name");
const passwordInput = document.getElementById("password");
const passwordConfirmField = document.getElementById("passwordConfirmField");
const passwordConfirmInput = document.getElementById("passwordConfirm");

const modeSwitch = document.getElementById("modeSwitch");
const modeDescription = document.getElementById("modeDescription");
const formTitle = document.getElementById("formTitle");

const passwordHint = document.getElementById("passwordHint");
const passwordConfirmHint = document.getElementById("passwordConfirmHint");

let currentMode = "login";

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = "block";
}

function setMode(mode) {
    currentMode = mode;

    errorMessage.style.display = "none";

    const isRegister = mode === "register";

    nameField.style.display = isRegister ? "block" : "none";
    passwordConfirmField.style.display = isRegister ? "block" : "none";

    nameInput.required = isRegister;
    passwordConfirmInput.required = isRegister;

    passwordInput.minLength = isRegister ? 6 : 1;

    formTitle.textContent = isRegister
        ? "Создание аккаунта"
        : "Вход в систему";

    modeDescription.textContent = isRegister
        ? "Уже есть аккаунт?"
        : "Впервые на сайте?";

    modeSwitch.textContent = isRegister
        ? "Войти"
        : "Зарегистрироваться";

    button.innerHTML = isRegister
        ? '<i class="bi bi-person-plus me-2"></i>Зарегистрироваться'
        : '<i class="bi bi-box-arrow-in-right me-2"></i>Войти в систему';

    passwordInput.autocomplete = isRegister
        ? "new-password"
        : "current-password";

    updatePasswordHints();
}

function updatePasswordHints() {
    const length = passwordInput.value.length;
    const isRegister = currentMode === "register";

    if (!isRegister) {
        passwordHint.textContent = "Введите пароль от аккаунта";
        passwordHint.className = "password-hint";
        return;
    }

    if (length === 0) {
        passwordHint.textContent = "Минимум 6 символов";
        passwordHint.className = "password-hint";
    } else if (length < 6) {
        passwordHint.textContent = `Осталось символов: ${6 - length}`;
        passwordHint.className = "password-hint invalid";
    } else {
        passwordHint.textContent = `✓ Длина пароля подходит (${length} символов)`;
        passwordHint.className = "password-hint valid";
    }

    if (!passwordConfirmInput.value) {
        passwordConfirmHint.textContent = "Повторите пароль для проверки";
        passwordConfirmHint.className = "password-hint";
    } else if (passwordInput.value === passwordConfirmInput.value) {
        passwordConfirmHint.textContent = "✓ Пароли совпадают";
        passwordConfirmHint.className = "password-hint valid";
    } else {
        passwordConfirmHint.textContent = "Пароли не совпадают";
        passwordConfirmHint.className = "password-hint invalid";
    }
}

passwordInput.addEventListener("input", updatePasswordHints);
passwordConfirmInput.addEventListener("input", updatePasswordHints);

modeSwitch.addEventListener("click", () => {
    setMode(currentMode === "login" ? "register" : "login");
});

function getFirebaseError(error) {
    const errors = {
        "auth/email-already-in-use": "Этот email уже зарегистрирован.",
        "auth/invalid-email": "Некорректный email.",
        "auth/weak-password": "Пароль должен содержать минимум 6 символов.",
        "auth/invalid-credential": "Неверный email или пароль.",
        "auth/user-disabled": "Учётная запись отключена.",
        "auth/too-many-requests": "Слишком много попыток. Попробуйте позже.",
        "auth/network-request-failed": "Проверьте подключение к интернету."
    };

    return errors[error.code] || error.message || "Неизвестная ошибка.";
}

async function sendTokenToServer(endpoint, token) {
    const response = await fetch(endpoint, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        }
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || `Ошибка сервера: ${response.status}`);
    }

    return data;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    errorMessage.style.display = "none";

    const email = document.getElementById("email").value.trim();
    const password = passwordInput.value;

    if (currentMode === "register") {
        const name = nameInput.value.trim();

        if (name.length < 2) {
            showError("Введите имя: минимум 2 символа.");
            return;
        }

        if (password.length < 6) {
            showError("Пароль должен содержать минимум 6 символов.");
            passwordInput.focus();
            return;
        }

        if (password !== passwordConfirmInput.value) {
            showError("Пароли не совпадают.");
            passwordConfirmInput.focus();
            return;
        }
    }

    button.disabled = true;

    try {
        let user;

        if (currentMode === "register") {
            button.textContent = "Создание аккаунта...";

            const name = nameInput.value.trim();

            const result = await createUserWithEmailAndPassword(
                auth,
                email,
                password
            );

            user = result.user;

            await updateProfile(user, {
                displayName: name
            });

            const token = await user.getIdToken(true);

            button.textContent = "Сохранение профиля...";

            await sendTokenToServer("/auth/register", token);

        } else {
            button.textContent = "Выполняется вход...";

            const result = await signInWithEmailAndPassword(
                auth,
                email,
                password
            );

            user = result.user;
        }

        const token = await user.getIdToken(true);

        button.textContent = "Проверка доступа...";

        await sendTokenToServer("/auth/session", token);

        window.location.href = "/";

    } catch (error) {
        console.error("Ошибка авторизации:", error);

        showError(
            error.code
                ? getFirebaseError(error)
                : error.message
        );

    } finally {
        button.disabled = false;
        setMode(currentMode);
    }
});

setMode("login");
