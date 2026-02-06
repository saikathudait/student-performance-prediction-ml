document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("register-form");
    if (!form) {
        return;
    }

    const errorBox = document.getElementById("auth-errors");
    const nameInput = document.getElementById("id_full_name");
    const emailInput = document.getElementById("id_email");
    const userInput = document.getElementById("id_username");
    const pass1 = document.getElementById("id_password1");
    const pass2 = document.getElementById("id_password2");

    form.addEventListener("submit", (event) => {
        const errors = [];
        const minLength = 8;

        if (nameInput && !nameInput.value.trim()) {
            errors.push("Full name is required.");
        }
        if (emailInput && !emailInput.value.trim()) {
            errors.push("Email is required.");
        }
        if (userInput && !userInput.value.trim()) {
            errors.push("Username is required.");
        }
        if (pass1 && pass1.value.length < minLength) {
            errors.push(`Password must be at least ${minLength} characters.`);
        }
        if (pass1 && pass2 && pass1.value !== pass2.value) {
            errors.push("Passwords do not match.");
        }

        if (errors.length) {
            event.preventDefault();
            if (errorBox) {
                errorBox.textContent = errors[0];
            }
        }
    });
});
