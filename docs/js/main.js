const LOCAL_HOSTNAMES = ["localhost", "127.0.0.1"];
let currentLocale = "en";

function isRunningLocally() {
    return LOCAL_HOSTNAMES.includes(window.location.hostname);
}

async function loadLocale(lang) {
    const response = await fetch(`locales/${lang}.json`);
    const strings = await response.json();

    document.querySelectorAll("[data-i18n]").forEach((el) => {
        const key = el.getAttribute("data-i18n");
        if (strings[key]) {
            el.textContent = strings[key];
        }
    });

    document.querySelectorAll("#lang-switch button").forEach((btn) => {
        btn.classList.toggle("active", btn.dataset.lang === lang);
    });

    currentLocale = lang;
    document.documentElement.lang = lang;
}

function setupLangSwitch() {
    document.querySelectorAll("#lang-switch button").forEach((btn) => {
        btn.addEventListener("click", () => loadLocale(btn.dataset.lang));
    });
}

function connectWebSocket() {
    const statusEl = document.getElementById("status");
    const socket = new WebSocket(`ws://${window.location.host}/ws`);

    socket.onopen = () => {
        statusEl.textContent = currentLocale === "es" ? "Conectado" : "Connected";
        statusEl.className = "connected";
    };

    socket.onclose = () => {
        statusEl.textContent = currentLocale === "es" ? "Desconectado" : "Disconnected";
        statusEl.className = "disconnected";
    };

    socket.onmessage = (event) => {
        const state = JSON.parse(event.data);
        document.getElementById("val-gesture").textContent = state.gesture ?? "-";
        document.getElementById("val-confidence").textContent = state.confidence ?? "-";
        document.getElementById("val-elbow").textContent = state.servos?.elbow ?? "-";
        document.getElementById("val-gripper").textContent = state.servos?.gripper ?? "-";
    };
}

function init() {
    setupLangSwitch();

    const browserLang = navigator.language.startsWith("es") ? "es" : "en";
    loadLocale(browserLang);

    if (isRunningLocally()) {
        document.getElementById("viewer-live").style.display = "block";
        document.getElementById("viewer-unavailable").style.display = "none";
        connectWebSocket();
    } else {
        document.getElementById("viewer-live").style.display = "none";
        document.getElementById("viewer-unavailable").style.display = "block";
    }
}

init();