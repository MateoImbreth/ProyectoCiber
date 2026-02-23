document.getElementById('registerForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Detenemos la recarga de página
    
    const errorMessage = document.getElementById('error-message');
    const formData = new FormData(this); // Recoge nick_name, contrasena, grupo, email

    // 1. Validaciones locales (Frontend)
    const password = document.getElementById('password').value.trim();
    const confirmar_contrasena = document.getElementById('confirm-password').value.trim();
    const emailValue = document.getElementById('email').value.trim();

    if (password !== confirmar_contrasena) {
        errorMessage.textContent = 'Las contraseñas no coinciden.';
        errorMessage.style.display = 'block';
        return;
    } 
    
    if (!isValidGmail(emailValue)) {
        errorMessage.textContent = 'Por favor, ingrese un correo electrónico de Gmail válido.';
        errorMessage.style.display = 'block';
        return;
    }

    // 2. Envío al servidor (Fetch)
    try {
        const response = await fetch('/register', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            // Éxito: Redirigir al login (index)
            alert("¡Registro exitoso! Ahora puedes iniciar sesión.");
            window.location.href = data.redirect; 
        } else {
            // Error del servidor (Email o Nickname duplicado)
            errorMessage.textContent = data.detail; // El mensaje que viene del backend
            errorMessage.style.display = 'block';
        }

    } catch (error) {
        errorMessage.textContent = 'Error de conexión con el servidor.';
        errorMessage.style.display = 'block';
    }
});

function isValidGmail(email) {
    const gmailRegex = /^[\w-\.]+@gmail\.com$/;
    return gmailRegex.test(email);
}