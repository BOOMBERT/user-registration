import { registerEmailLabel, registerPasswordLabel } from "./dataValidation.js";

const registerEmailInput = document.getElementById('register-email');
const registerPasswordInput = document.getElementById('register-password');

export async function registerResponseValidation(registerResponse) {
    if (registerResponse.status === 201) {
        alert("Succesfully registered");
        console.log("Succesfully registered");
        registerEmailInput.value = "";
        registerPasswordInput.value = "";
    } else {
        const responseData = await registerResponse.json();
        const responseDataMessage = await responseData.detail.msg;
        const responseDataLocation = await responseData.detail.loc[1];

        if (responseDataLocation === "email") {
            registerEmailLabel.textContent = responseDataMessage;
        } else if (responseDataLocation === "password") {
            registerPasswordLabel = responseDataMessage;
        }
        console.error(responseDataMessage);
    }

    return registerResponse;
}
