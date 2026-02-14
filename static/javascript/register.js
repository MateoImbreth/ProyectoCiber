
document.getElementById('registerForm').addEventListener('submit', function(event) {
    const password = document.getElementById('password').value.trim();
    const confirmar_contrasena = document.getElementById('confirm-password').value.trim();
    const email = document.getElementById('email').value.trim();
    const errorMessage = document.getElementById('error-message');

    if (password !== confirmar_contrasena) {
        errorMessage.textContent = 'Las contraseñas no coinciden.';
        errorMessage.style.display = 'block';
        event.preventDefault();
    } else if (!isValidGmail(email)) {
        errorMessage.textContent = 'Por favor, ingrese un correo electrónico de Gmail válido.';
        errorMessage.style.display = 'block';
        event.preventDefault();
    } else {
        errorMessage.style.display = 'none';
    }
});

function isValidGmail(email) {
    const gmailRegex = /^[\w-\.]+@gmail\.com$/;
    return gmailRegex.test(email);
}