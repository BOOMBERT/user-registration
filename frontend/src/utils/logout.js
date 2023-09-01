import { removeCookie } from "./cookies.js";

const logoutButton = document.getElementById('logout-button');

logoutButton.addEventListener("click", () => {
    removeCookie();
    window.location.href = "/";
})
