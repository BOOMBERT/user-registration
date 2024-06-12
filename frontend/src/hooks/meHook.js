import { baseApiUrl } from "./config.js";
import { getCookie, removeCookies } from "../utils/cookies.js";
import { checkAccessToken } from "../utils/authorizationCheck.js";
import { meResponseValidation, refreshAccessTokenResponseValidation } from "../validations/responseValidation.js";
import { isTokenExpired } from "../utils/authorizationCheck.js"


const meRequestUrl = `${baseApiUrl}/users/me`;

async function meSendRequest() {
    try {
        const meResponse = await fetch(meRequestUrl, {
            method: "GET",
            headers: {
                "Accept": "application/json",
                "Authorization": `Bearer ${getCookie("accessToken")}`
            }
        })
        meResponseValidation(meResponse);
        return meResponse;

    } catch (error) {
        removeCookies();
        console.error(`Internal Server Error, ${error}`);
        alert("Server error");
        checkAccessToken();
    }
}

let refreshAccessTokenRequestUrl = `${baseApiUrl}/users/refresh` 

async function refreshAccessTokenSendRequest() {
    try {
        refreshAccessTokenRequestUrl += `?refresh_token=${getCookie("refreshToken")}`;
        
        const refreshAccessTokenResponse = await fetch(refreshAccessTokenRequestUrl, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        })
        return refreshAccessTokenResponseValidation(refreshAccessTokenResponse);

    } catch (error) {
        removeCookies();
        console.error(`Internal Server Error, ${error}`);
        alert("Server error");
        checkAccessToken();
    }
}

if (isTokenExpired(getCookie("accessToken"))) {
    if (await refreshAccessTokenSendRequest()) {
        meSendRequest();
    }
} else {
    meSendRequest();
}
