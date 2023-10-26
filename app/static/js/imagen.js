document.addEventListener("DOMContentLoaded", function () {
    // Obtén todas las imágenes con la clase "imagen-click"
    const imagenes = document.querySelectorAll(".imagen-click");

    // Agrega un evento de clic a cada imagen
    imagenes.forEach(function (imagen) {
        imagen.addEventListener("click", function () {
            // Crea un div para la capa de fondo
            const fondo = document.createElement("div");
            fondo.className = "imagen-fondo";
            fondo.addEventListener("click", function () {
                // Al hacer clic en el fondo, cierra la imagen ampliada
                fondo.style.display = "none";
            });

            // Crea una imagen ampliada
            const imagenAmpliada = document.createElement("img");
            imagenAmpliada.src = imagen.src;
            imagenAmpliada.className = "imagen-ampliada";

            // Agrega la imagen ampliada al fondo
            fondo.appendChild(imagenAmpliada);

            // Agrega el fondo a la página
            document.body.appendChild(fondo);

            // Muestra la imagen ampliada
            fondo.style.display = "block";
        });
    });
});