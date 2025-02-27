import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
    
    def test_get_user_not_found(self):
        response = self.client.get('/api/v1/users/qsdqsqqds')
        self.assertEqual(response.status_code, 404)

    def test_create_and_get_user_and_update(self):
        # Create user
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bobby",
            "last_name": "aaaa", 
            "email": "Bobbye.aaaa@example.com"
        })
        print(f"\nCreate response: {response.json}")
        self.assertEqual(response.status_code, 201)
        
        user_id = response.json['id']
        
        # Get user
        get_response = self.client.get(f'/api/v1/users/{user_id}')
        print(f"Get response: {get_response.json}")
        self.assertEqual(get_response.status_code, 200)

        # Update user
        update_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "bbbbb",
            "last_name": "poaoaoa",
            "email": "aaaa@example.com"
        })
        print(f"Update response: {update_response.json}")
        self.assertEqual(update_response.status_code, 200)
        
        # Verify update
        verify_response = self.client.get(f'/api/v1/users/{user_id}')
        print(f"Verify response: {verify_response.json}")
        self.assertEqual(verify_response.status_code, 200)

    def test_create_user_place(self):

        response1 = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "aaa@aaa.aa"
        })
        self.assertEqual(response1.status_code, 201)
        user_id = response1.json['id']


        response = self.client.post('/api/v1/places/', json={
            "title": "My Place",
            "description": "A beautiful place",
            "price": 100.0,
            "latitude": 1.0,
            "longitude": 1.0,
            "owner_id": user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 201)
