import { getCookie } from "./cookies.js";


export function checkAccessToken() {
    const authToken = getCookie("accessToken");

    if (!authToken) {
        window.location.href = "/";
    }
}

export async function correctUrl() {
    const authToken = getCookie("accessToken");

    if (authToken && window.location.pathname === "/") {
        window.location.href = "/users/me";
    } else if (authToken === undefined && window.location.pathname === "/users/me/") {
        window.location.href = "/"
    }
}
