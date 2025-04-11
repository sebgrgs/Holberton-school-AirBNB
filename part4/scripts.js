document.addEventListener('DOMContentLoaded', () => {
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();
    const loginForm = document.getElementById('login-form');
    const reviewForm = document.getElementById('review-form');
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

    if (reviewForm && token && placeId) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const reviewText = document.getElementById('review-text').value.trim();
            const rating = parseInt(document.getElementById('review-rating').value);            
            if (!reviewText || isNaN(rating)) {
                alert('Please provide both review text and rating.');
                return;
            }
            
            const tokenPayload = parseJwt(token);
            const userId = tokenPayload.sub || tokenPayload.id;

            if (!userId) {
                alert('User ID not found. Please log in again.');
                return;
            }
            
            try {
                const response = await fetch('http://localhost:5000/api/v1/reviews', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        place_id: placeId,
                        text: reviewText,
                        rating: rating,
                        user_id: userId.id
                    })
                });
                
                if (response.ok) {
                    alert('Review submitted successfully!');
                    document.getElementById('review-text').value = '';
                    document.getElementById('review-rating').selectedIndex = 0;
                    fetchPlaceReviews(token, placeId);
                } else {
                    const errorData = await response.json();
                    alert(`Failed to submit review: ${errorData.error || errorData.message || 'Unknown error'}`);
                }
            } catch (error) {
                alert('Error submitting review: ' + error.message);
            }
        });
    }
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
        // Store user_id in localStorage or a cookie
        localStorage.setItem('user_id', data.user_id);
        
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
    const placeId = getPlaceIdFromURL();
    
    // Redirect unauthenticated users to index page if on place details page
    if (!token && document.getElementById('place-details')) {
        window.location.href = 'index.html';
        return null;
    }
    
    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
        if (token && placeId) {
            fetchPlaceDetails(token, placeId);
        }
    }
    
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
    
    const placesList = document.getElementById('places-list');
    if (placesList) {
        fetchPlaces(token);
    }
    
    return token;
}

function getCookie(name) {
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
            allPlaces = data;
            displayPlaces(data);
            setupPriceFilter();
        } else {
            console.error('Failed to fetch places:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

let allPlaces = [];

function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;
    
    priceFilter.addEventListener('change', function() {
        const maxPrice = this.value ? parseInt(this.value) : Infinity;
        filterPlacesByPrice(maxPrice);
    });
}

function filterPlacesByPrice(maxPrice) {
    if (!allPlaces || allPlaces.length === 0) return;
    
    if (maxPrice === Infinity) {
        displayPlaces(allPlaces);
        return;
    }
    
    const filteredPlaces = allPlaces.filter(place => {
        const price = place.price_by_night || place.price || 0;
        return price <= maxPrice;
    });
    
    displayPlaces(filteredPlaces);
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
    placesList.innerHTML = '';
    
    if (!places || places.length === 0) {
        placesList.innerHTML = '<p>No places match your criteria.</p>';
        return;
    }
    
    places.forEach(place => {
        const placeElement = document.createElement('div');
        placeElement.className = 'place-card';
        
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
            fetchPlaceReviews(token, placeId);
        } else {
            console.error('Failed to fetch place details:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

function displayPlaceDetails(place) {
    const placeTitle = document.getElementById('place-title');
    if (placeTitle) {
        placeTitle.textContent = place.title || 'Unnamed Place';
    }
    
    const hostName = document.getElementById('host-name');
    if (hostName && place.owner) {
        hostName.textContent = `${place.owner.first_name} ${place.owner.last_name}`;
    }
    
    const placePrice = document.getElementById('place-price');
    if (placePrice) {
        placePrice.textContent = place.price || 0;
    }
    
    const placeDescription = document.getElementById('place-description');
    if (placeDescription) {
        placeDescription.textContent = place.description || 'No description available.';
    }
    
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
            const reviews = await response.json();
            
            // Fetch user details for each review
            const reviewsWithUserDetails = await Promise.all(reviews.map(async (review) => {
                try {
                    const userResponse = await fetch(`http://localhost:5000/api/v1/users/${review.user_id}`, {
                        method: 'GET',
                        headers: {
                            'Authorization': token ? `Bearer ${token}` : '',
                            'Content-Type': 'application/json'
                        }
                    });
                    
                    if (userResponse.ok) {
                        const userData = await userResponse.json();
                        // Add user details to the review object
                        review.user = {
                            first_name: userData.first_name,
                            last_name: userData.last_name
                        };
                    }
                } catch (error) {
                    console.error(`Error fetching user details for review ${review.id}:`, error);
                }
                return review;
            }));
            
            displayReviews(reviewsWithUserDetails);
        } else {
            console.error('Failed to fetch reviews:', response.statusText);
            displayReviews([]);
        }
    } catch (error) {
        console.error('Error fetching reviews:', error);
        displayReviews([]);
    }
}

function displayReviews(reviews) {
    const reviewList = document.getElementById('review-list');
    if (!reviewList) return;
    
    reviewList.innerHTML = '';
    
    if (!reviews || reviews.length === 0) {
        reviewList.innerHTML = '<p>No reviews yet for this place.</p>';
        return;
    }
    
    reviews.forEach(review => {
        const reviewElement = document.createElement('div');
        reviewElement.className = 'review-card';
        
        const ratingStars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
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

function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (e) {
        console.error('Error parsing JWT token:', e);
        return {};
    }
}