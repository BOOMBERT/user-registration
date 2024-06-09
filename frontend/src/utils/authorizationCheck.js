import { getCookie } from "./cookies.js";


export function checkAccessToken() {
    const authToken = getCookie("accessToken");

    if (!authToken) {
        window.location.href = "/";
    }
}

export function correctUrl() {
    const authToken = getCookie("accessToken");

    if (authToken && window.location.pathname === "/") {
        window.location.href = "/users/me";
    }
}
