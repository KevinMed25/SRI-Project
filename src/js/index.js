
// Cargar usuarios al iniciar
async function loadUsers() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/users');
        if (!response.ok) throw new Error('Error cargando usuarios');
        
        const data = await response.json();
        const users = data.users;

        const select = document.getElementById('userSelect');
        
        // Generar opciones para el select
        select.innerHTML = users.map(user => 
            `<option value="${user.name}">${user.name}</option>`
        ).join('');
    } catch (error) {
        console.error('Error:', error);
        alert('Error al cargar usuarios');
    }
}


// Cargar recomendaciones al seleccionar usuario
async function loadRecommendations(username) {
    const container = document.querySelector('.movie-grid');
    const loading = document.querySelector('.loading');
    
    try {
        loading.style.display = 'block';
        container.innerHTML = '';
        
        const response = await fetch(`http://localhost:3000/recommendations?user=${encodeURIComponent(username)}`);
        if (!response.ok) throw new Error('Error en recomendaciones');
        
        const data = await response.json();
        
        if (data.length > 0 && data[0].peliculas) {
            const peliculas = data[0].peliculas;
            
            container.innerHTML = peliculas.map(movie => `
                <div class="movie-card">
                    <h3>${movie.titulo}</h3>
                    <p>${movie.descripcion}</p>
                    <p>Categoría: ${movie.categoria}</p>
                </div>
            `).join('');
        } else {
            container.innerHTML = `<p class="error">No se encontraron recomendaciones para este usuario.</p>`;
        }
        
    } catch (error) {
        console.error('Error:', error);
        container.innerHTML = `<p class="error">${error.message}</p>`;
    } finally {
        loading.style.display = 'none';
    }
}

// Event Listeners
document.getElementById('userSelect').addEventListener('change', (e) => {
    if (e.target.value) loadRecommendations(e.target.value);
});

// Inicialización
loadUsers();