// Cargar usuarios al iniciar
async function loadUsers() {
    try {
        const response = await fetch('http://localhost:3000/users');
        if (!response.ok) throw new Error('Error cargando usuarios');
        
        const users = await response.json();
        const select = document.getElementById('userName');
        
        select.innerHTML = users.map(user => 
            `<option value="${user.nombre}">${user.nombre}</option>`
        ).join('');
    } catch (error) {
        console.error('Error:', error);
        alert('Error al cargar usuarios');
    }
}

// Mostrar formulario al seleccionar una película
document.querySelectorAll('.movie-card').forEach(card => {
    card.addEventListener('click', () => {
        const titulo = card.dataset.titulo;
        document.getElementById('selectedMovie').textContent = titulo;
        document.getElementById('votingForm').style.display = 'block';
    });
});

// Enviar voto
document.getElementById('voteForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const titulo = document.getElementById('selectedMovie').textContent;
    const userName = document.getElementById('userName').value;
    const rating = document.getElementById('rating').value;

    if (!titulo || !userName || !rating) {
        alert('Por favor, completa todos los campos.');
        return;
    }

    try {
        const response = await fetch('http://localhost:3000/votaciones', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ titulo, userName, rating: parseInt(rating) }), // Convertir rating a número
        });

        if (!response.ok) throw new Error('Error al enviar la votación');

        alert('Votación enviada exitosamente');
        document.getElementById('votingForm').style.display = 'none';
    } catch (error) {
        console.error('Error:', error);
        alert('Error al enviar la votación');
    }
});

// Mostrar formulario al seleccionar una película
document.querySelectorAll('.movie-card').forEach(card => {
    card.addEventListener('click', () => {
        const titulo = card.dataset.titulo;
        const imagen = card.querySelector('img').src; // Obtener la URL de la imagen

        document.getElementById('selectedMovie').textContent = titulo;
        document.getElementById('selectedMovieImage').src = imagen; // Actualizar la imagen
        document.getElementById('votingForm').style.display = 'block';
    });
});

// Mostrar formulario al seleccionar una película
document.querySelectorAll('.movie-card').forEach(card => {
    card.addEventListener('click', () => {
        const titulo = card.dataset.titulo;
        const imagen = card.querySelector('img').src;

        document.getElementById('selectedMovie').textContent = titulo;
        document.getElementById('selectedMovieImage').src = imagen;
        document.getElementById('votingForm').style.display = 'block';

        // Desplazar la página al formulario
        document.getElementById('votingForm').scrollIntoView({ behavior: 'smooth' });
    });
});


// Inicialización
loadUsers();
