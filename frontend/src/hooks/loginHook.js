import { baseUrl } from "./config.js";
import { loginParametersValidation } from "../validations/dataValidation.js";
import { loginResponseValidation } from "../validations/responseValidation.js";


const requestUrl = `${baseUrl}/users/login`;
const submitLoginButton = document.getElementById("login-submit-button");

submitLoginButton.addEventListener("click", (event) => {
    event.preventDefault();

    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    if (loginParametersValidation(email, password)) {
        loginRequest(email, password);
    }
})

async function loginRequest(email, password) {
    try {
        const loginData = `grant_type=&username=${email}&password=${password}&scope=&client_id=&client_secret=`;
    
        const loginResponse = await fetch(requestUrl, {
            method: "POST",
            body: loginData,
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
