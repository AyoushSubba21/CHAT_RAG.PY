function changeTheme(theme) {
    document.getElementById("theme-style").href = theme;
    localStorage.setItem("selectedTheme", theme);
}

window.onload = function() {
    const savedTheme = localStorage.getItem("selectedTheme");
    const select=document.querySelector("select");
    if (savedTheme) {
        document.getElementById("theme-style").href = savedTheme;
        select.value=savedTheme;
    }
}
