// scripts.js

document.addEventListener('DOMContentLoaded', () => {
  // Vérifie l'authentification à chaque chargement de la page
  const token = checkAuthentication();

  // Si le formulaire de connexion existe, ajoute un écouteur d'événements
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
          event.preventDefault();
          const email = document.getElementById('email').value;
          const password = document.getElementById('password').value;
          await loginUser(email, password);
      });
  }

  // Vérification de l'authentification pour charger les lieux
  checkAuthentication();

  // Filtrage des lieux par prix
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
      priceFilter.addEventListener('change', (event) => {
          const selectedPrice = parseInt(event.target.value);
          const allPlaces = document.querySelectorAll('.place-card');

          allPlaces.forEach(place => {
              const priceText = place.querySelector('p:nth-of-type(2)').textContent;
              const price = parseFloat(priceText.replace(/[^0-9.]/g, ''));
              place.style.display = (isNaN(selectedPrice) || price <= selectedPrice) ? 'block' : 'none';
          });
      });
  }

  // Gestion des révisions (pour une page de lieu spécifique)
  const reviewForm = document.getElementById('review-form');
  if (reviewForm) {
      const placeId = getPlaceIdFromURL();
      reviewForm.addEventListener('submit', async (event) => {
          event.preventDefault();
          const reviewText = document.getElementById('review-text').value;
          await submitReview(token, placeId, reviewText);
      });
  }
});

// Fonction pour l'authentification (connexion)
async function loginUser(email, password) {
  try {
      const response = await fetch('https://your-api-url/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
      });

      if (response.ok) {
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = 'index.html';
      } else {
          alert('Connexion échouée : ' + response.statusText);
      }
  } catch (error) {
      console.error('Erreur lors de la connexion :', error);
      alert('Erreur réseau. Veuillez réessayer.');
  }
}

// Fonction pour vérifier l'authentification
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (!token) {
      if (loginLink) loginLink.style.display = 'block';
  } else {
      if (loginLink) loginLink.style.display = 'none';
      fetchPlaces(token);
  }
  return token;
}

// Fonction pour obtenir la valeur d'un cookie
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  return parts.length === 2 ? parts.pop().split(';').shift() : null;
}

// Fonction pour récupérer l'ID du lieu à partir de l'URL
function getPlaceIdFromURL() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('id');
}

// Fonction pour récupérer les lieux
async function fetchPlaces(token) {
  try {
      const response = await fetch('https://your-api-url/places', {
          method: 'GET',
          headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
          }
      });

      if (response.ok) {
          const data = await response.json();
          displayPlaces(data);
      } else {
          console.error('Erreur de récupération des lieux :', response.statusText);
          alert('Impossible de récupérer les lieux.');
      }
  } catch (error) {
      console.error('Erreur réseau :', error);
      alert('Erreur de connexion au serveur.');
  }
}

// Fonction pour afficher les lieux
function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  if (!placesList) return;
  placesList.innerHTML = ''; // On vide d'abord l'ancien contenu

  places.forEach(place => {
      const placeDiv = document.createElement('div');
      placeDiv.classList.add('place-card');
      placeDiv.innerHTML = `
          <h3>${place.name}</h3>
          <p><strong>Description:</strong> ${place.description}</p>
          <p><strong>Price:</strong> $${place.price}</p>
          <p><strong>Host:</strong> ${place.host}</p>
      `;
      placesList.appendChild(placeDiv);
  });
}

// Fonction pour soumettre la révision
async function submitReview(token, placeId, reviewText) {
  try {
      const response = await fetch(`https://your-api-url/places/${placeId}/reviews`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ review: reviewText })
      });

      if (response.ok) {
          const data = await response.json();
          alert('Review submitted successfully');
      } else {
          console.error('Failed to submit review:', response.statusText);
          alert('Failed to submit review. Please try again.');
      }
  } catch (error) {
      console.error('Error while submitting review:', error);
      alert('An error occurred while submitting your review. Please try again.');
  }
}
