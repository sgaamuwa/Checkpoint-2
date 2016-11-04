from app.authentication import Authentication
from app.models import User
from tests.test_setup import TestBaseCase


class EndpointTests(TestBaseCase):

    def test_valid_login(self):
        login_data = {"username": "Samuel", "password": "pass123"}
        response = self.app.post(
            '/auth/login',
            data=login_data,
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        login_data = {"username": "Samuel", "password": "incorrect"}
        response = self.app.post(
            '/auth/register', 
            data=login_data, 
            content_type='application/json'
            )
        self.assertEqual(response.status_code, 200)

    def test_create_bucketlist(self):
        response = self.app.post('/bucketlists/')
        self.assertEqual(response.status_code, 200)

    def test_list_bucketlist(self):
        response = self.app.get('/bucketlists/')
        self.assertEqual(response.status_code, 200)

    def test_searches_bucketlists(self):
        # With one that exists
        response = self.app.get('/bucketlists?q=bucketlist')
        self.assertEqual(response.status_code, 200)
        # With one that doesn't exist
        response = self.app.get('/bucketlists?q=nolist')
        self.assertEqual(response.status_code, 404)
    
    def test_get_bucketlist(self):
        # test with a correct id
        response = self.app.get('/bucketlists/1')
        self.assertEqual(response.status_code, 200)
        # test with a wrong id
        response = self.app.get('/bucketlists/48')
        self.assertEqual(response.status_code, 404)
    
    def test_update_bucketlist(self):
        # test with a correct id
        response = self.app.put('/bucketlists/1')
        self.assertEqual(response.status_code, 200)
        # test with a wrong id
        response = self.app.put('/bucketlists/43')
        self.assertEqual(response.status_code, 404)

    def test_delete_bucketlist(self):
        # test with a correct id
        response = self.app.delete('/bucketlists/1')
        self.assertEqual(response.status_code, 200)
        # test with an incorrect id 
        response = self.app.delete('/bucketlists/43')
        self.assertEqual(response.status_code, 404)

    def test_create_item(self):
        # test with a correct bucketlist id
        response = self.app.post('/bucketlists/1/items/')
        self.assertEqual(response.status_code, 200)
        # test with an incorrect bucketlist id
        response = self.app.post('/bucketlists/43/items/')
        self.assertEqual(response.status_code, 404)

    def test_update_item(self):
        # test with all correct ids
        response = self.app.put('/bucketlists/1/items/1')
        self.assertEqual(response.status_code, 200)
        # test with correct bucketlist id, incorrect item id
        response = self.app.put('/bucketlists/1/items/43')
        self.assertEqual(response.status_code, 404)
        # test with incorrect bucketlist id, correct item id
        response = self.app.put('/bucketlists/43/items/1')
        self.assertEqual(response.status_code, 404)
        # test with incorrect ids
        response = self.app.put('/bucketlists/43/items/43')
        self.assertEqual(response.status_code, 404)
    
    def test_delete_item(self):
        # test with all correct ids
        response = self.app.delete('/bucketlists/1/items/1')
        self.assertEqual(response.status_code, 200)
        # test with correct bucketlist id, incorrect item id
        response = self.app.delete('/bucketlists/1/items/43')
        self.assertEqual(response.status_code, 404)
        # test with incorrect bucketlist id, correct item id
        response = self.app.delete('/bucketlists/43/items/1')
        self.assertEqual(response.status_code, 404)
        # test with incorrect ids
        response = self.app.delete('/bucketlists/43/items/43')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()