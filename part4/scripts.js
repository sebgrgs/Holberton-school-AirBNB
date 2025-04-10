document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message') || createErrorElement();

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            try {
                await loginUser(email, password);
            } catch (error) {
                showError(errorMessage, error.message || 'An error occurred during login');
            }
        });
    }
    checkAuthentication();
});

async function loginUser(email, password) {
    hideError();
    
    const submitButton = document.querySelector('button[type="submit"]');
    if (submitButton) {
        const originalText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Logging in...';
        
        setTimeout(() => {
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }, 3000);
    }
    
    const response = await fetch('http://localhost:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    
    if (response.ok) {
        const data = await response.json();
        
        const expiryDate = new Date();
        expiryDate.setTime(expiryDate.getTime() + (24 * 60 * 60 * 1000));
        document.cookie = `token=${data.access_token}; path=/; expires=${expiryDate.toUTCString()}; SameSite=Strict`;
        
        window.location.href = 'index.html';
    } else {
        const errorData = await response.json().catch(() => ({ message: response.statusText }));
        throw new Error(errorData.message || 'Login failed. Please check your credentials.');
    }
}

function createErrorElement() {
    const errorElement = document.createElement('div');
    errorElement.id = 'error-message';
    errorElement.className = 'error-message';
    errorElement.style.color = 'red';
    errorElement.style.marginTop = '10px';
    errorElement.style.display = 'none';
    
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.parentNode.insertBefore(errorElement, loginForm);
    }
    
    return errorElement;
}

function showError(element, message) {
    if (element) {
        element.textContent = message;
        element.style.display = 'block';
    } else {
        alert(message);
    }
}

function hideError() {
    const errorMessage = document.getElementById('error-message');
    if (errorMessage) {
        errorMessage.style.display = 'none';
    }
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');
    
    // Get placeId from URL if we're on a place details page
    const placeId = getPlaceIdFromURL();
    
    if (addReviewSection) {
        if (!token) {
            addReviewSection.style.display = 'none';
        } else {
            addReviewSection.style.display = 'block';
            
            // Only fetch place details if we have both a token and a placeId
            if (placeId) {
                fetchPlaceDetails(token, placeId);
            }
        }
    }

    // Only modify loginLink if it exists
    if (loginLink) {
        if (!token) {
            loginLink.textContent = 'Login';
            loginLink.href = 'login.html';
        } else {
            loginLink.textContent = 'Logout';
            loginLink.href = '#';
            loginLink.onclick = function(e) {
                e.preventDefault();
                document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
                window.location.href = 'login.html';
            };
        }
    }
    
    // Check if we're on the places listing page before fetching places
    const placesList = document.getElementById('places-list');
    if (placesList) {
        fetchPlaces(token);
    }
}

function getCookie(name) {
    // Function to get a cookie value by its name
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

async function fetchPlaces(token) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/places/', {
            method: 'GET',
            headers: {
                'Authorization': token ? `Bearer ${token}` : '',
                'Content-Type': 'application/json'
            }
        });
        if (response.ok) {
            const data = await response.json();
            allPlaces = data; // Store all places in global variable
            displayPlaces(data); // Display all places initially
            setupPriceFilter(); // Set up the price filter
        } else {
            display.error('Failed to fetch places:', response.statusText);
        }
    } catch (error) {
        display.error('Error fetching places:', error);
    }
}

let allPlaces = []; // Global variable to store all places

function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;
    
    // Add event listener for the price filter
    priceFilter.addEventListener('change', function() {
        const maxPrice = this.value ? parseInt(this.value) : Infinity;
        filterPlacesByPrice(maxPrice);
    });
}

