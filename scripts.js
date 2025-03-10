// Función para agregar una nueva publicación
function addPost() {
    const content = document.getElementById("content").value;
    if (content.trim() === "") {
        alert("No puedes publicar un contenido vacío.");
        return;
    }

    // Crear el contenedor de la publicación
    const postContainer = document.createElement("div");
    postContainer.classList.add("post");

    // Crear el contenido de la publicación
    const postContent = document.createElement("p");
    postContent.textContent = content;

    // Añadir contenido a la publicación
    postContainer.appendChild(postContent);

    // Añadir la publicación al contenedor principal de publicaciones
    const postsSection = document.getElementById("posts");
    postsSection.prepend(postContainer);  // Prepend agrega al inicio de la lista

    // Limpiar el área de texto
    document.getElementById("content").value = "";
}

// Función para mostrar/ocultar la ventana de chat
function toggleChat() {
    const chatWindow = document.getElementById("chatWindow");
    chatWindow.classList.toggle("active");
}

// Función para enviar mensaje en el chat
function sendMessage() {
    const messageInput = document.querySelector("#chatWindow .chat-footer input");
    const messageContent = messageInput.value;

    if (messageContent.trim() === "") {
        alert("Escribe un mensaje antes de enviarlo.");
        return;
    }

    const chatBody = document.querySelector("#chatWindow .chat-body");

    // Crear el nuevo mensaje
    const newMessage = document.createElement("div");
    newMessage.classList.add("message");
    newMessage.innerHTML = `<p>${messageContent}</p>`;

    // Agregar el mensaje al chat
    chatBody.appendChild(newMessage);

    // Desplazar la vista hacia el último mensaje
    chatBody.scrollTop = chatBody.scrollHeight;

    // Limpiar el campo de mensaje
    messageInput.value = "";
}

// Añadir evento de envío en el chat
document.querySelector("#chatWindow .chat-footer button").addEventListener("click", sendMessage);

// Agregar funcionalidad para que el Enter envíe el mensaje
document.querySelector("#chatWindow .chat-footer input").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

// Cerrar sesión
function logout() {
    // Aquí iría la lógica para cerrar sesión (p.ej., borrar token o redirigir)
    alert("¡Has cerrado sesión!");
    window.location.href = "index.html";  // Redirigir a la página de inicio
}

// Función para actualizar la foto de perfil
function updateProfilePicture() {
    const fileInput = document.querySelector("#profilePictureInput");
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.querySelector(".profile-photo").src = e.target.result;
        };
        reader.readAsDataURL(file);
    } else {
        alert("Por favor selecciona una imagen.");
    }
}

// Mostrar el número de notificaciones no leídas en la barra de navegación
function updateNotificationCount() {
    const notificationCount = document.querySelector(".notification-count");
    const unreadNotifications = document.querySelectorAll(".notification.unread").length;
    
    notificationCount.textContent = unreadNotifications > 0 ? unreadNotifications : "";
}

// Llamar a la función para actualizar las notificaciones al cargar la página
updateNotificationCount();

// Aquí podrías agregar más funciones relacionadas con la interacción
