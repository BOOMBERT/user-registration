import { baseApiUrl } from "./config.js";
import { registerParametersValidation } from "../validations/dataValidation.js";
import { registerResponseValidation } from "../validations/responseValidation.js";


const registerRequestUrl = `${baseApiUrl}/users/register`;
const submitRegisterButton = document.getElementById("register-submit-button");

submitRegisterButton.addEventListener("click", (event) => {
    event.preventDefault();

    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;

    if (registerParametersValidation(email, password)) {
        registerRequest(email, password);
    }
});

async function registerRequest(email, password) {

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
