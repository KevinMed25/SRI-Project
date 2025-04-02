document.addEventListener("DOMContentLoaded", () => {
  loadUsers();
});

// Cargar usuarios al iniciar
async function loadUsers() {
  try {
    const response = await fetch("http://localhost:5000/api/users");
    if (!response.ok) throw new Error("Error cargando usuarios");

    const data = await response.json(); // Obtener el objeto completo
    const users = data.users; // Acceder al array "users"

    const select = document.getElementById("userName");

    // Generar opciones para el select
    select.innerHTML = users
      .map((user) => `<option value="${user.name}">${user.name}</option>`)
      .join("");
  } catch (error) {
    console.error("Error:", error);
    alert("Error al cargar usuarios");
  }
}

// Mostrar formulario al seleccionar una película
document.querySelectorAll(".movie-card").forEach((card) => {
  card.addEventListener("click", () => {
    const titulo = card.dataset.titulo;
    document.getElementById("selectedMovie").textContent = titulo;
    document.getElementById("votingForm").style.display = "block";
  });
});

// Enviar voto
document.getElementById("voteForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const movie = document.getElementById("selectedMovie").textContent;
  const username = document.getElementById("userName").value;
  const rating = document.getElementById("rating").value;

  if (!movie || !username || !rating) {
    alert("Por favor, completa todos los campos.");
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/api/save-ratings", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ movie, username, rating: parseInt(rating) }), // Convertir rating a número
    });

    if (!response.ok) throw new Error("Error al enviar la votación");

    alert("Votación enviada exitosamente");
    document.getElementById("votingForm").style.display = "none";
  } catch (error) {
    console.error("Error:", error);
    alert("Error al enviar la votación");
  }
});

// Mostrar formulario al seleccionar una película
document.querySelectorAll(".movie-card").forEach((card) => {
  card.addEventListener("click", () => {
    const titulo = card.dataset.titulo;
    const imagen = card.querySelector("img").src; // Obtener la URL de la imagen

    document.getElementById("selectedMovie").textContent = titulo;
    document.getElementById("selectedMovieImage").src = imagen; // Actualizar la imagen
    document.getElementById("votingForm").style.display = "block";
  });
});

// Mostrar formulario al seleccionar una película
document.querySelectorAll(".movie-card").forEach((card) => {
  card.addEventListener("click", () => {
    const titulo = card.dataset.titulo;
    const imagen = card.querySelector("img").src;

    document.getElementById("selectedMovie").textContent = titulo;
    document.getElementById("selectedMovieImage").src = imagen;
    document.getElementById("votingForm").style.display = "block";

    document
      .getElementById("votingForm")
      .scrollIntoView({ behavior: "smooth" });
  });
});
