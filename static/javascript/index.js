document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // <-- ESTO evita que la página se recargue

    const formData = new FormData(this); // Captura los datos del formulario automáticamente
    const errorMessage = document.getElementById('error-message');
    
    // Validación previa local (contraseñas)
    const password = document.getElementById('password').value.trim();
    const confirm = document.getElementById('confirm-password').value.trim();

    if (password !== confirm) {
        errorMessage.textContent = 'Las contraseñas no coinciden.';
        errorMessage.style.display = 'block';
        return; // Detenemos aquí
    }

    try {
        // Enviamos los datos al servidor usando fetch
        const response = await fetch('/login', {
            method: 'POST',
            body: formData // Enviamos como FormData porque el backend usa Form(...)
        });

        const data = await response.json();

        if (response.ok) {
            // Si el login es exitoso, redirigimos manualmente
            window.location.href = data.redirect; 
        } else {
            // Si hay un error (400 o 401), lo mostramos sin recargar
            errorMessage.textContent = data.detail || 'Ocurrió un error inesperado';
            errorMessage.style.display = 'block';
        }
    } catch (error) {
        console.error("Error en la petición:", error);
        errorMessage.textContent = 'Error de conexión con el servidor.';
        errorMessage.style.display = 'block';
    }
});