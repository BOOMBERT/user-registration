import { removeCookies } from "./cookies.js";
import { checkAccessToken } from "./authorizationCheck.js";

const userId = document.getElementById('user-id-space');
const userEmail = document.getElementById('user-email-space');
const logoutButton = document.getElementById('logout-button');

logoutButton.addEventListener("click", () => {
    userId.textContent = "null";
    userEmail.textContent = "null";
    removeCookies();
    checkAccessToken();
});

window.addEventListener("unload", function () {
    userId.textContent = "null";
    userEmail.textContent = "null";
});
