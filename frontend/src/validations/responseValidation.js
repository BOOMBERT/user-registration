import { clearFormInputData } from "../utils/clearForms.js";


const registerEmailErrorLabel = document.getElementById('register-email-error-label');
const registerPasswordErrorLabel = document.getElementById('register-password-error-label');

const registerEmailInput = document.getElementById('register-email');
const registerPasswordInput = document.getElementById('register-password');
const registerPasswordCheckbox = document.getElementById('register-password-checkbox');

export async function registerResponseValidation(registerResponse) {
    if (registerResponse.status === 201) {
        alert("Successfully registered");
        console.log("Successfully registered");
        clearFormInputData(registerEmailInput, registerPasswordInput, registerPasswordCheckbox);
    } else {
        const responseData = await registerResponse.json();
        const responseDataMessage = await responseData.detail.msg;
        const responseDataLocation = await responseData.detail.loc[1];

        if (responseDataLocation === "email") {
            registerEmailErrorLabel.textContent = responseDataMessage;
        } else if (responseDataLocation === "password") {
            registerPasswordErrorLabel = responseDataMessage;
        }
        console.error(responseDataMessage);
    }

    return registerResponse;
}

const loginEmailPasswordError = document.getElementById('login-email-password-error');

const loginEmailInput = document.getElementById('login-email');
const loginPasswordInput = document.getElementById('login-password');
const loginPasswordCheckbox = document.getElementById('login-password-checkbox');

export async function loginResponseValidation(loginResponse) {
    if (loginResponse.status === 200) {
        console.log("Successfully logged in");
        clearFormInputData(loginEmailInput, loginPasswordInput, loginPasswordCheckbox);
        
        return true;
    } else {
        const responseData = await loginResponse.json();
        const responseDataMessage = await responseData.detail.msg;

        loginEmailPasswordError.textContent = responseDataMessage;
        
        console.error(responseDataMessage);
        return false;
    }
}
