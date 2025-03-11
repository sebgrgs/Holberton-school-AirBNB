import unittest
from app import create_app
from app.services import facade
import bcrypt

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        print('\n' + '-'*50)  # Add separator between tests

    def test_create_user(self):
        print("\nTest: Creating user")
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 201)
        print(f"Response (status {response.status_code}): {response.json}")

        # Verify that the password is hashed
        user_id = response.json['id']
        user = facade.get_user(user_id)
        self.assertNotEqual(user.password, "password123")
        self.assertTrue(bcrypt.check_password_hash(user.password, "password123"))

        print("\nTest: Creating user with existing email")
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)
        print(f"Response (status {response.status_code}): {response.json}")

        print("\nTest: Getting all users")
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        print(f"Response (status {response.status_code}): {response.json}")

    def test_create_user_invalid_data(self):
        print("\nTest: Creating user with invalid data")
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        print(f"Response (status {response.status_code}): {response.json}")

    def test_get_all_users(self):
        print("\nTest: Getting all users")
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        print(f"Response (status {response.status_code}): {response.json}")
    
    def test_get_user_not_found(self):
        print("\nTest: Getting non-existent user")
        response = self.client.get('/api/v1/users/qsdqsqqds')
        self.assertEqual(response.status_code, 404)
        print(f"Response (status {response.status_code}): {response.json}")

    def test_create_and_get_user_and_update(self):
        print("\nTest: Create, Get, and Update user")
        
        print("\n1. Creating user...")
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bobby",
            "last_name": "aaaa", 
            "email": "Bobbye.aaaa@example.com"
        })
        self.assertEqual(response.status_code, 201)
        print(f"Response (status {response.status_code}): {response.json}")
        
        user_id = response.json['id']
        
        print("\n2. Getting user...")
        get_response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(get_response.status_code, 200)
        print(f"Response (status {get_response.status_code}): {get_response.json}")

        print("\n3. Updating user...")
        update_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "bbbbb",
            "last_name": "poaoaoa",
            "email": "aaaa@example.com"
        })
        self.assertEqual(update_response.status_code, 200)
        print(f"Response (status {update_response.status_code}): {update_response.json}")
        
        print("\n4. Verifying update...")
        verify_response = self.client.get(f'/api/v1/users/')
        self.assertEqual(verify_response.status_code, 200)
        print(f"Response (status {verify_response.status_code}): {verify_response.json}")

    def test_create_user_place_and_update(self):
        print("\nTest: Create User and Place and update")

        print("\n1. Creating user...")
        user_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "aaa@aaa.aa"
        }
        print(f"Request data: {user_data}")
        response1 = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response1.status_code, 201)
        print(f"Response (status {response1.status_code}): {response1.json}")
        
        user_id = response1.json['id']

        print("\n2. Creating place...")
        place_data = {
            "title": "My Place",
            "description": "A beautiful place",
            "price": 100.0,
            "latitude": 1.0,
            "longitude": 1.0,
            "owner_id": user_id,
            "amenities": []
        }
        print(f"Request data: {place_data}")
        response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response.status_code, 201)
        print(f"Response (status {response.status_code}): {response.json}")

        place_id = response.json['id']

        print("\n3. Getting place...")
        get_response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(get_response.status_code, 200)
        print(f"Response (status {get_response.status_code}): {get_response.json}")

        print("\n4. Updating place...")
        update_response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Updated My Place",
            "description": "updated A beautiful place",
            "price": 50.0,
            "latitude": 2.0,
            "longitude": 0.0,
            "owner_id": user_id,
            "amenities": []
        })
        self.assertEqual(update_response.status_code, 200)
        print(f"Response (status {update_response.status_code}): {update_response.json}")

    def test_get_all_places(self):
        print("\nTest: Getting all places")
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        print(f"Response (status {response.status_code}): {response.json}")
    
    def test_get_place_not_found(self):
        print("\nTest: Getting non-existent place")
        response = self.client.get('/api/v1/places/qsdqsqqds')
        self.assertEqual(response.status_code, 404)
        print(f"Response (status {response.status_code}): {response.json}")

    def test_create_and_get_user_and_update_invalid_data(self):
        print("\nTest: Create, Get, and Update user")
        
        print("\n1. Creating user...")
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bobby",
            "last_name": "aaaa", 
            "email": "Bobbye.aaaa@example.com"
        })
        self.assertEqual(response.status_code, 201)
        print(f"Response (status {response.status_code}): {response.json}")
        
        user_id = response.json['id']
        
        print("\n2. Getting user...")
        get_response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(get_response.status_code, 200)
        print(f"Response (status {get_response.status_code}): {get_response.json}")

        print("\n3. Updating user with invalid data...")
        update_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "bbbbb",
            "last_name": "poaoaoa",
            "email": "invalid-email"
        })
        self.assertEqual(update_response.status_code, 400)
        print(f"Response (status {update_response.status_code}): {update_response.json}")
        
        print("\n4. Verifying update...")
        verify_response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(verify_response.status_code, 200)
        print(f"Response (status {verify_response.status_code}): {verify_response.json}")

        
    def test_create_user_place_invalid_data(self):
        print("\nTest: Create User and Place with invalid data")

        print("\n1. Creating user...")
        user_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "aaa@aa.aa"
        }
        print(f"Request data: {user_data}")
        response1 = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response1.status_code, 201)
        print(f"Response (status {response1.status_code}): {response1.json}")
        
        user_id = response1.json['id']

        print("\n2. Creating place with invalid data...")
        place_data = {
            "title": "My Place",
            "description": "A beautiful place",
            "price": -1,
            "latitude": 1.0,
            "longitude": 1.0,
            "owner_id": user_id,
            "amenities": []
        }
        print(f"Request data: {place_data}")
        response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response.status_code, 400)
        print(f"Response (status {response.status_code}): {response.json}")
    

    def test_create_user_place_review_get_all_reviews(self):
            print("\nTest: Create User, Place, Review, and Get All Reviews")

            print("\n1. Creating user...")
            user_data = {
                "first_name": "Test",
                "last_name": "User",
                "email": "test.user@example.com"
            }
            print(f"Request data: {user_data}")
            response1 = self.client.post('/api/v1/users/', json=user_data)
            self.assertEqual(response1.status_code, 201)
            user_id = response1.json['id']

            print("\n2. Creating place...")
            place_data = {
                "title": "Test",
                "description": "Test description",
                "price": 100.0,
                "latitude": 1.0,
                "longitude": 1.0,
                "owner_id": user_id,
                "amenities": []
            }
            print(f"Request data: {place_data}")
            response2 = self.client.post('/api/v1/places/', json=place_data)
            self.assertEqual(response2.status_code, 201)
            place_id = response2.json['id']

            print("\n3. Creating review...")
            review_data = {
                "text": "Test review",
                "rating": 4,
                "user_id": user_id,
                "place_id": place_id
            }
            print(f"Request data: {review_data}")
            response3 = self.client.post('/api/v1/reviews/', json=review_data)
            self.assertEqual(response3.status_code, 201)

            print("\n4. Getting all reviews for the place...")
            get_response = self.client.get(f'/api/v1/places/{place_id}/reviews')
            self.assertEqual(get_response.status_code, 200)
            print(f"Response (status {get_response.status_code}): {get_response.json}")
        
    def test_create_user_place_place_same_title(self):
        print("\nTest: Create User, Place, Place with same title")

        print("\n1. Creating user...")
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@email.com"
        }
        print(f"Request data: {user_data}")
        response1 = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response1.status_code, 201)
        user_id = response1.json['id']

        print("\n2. Creating place...")
        place_data = {
            "title": "Test Place",
            "description": "Test description",
            "price": 100.0,
            "latitude": 1.0,
            "longitude": 1.0,
            "owner_id": user_id,
            "amenities": []
        }
        print(f"Request data: {place_data}")
        response2 = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response2.status_code, 201)
        place_id = response2.json['id']

        print("\n3. Creating place with same title...")
        place_data = {
            "title": "Test Place",
            "description": "Test description",
            "price": 100.0,
            "latitude": 1.0,
            "longitude": 1.0,
            "owner_id": user_id,
            "amenities": []
        }
        print(f"Request data: {place_data}")
        response3 = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response3.status_code, 400)
        print(f"Response (status {response3.status_code}): {response3.json}")

    def test_create_user_place_and_update_place_same_title(self):
        print("\nTest: Create User and Place and update place with same title")

        print("\n1. Creating user...")
        user_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "aaaaaa@aaa.aa"
        }
        print(f"Request data: {user_data}")
        response1 = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response1.status_code, 201)
        print(f"Response (status {response1.status_code}): {response1.json}")
        
        user_id = response1.json['id']

        print("\n2. Creating place...")
        place_data = {
            "title": "New place",
            "description": "A beautiful place",
            "price": 100.0,
            "latitude": 1.0,
            "longitude": 1.0,
            "owner_id": user_id,
            "amenities": []
        }
        print(f"Request data: {place_data}")
        response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response.status_code, 201)
        print(f"Response (status {response.status_code}): {response.json}")

        place_id = response.json['id']

        print("\n3. Getting place...")
        get_response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(get_response.status_code, 200)
        print(f"Response (status {get_response.status_code}): {get_response.json}")

        print("\n4. Creating another place...")
        place_data = {
            "title": "Another place",
            "description": "A beautiful place",
            "price": 100.0,
            "latitude": 1.0,
            "longitude": 1.0,
            "owner_id": user_id,
            "amenities": []
        }
        print(f"Request data: {place_data}")
        response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response.status_code, 201)
        print(f"Response (status {response.status_code}): {response.json}")

        print("\n5. Updating place with same title...")
        update_response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Another place",
            "description": "A beautiful place",
            "price": 50.0,
            "latitude": 2.0,
            "longitude": 0.0,
            "owner_id": user_id,
            "amenities": []
        })
        self.assertEqual(update_response.status_code, 400)
        print(f"Response (status {update_response.status_code}): {update_response.json}")