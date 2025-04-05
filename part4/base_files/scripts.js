/*----------- LOGIN -----------*/

document.addEventListener('DOMContentLoaded', () => {
  const loginLink = document.querySelector('.login-button');
  if (loginLink) {
    loginLink.addEventListener('click', () => {
      window.location.href = 'login.html';
    });
  }

  const loginForm = document.getElementById('login-form');
    if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(loginForm);
        const loginData = {
          email: formData.get('email'),
          password: formData.get('password')
        };
        console.log('Login data:', loginData);

        try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(loginData)
        });

        if (response.ok) {
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = 'index.html';
        } else {
          alert('Login failed: ' + response.statusText);
        }
      } catch (error) {
        console.error('Login failed:', error);
        alert('Login failed: ' + error.message);
      }
   });
  }
  checkAuthentication();

});


/*----------- PLACES -----------*/


async function fetchPlaces(token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });
    if (!response.ok) {
      throw new Error('Erreur lors de la récupération des lieux ' + response.statusText);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erreur:', error);
  }
}


async function displayPlaces(token) {
  const placesContainer = document.getElementById('places-list');
  if(!placesContainer) {
    console.error('Elément container des lieux est introuvable.');
    return;
  }
  placesContainer.innerHTML = '';

  const places = await fetchPlaces(token);

  if (places && Array.isArray(places)) {
    places.forEach(place => {
      const card = document.createElement('form');
      card.className = 'places-card';
      card.innerHTML = `
        <h2>${place.title}</h2>
        <p>${place.price} per night</p>
        <button type='submit' class='view-details-card-button'>View details</button>
        `;
        placesContainer.appendChild(card);
      });     
  } else {
    placesContainer.innerHTML = "<p>Aucun lieu trouvé.</p>";
  }
}

/*----------- INDEX -----------*/

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
      loginLink.style.display = 'block';
  } else {
      loginLink.style.display = 'none';
      // Fetch places data if the user is authenticated
      displayPlaces(token);
  }
}
function getCookie(name) {
  const v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return v ? v[2] : null;
}
