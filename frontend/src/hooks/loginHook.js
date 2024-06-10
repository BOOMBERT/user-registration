import { baseApiUrl } from "./config.js";
import { loginArgumentsValidation } from "../validations/dataValidation.js";
import { loginResponseValidation } from "../validations/responseValidation.js";


const requestUrl = `${baseApiUrl}/users/login`;
const loginButton = document.getElementById('login-button');

loginButton.addEventListener("click", (event) => {
    event.preventDefault();

    const email = document.getElementById('login-email-input').value;
    const password = document.getElementById('login-password-input').value;
    if (loginArgumentsValidation(email, password)) {
        loginSendRequest(email, password);
    }
});

async function loginSendRequest(email, password) {
    try {
        const loginBodyData = `grant_type=&username=${email}&password=${password}&scope=&client_id=&client_secret=`;
        
        const loginResponse = await fetch(requestUrl, {
            method: "POST",
            body: loginBodyData,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
        if (await loginResponseValidation(loginResponse)) {
            const responseData = await loginResponse.json();
            const accessToken = await responseData.access_token;
            
            document.cookie = `accessToken=${accessToken}; path=/;`;
            window.location.href = "/users/me";
        }
        return loginResponse;

    } catch(error) {
        console.error(`Internal Server Error, ${error}`);
        alert("Server error");
    }
}
