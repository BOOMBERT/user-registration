const registerEmailErrorLabel = document.getElementById('register-email-error-label');
const registerPasswordErrorLabel = document.getElementById('register-password-error-label');
const invalidEmailMessage = "Invalid email address";

export function registerParametersValidation(email, password) {
    let isValid = true;

    if (!validateEmail(email)) {
        registerEmailErrorLabel.textContent = invalidEmailMessage;
        console.error(invalidEmailMessage);
        isValid = false;
    } else {
        registerEmailErrorLabel.textContent = "";
    }

    const validPassword = validatePassword(password);
    if (validPassword !== true) {
        registerPasswordErrorLabel.textContent = validPassword;
        console.error(validPassword);
        isValid = false;
    } else {
        registerPasswordErrorLabel.textContent = "";
    }

    return isValid;
}

const loginEmailPasswordError = document.getElementById('login-email-password-error');
const invalidEmailOrPasswordMessage = "Email address or password is incorrect"

export function loginParametersValidation(email, password) {
    if (!validateEmail(email) || validatePassword(password) !== true) {
        loginEmailPasswordError.textContent = invalidEmailOrPasswordMessage;
        console.error(invalidEmailOrPasswordMessage);
        return false;
    } else {
        loginEmailPasswordError.textContent = "";
        return true;
    }
}

function validateEmail(email) {
    return email.match(
      /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
}

function validatePassword(password) {
    if (password.length < 8) {
        return "Password should contain at least 8 characters";
    }
    if (password.length > 256) {
        return "Password cannot exceed 256 characters";
    }
    if (!password.match(/[a-z]/)) {
        return "Password must include at least 1 lowercase character";
    }
    if (!password.match(/[A-Z]/)) {
        return "Password must include at least 1 uppercase character";
    }
    if (!password.match(/\d/)) {
        return "Password must include at least 1 digit";
    }

    return true;
}
