export function clearFormData(inputEmail, inputPassword, checkbox) {
    inputEmail.value = "";
    inputPassword.value = "";

    if (inputPassword.type === "text") {
        inputPassword.type = "password";
        checkbox.checked = false;
    }
}