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

  if (window.location.pathname.includes('place.html')) {
    const placeId = getPlaceIdFromURL();
    if (placeId) {
      displayPlaceDetails(placeId);
    }
  }
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
    return [];
  }
}

async function fetchPlaceDetails(token, placeId) {
  // Make a GET request to fetch place details
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      } 
    });
    if (!response.ok) {
      throw new Error('Erreur lors de la récupération des détails du lieu ' + response.statusText);
    }
    const data = await response.json();
    return data;
  }
  catch (error) {
    console.error('Erreur:', error);
    return [];
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
        // placesContainer.appendChild(card);

        card.addEventListener('submit', (event) => {
          event.preventDefault();
          window.location.href = `place.html?id=${place.id}`;
        })
        placesContainer.appendChild(card);
      });
      populatePriceFilter();
  } else {
    placesContainer.innerHTML = "<p>Aucun lieu trouvé.</p>";
  }
}

async function displayPlaceDetails(placeId) {
  // Clear the current content of the place details section
  const placeDetails = document.getElementById('place-details');
  const reviewButton = document.querySelector('.add-a-review-button');

  if(!placeDetails) {
    console.error('Détails du lieu introuvables.');
    return;
  }
  placeDetails.innerHTML = '';
  // Create elements to display the place details (name, description, price, amenities and reviews)
  
  try {
    
    const token = getCookie('token');
    const isAuthenticated = !!token;

    if (reviewButton) {
      if (isAuthenticated) {
        reviewButton.style.display = 'block';
        reviewButton.addEventListener('click', () => {
          window.location.href = `add_review.html?id=${placeId}`;
        });
      } else {
        reviewButton.style.display = 'none';
      }
    }

    const placeData = await fetchPlaceDetails(token, placeId);

    if (placeData) {
      const titleElement = document.querySelector('.title-place');
      if (titleElement) {
        titleElement.textContent = placeData.title;
      }

      const host = document.createElement('p');
      host.textContent = `Host: ${placeData.owner.first_name} ${placeData.owner.last_name}`;

      const price = document.createElement('p');
      price.textContent = `${placeData.price}$ per night`;

      const description = document.createElement('p');
      description.textContent = placeData.description;

      const amenitiesList = document.createElement('p');
      const amenitiesText = Array.isArray(placeData.amenities) ? placeData.amenities.map(amenity => amenity.name).join(', ') : 'None listed';
      amenitiesList.textContent = `Amenities: ${amenitiesText}`;

      placeDetails.appendChild(host);
      placeDetails.appendChild(price);
      placeDetails.appendChild(description);
      placeDetails.appendChild(amenitiesList);

      // displayReviews(place.reviews);
    } else {
      placeDetails.innerHTML = "<p>Unable to load place details.</p>";
    }
  } catch (error) {
    console.error('Error displaying place details:', error);
    placeDetails.innerHTML = "<p>Unable to load place details.</p>";
  }
}

//Price filter
function populatePriceFilter() {
  const priceFilter = document.getElementById('price-filter');
  if (!priceFilter) return;

  priceFilter.innerHTML = '';

  const options = [
    { value: '0', text: 'All' },
    { value: '10', text: '10' },
    { value: '50', text: '50' },
    { value: '100', text: '100' },
  ];

  options.forEach(option => {
    const optionElement = document.createElement('option');
    optionElement.value = option.value;
    optionElement.textContent = option.text;
    priceFilter.appendChild(optionElement);
  });

priceFilter.addEventListener('change', (event) => {
  const maxPrice = parseInt(event.target.value);
  const placeCards = document.querySelectorAll('.places-card');

  placeCards.forEach(card => {
    const priceText = card.querySelector('p').textContent;
    const price = parseInt(priceText.match(/\d+/)[0]);

    if (maxPrice === 0 || price <= maxPrice) {
      card.style.display = 'flex';
    } else {
      card.style.display = 'none';
    }
  });
});
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

/*----------- INDEX -----------*/

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.querySelector('.login-button');

  if (loginLink) {
    if (!token) {
      loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        // Fetch places data if the user is authenticated
        displayPlaces(token);
    }
  }
  
}
function getCookie(name) {
  const v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return v ? v[2] : null;
}
