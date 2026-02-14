
document.getElementById('loginForm').addEventListener('submit', function(event) {
    const password = document.getElementById('password').value.trim();
    const confirmar_password = document.getElementById('confirm-password').value.trim();
    const errorMessage = document.getElementById('error-message');

    if (password !== confirmar_password) {
        errorMessage.textContent = 'Las contraseñas no coinciden.';
        errorMessage.style.display = 'block';
        event.preventDefault(); // Evita que el formulario se envíe
    } else {
        errorMessage.style.display = 'none'; // Oculta el mensaje de error si las contraseñas coinciden
    }
});