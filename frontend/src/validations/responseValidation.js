import { clearFormData } from "../utils/clearForms.js";


const registerEmailInput = document.getElementById('register-email-input');
const registerPasswordInput = document.getElementById('register-password-input');
const registerPasswordCheckbox = document.getElementById('register-password-checkbox');
const registerEmailError = document.getElementById('register-email-error');
const registerPasswordError = document.getElementById('register-password-error');

export async function registerResponseValidation(registerResponse) {
    if (registerResponse.status === 201) {
        alert("Successfully registered");
        console.log("Successfully registered");
        clearFormData(registerEmailInput, registerPasswordInput, registerPasswordCheckbox);
        return true;
    } else {
        const responseErrorData = await registerResponse.json();
        const responseErrorMessage = await responseErrorData.detail.msg;
        const responseErrorLocation = await responseErrorData.detail.loc[1];
        console.error(responseErrorMessage);

        if (responseErrorLocation === "email") {
            registerEmailError.textContent = responseErrorMessage;
        } else if (responseErrorLocation === "password") {
            registerPasswordError.textContent = responseErrorMessage;
        }
        return false;
    }
}

// const loginEmailPasswordError = document.getElementById('login-email-password-error');

// const loginEmailInput = document.getElementById('login-email');
// const loginPasswordInput = document.getElementById('login-password');
// const loginPasswordCheckbox = document.getElementById('login-password-checkbox');

// export async function loginResponseValidation(loginResponse) {
//     if (loginResponse.status === 200) {
//         console.log("Successfully logged in");
//         clearFormInputData(loginEmailInput, loginPasswordInput, loginPasswordCheckbox);
        
//         return true;
//     } else {
//         const responseData = await loginResponse.json();
//         const responseDataMessage = await responseData.detail.msg;

//         loginEmailPasswordError.textContent = responseDataMessage;
        
//         console.error(responseDataMessage);
//         return false;
//     }
// }
