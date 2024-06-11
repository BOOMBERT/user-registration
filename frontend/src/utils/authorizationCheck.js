import { getCookie, removeCookies } from "./cookies.js";


export function checkAccessToken() {
    const authToken = getCookie("accessToken");

    if (!authToken || isTokenExpired(authToken)) {
        window.location.href = "/";
    }
}

export function correctUrl() {
    const accessToken = getCookie("accessToken");

    if (accessToken && window.location.pathname === "/") {
        window.location.href = "/users/me";
    } else if (!accessToken && window.location.pathname === "/users/me/") {
        removeCookies();
        window.location.href = "/"
    }
}

export function isTokenExpired(token) {
    try {
        const expiry = (JSON.parse(atob(token.split('.')[1]))).exp;
        return (Math.floor((new Date()).getTime() / 1000)) >= expiry;
        
    } catch (error) {
        console.error('Invalid token:', error);
        return true;
    }
}
