// NO @odoo-module, script legacy que se ejecuta al cargar
(function () {
    "use strict";

    function applyInitialTheme(btn) {
        const saved = window.localStorage.getItem("rigging_dark_mode");
        const isDark = saved === "1";

        if (isDark) {
            document.body.classList.add("rigging-dark-mode");
        } else {
            document.body.classList.remove("rigging-dark-mode");
        }

        btn.textContent = isDark ? "☀️" : "🌙";
    }

    function addThemeToggle() {
        const navbar = document.querySelector(".o_main_navbar");
        if (!navbar) {
            // todavía no existe la navbar
            return false;
        }

        // evitar duplicados
        if (navbar.querySelector(".rigging-theme-toggle")) {
            return true;
        }

        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "btn btn-link rigging-theme-toggle";
        btn.title = "Toggle dark / light mode";

        // estado inicial
        applyInitialTheme(btn);

        btn.addEventListener("click", function () {
            const isDark = document.body.classList.toggle("rigging-dark-mode");
            window.localStorage.setItem("rigging_dark_mode", isDark ? "1" : "0");
            btn.textContent = isDark ? "☀️" : "🌙";
            console.log("Dark mode?", isDark);
        });

        navbar.appendChild(btn);
        return true;
    }

    function startThemeSwitcher() {
        // primer intento
        if (addThemeToggle()) {
            return;
        }

        // reintentar cada 1s hasta que exista la navbar
        const intervalId = setInterval(function () {
            if (addThemeToggle()) {
                clearInterval(intervalId);
            }
        }, 1000);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", startThemeSwitcher);
    } else {
        startThemeSwitcher();
    }
})();