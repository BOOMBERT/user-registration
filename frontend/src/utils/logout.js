import { removeCookie } from "./cookies.js";
import { checkAccessToken } from "./authorizationCheck.js";

const logoutButton = document.getElementById('logout-button');

logoutButton.addEventListener("click", () => {
    removeCookie();
    checkAccessToken();
})
