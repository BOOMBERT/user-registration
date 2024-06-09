import { baseApiUrl } from "./config.js";
import { registerArgumentsValidation } from "../validations/dataValidation.js";
import { registerResponseValidation } from "../validations/responseValidation.js";


const registerRequestUrl = `${baseApiUrl}/users/register`;
const RegisterButton = document.getElementById('register-button');

RegisterButton.addEventListener("click", (event) => {
    event.preventDefault();
    const email = document.getElementById('register-email-input').value;
    const password = document.getElementById('register-password-input').value;

    if (registerArgumentsValidation(email, password)) {
        registerSendRequest(email, password);
    }
});

async function registerSendRequest(email, password) {
    try {
        const registerResponse = await fetch(registerRequestUrl, {
            method: "POST",
            body: JSON.stringify({
                "email": email,
                "password": password
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        registerResponseValidation(registerResponse);
        return registerResponse;

    } catch(error) {
        console.error(`Internal Server Error, ${error}`);
        alert("Server error");
    }
}
