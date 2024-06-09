const registerEmailError = document.getElementById('register-email-error');
const registerPasswordError = document.getElementById('register-password-error');
const invalidEmailMessage = "Invalid email address";

export function registerArgumentsValidation(email, password) {
    let isValid = true;

    if (!emailValidation(email)) {
        registerEmailError.textContent = invalidEmailMessage;
        console.error(invalidEmailMessage);
        isValid = false;
    } else {
        registerEmailError.textContent = "";
    }

    const passwordCheck = passwordValidation(password);
    if (passwordCheck !== true) {
        registerPasswordError.textContent = passwordCheck;
        console.error(passwordCheck);
        isValid = false;
    } else {
        registerPasswordError.textContent = "";
    }

    return isValid;
}

// const loginEmailPasswordError = document.getElementById('login-email-password-error');
// const invalidEmailOrPasswordMessage = "Email address or password is incorrect"

// export function loginParametersValidation(email, password) {
//     if (!emailValidation(email) || passwordValidation(password) !== true) {
//         loginEmailPasswordError.textContent = invalidEmailOrPasswordMessage;
//         console.error(invalidEmailOrPasswordMessage);
//         return false;
//     } else {
//         loginEmailPasswordError.textContent = "";
//         return true;
//     }
// }

function emailValidation(email) {
    return email.match(
      /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
}

function passwordValidation(password) {
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
