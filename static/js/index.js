document.addEventListener('DOMContentLoaded', loadUsers)

// Event Listeners
document.getElementById("userSelect").addEventListener("change", (e) => {
  if (e.target.value) loadRecommendations(e.target.value);
});

// Cargar usuarios al iniciar
async function loadUsers() {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/users");
    if (!response.ok) throw new Error("Error cargando usuarios");


    const data = await response.json();
    const users = data.users;

    const select = document.getElementById("userSelect");

    // Generar opciones para el select

    users.forEach(user => {
      
      const option = document.createElement('option'); 
      option.value = user.name; 
      option.text = user.name; 
      select.appendChild(option)

    });
  } catch (error) {
    console.error("Error:", error);
    alert("Error al cargar usuarios");
  }
}

// Cargar recomendaciones al seleccionar usuario
async function loadRecommendations(username) {
  const container = document.querySelector(".movie-grid");
  const loading = document.querySelector(".loading");

  try {
    loading.style.display = "block";
    container.innerHTML = "";

    const response = await fetch(
      `http://127.0.0.1:5000/api/recommendations?user=${encodeURIComponent(
        username
      )}`
    );
    if (!response.ok) throw new Error("Error en recomendaciones");

    const data = await response.json();

    if (data.movies && data.movies.length > 0) {
      const movies = data.movies;

      container.innerHTML = movies
        .map(
          (movie) => `
                <div class="movie-card">
                    <h3>${movie.title}</h3>
                    <p>${movie.description}</p>
                    <p>Categoría: ${movie.category}</p>
                </div>
            `
        )
        .join("");
    } else {
      container.innerHTML = `<p class="error">No se encontraron recomendaciones para este usuario.</p>`;
    }
  } catch (error) {
    console.error("Error:", error);
    container.innerHTML = `<p class="error">${error.message}</p>`;
  } finally {
    loading.style.display = "none";
  }
}