function filterPlacesByPrice(maxPrice) {
    if (!allPlaces || allPlaces.length === 0) return;
    
    // If maxPrice is not set (All Prices selected), show all places
    if (maxPrice === Infinity) {
        displayPlaces(allPlaces);
        return;
    }
    
    // Filter places based on the selected maximum price
    const filteredPlaces = allPlaces.filter(place => {
        // Assuming the price is stored in place.price_by_night or place.price
        const price = place.price_by_night || place.price || 0;
        return price <= maxPrice;
    });
    
    // Display the filtered places
    displayPlaces(filteredPlaces);
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
    // Clear the current content
    placesList.innerHTML = '';
    
    // If no places to display
    if (!places || places.length === 0) {
        placesList.innerHTML = '<p>No places match your criteria.</p>';
        return;
    }
    
    // Iterate over the places data
    places.forEach(place => {
        const placeElement = document.createElement('div');
        placeElement.className = 'place-card';
        
        // Use the correct property names based on your API response
        const title = place.name || place.title || 'Unnamed Place';
        const price = place.price_by_night || place.price || 0;
        const id = place.id || '1';
        
        placeElement.innerHTML = `
            <h3>${title}</h3>
            <p>$${price} per night</p>
            <a href="place.html?id=${id}" class="details-button">View Details</a>
        `;
        
        placesList.appendChild(placeElement);
    });
}

function getPlaceIdFromURL() {
    // Extract the place ID from window.location.search
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Authorization': token ? `Bearer ${token}` : '',
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            displayPlaceDetails(data);
            
            // After displaying place details, fetch and display reviews
            fetchPlaceReviews(token, placeId);
        } else {
            console.error('Failed to fetch place details:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

function displayPlaceDetails(place) {
    // Update place title
    const placeTitle = document.getElementById('place-title');
    if (placeTitle) {
        placeTitle.textContent = place.title || 'Unnamed Place';
    }
    
    // Update host name
    const hostName = document.getElementById('host-name');
    if (hostName && place.owner) {
        hostName.textContent = `${place.owner.first_name} ${place.owner.last_name}`;
    }
    
    // Update price
    const placePrice = document.getElementById('place-price');
    if (placePrice) {
        placePrice.textContent = place.price || 0;
    }
    
    // Update description
    const placeDescription = document.getElementById('place-description');
    if (placeDescription) {
        placeDescription.textContent = place.description || 'No description available.';
    }
    
    // Update amenities list
    const amenitiesList = document.getElementById('amenities-list');
    if (amenitiesList) {
        amenitiesList.innerHTML = '';
        
        const amenities = place.amenities || [];
        if (amenities.length > 0) {
            amenities.forEach(amenity => {
                const amenityItem = document.createElement('li');
                amenityItem.textContent = amenity.name || 'Unnamed Amenity';
                amenitiesList.appendChild(amenityItem);
            });
        } else {
            const noAmenitiesItem = document.createElement('li');
            noAmenitiesItem.textContent = 'No amenities available.';
            noAmenitiesItem.className = 'no-amenities';
            amenitiesList.appendChild(noAmenitiesItem);
        }
    }
}

async function fetchPlaceReviews(token, placeId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, {
            method: 'GET',
            headers: {
                'Authorization': token ? `Bearer ${token}` : '',
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            displayReviews(data);
        } else {
            console.error('Failed to fetch reviews:', response.statusText);
            displayReviews([]);  // Show empty reviews
        }
    } catch (error) {
        console.error('Error fetching reviews:', error);
        displayReviews([]);  // Show empty reviews
    }
}

function displayReviews(reviews) {
    const reviewList = document.getElementById('review-list');
    if (!reviewList) return;
    
    // Clear the current content
    reviewList.innerHTML = '';
    
    // If no reviews to display
    if (!reviews || reviews.length === 0) {
        reviewList.innerHTML = '<p>No reviews yet for this place.</p>';
        return;
    }
    
    // Iterate over the reviews data
    reviews.forEach(review => {
        const reviewElement = document.createElement('div');
        reviewElement.className = 'review-card';
        
        // Convert numeric rating to stars
        const ratingStars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
        
        // Get user name or fallback to anonymous if user details are missing
        let reviewerName = 'Anonymous User';
        if (review.user && review.user.first_name && review.user.last_name) {
            reviewerName = `${review.user.first_name} ${review.user.last_name}`;
        }
        
        reviewElement.innerHTML = `
            <div class="rating">${ratingStars}</div>
            <p>${review.text}</p>
            <div class="reviewer">Posted by ${reviewerName}</div>
        `;
        
        reviewList.appendChild(reviewElement);
    });
}
