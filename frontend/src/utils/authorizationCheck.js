import { getCookie } from "./cookies.js";


export function checkAccessToken() {
    const authToken = getCookie("accessToken");

    if (!authToken) {
        window.location.href = "/frontend/public/index.html";
    }
}
