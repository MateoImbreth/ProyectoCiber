# Proyecto de Registro de Usuarios

## Qué hace el proyecto

Este proyecto es una aplicación web diseñada para facilitar el registro de nuevos usuarios. La aplicación permite a los usuarios ingresar su información personal, incluyendo nombre, correo electrónico, contraseña y grupo, a través de un formulario de registro. El proyecto también incluye validación de entrada, específicamente para asegurar que el correo electrónico proporcionado sea una dirección de Gmail válida, y que la contraseña y su confirmación coincidan.

Además, el proyecto implementa medidas de seguridad importantes:

* **Hasheo de contraseñas:** Las contraseñas ingresadas por los usuarios se hashean antes de ser almacenadas en la base de datos, lo que protege la información confidencial en caso de una brecha de seguridad.
* **Tokens de autenticación:** Se utilizan tokens para gestionar las sesiones de los usuarios después de que se han autenticado correctamente, lo que mejora la seguridad y la experiencia del usuario al permitir el acceso a partes protegidas de la aplicación sin necesidad de volver a ingresar las credenciales.

## Por qué el proyecto es útil

Este proyecto es útil por varias razones:

* **Gestión de usuarios:** Proporciona una base para la gestión de usuarios en una aplicación web, incluyendo el registro, la autenticación y la autorización.
* **Seguridad:** Implementa prácticas de seguridad recomendadas, como el hasheo de contraseñas y el uso de tokens, para proteger la información de los usuarios.
* **Validación de datos:** Valida la entrada del usuario para asegurar que los datos ingresados sean correctos y completos, lo que mejora la calidad de los datos y la experiencia del usuario.
* **Personalizable:** El proyecto puede ser adaptado y extendido para satisfacer las necesidades específicas de diferentes aplicaciones web.

## Cómo pueden comenzar los usuarios con el proyecto

Para comenzar a utilizar este proyecto, los desarrolladores pueden seguir estos pasos:

1.  **Clonar el repositorio:** Clonar el repositorio de Git que contiene el código del proyecto en su máquina local.
2.  **Configurar la base de datos:** Configurar una base de datos PostgreSQL y actualizar la variable `DATABASE_URL` en el código con las credenciales de la base de datos.
3.  **Instalar dependencias:** Instalar las dependencias de Python necesarias, estas se encuentran en requeriments.txt.
4.  **Configurar variables de entorno:** Configurar las variables de entorno `SECRET_KEY` y `DATABASE_URL` para proteger la información confidencial.
5.  **Ejecutar la aplicación:** Ejecutar la aplicación FastAPI.
6.  **Acceder a la aplicación:** Acceder a la aplicación a través de un navegador web.

## Quién mantiene y contribuye con el proyecto

Este proyecto es mantenido y contribuido por:

* **Mateo Imbreth y Glendy Jaimes:** Desarrolladores principales del proyecto.
