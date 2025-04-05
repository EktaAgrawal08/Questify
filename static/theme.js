document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    const sunIcon = "/static/icons/sun.png";
    const moonIcon = "/static/icons/moon.png";

    // Check saved theme
    let theme = localStorage.getItem("theme") || "light";
    applyTheme(theme);

    // Toggle theme on click
    themeToggle.addEventListener("click", function () {
        theme = theme === "dark" ? "light" : "dark";
        localStorage.setItem("theme", theme);
        applyTheme(theme);
    });

    function applyTheme(theme) {
        if (theme === "dark") {
            document.documentElement.classList.add("dark-mode");
            document.body.classList.add("dark-mode");
            themeIcon.src = moonIcon;
        } else {
            document.documentElement.classList.remove("dark-mode");
            document.body.classList.remove("dark-mode");
            themeIcon.src = sunIcon;
        }
    }
});
