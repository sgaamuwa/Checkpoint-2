from app.authentication import Authentication
from app.models import User
from tests.test_setup import TestBaseCase


class EndpointTests(TestBaseCase):
    """Tests the endpoints in the application"""

    def test_valid_login(self):
        """tests that valid login information enables one to login"""
        login_data = {"username": "Samuel", "password": "pass123"}
        response = self.app.post(
            "/auth/login",
            data=login_data,
            content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        """tests that register responses with correct data"""
        register_data = {"username": "Samuel", "password": "incorrect"}
        response = self.app.post(
            "/auth/register", 
            data=register_data, 
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)

    def test_create_bucketlist(self):
        """tests that a new bucketlist is created and the response received"""
        bucketlist = {"name": "New Bucketlist"}
        response = self.app.post(
            "/bucketlists/",
            data=bucketlist,
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)

    def test_list_bucketlist(self):
        """tests that list bucketlist returns a list of bucketlists"""
        response = self.app.get("/bucketlists/")
        self.assertEqual(response.status_code, 200)

    def test_searches_bucketlists(self):
        """tests that a search by name returns the bucketlist item"""
        # With one that exists
        response = self.app.get("/bucketlists?q=bucketlist")
        self.assertEqual(response.status_code, 200)
        # With one that doesn"t exist
        response = self.app.get("/bucketlists?q=nolist")
        self.assertEqual(response.status_code, 404)
    
    def test_get_bucketlist(self):
        """tests that a bucketlist is returned when its id is passed"""
        # test with a correct id
        response = self.app.get("/bucketlists/1")
        self.assertEqual(response.status_code, 200)
        # test with a wrong id
        response = self.app.get("/bucketlists/48")
        self.assertEqual(response.status_code, 404)
    
    def test_update_bucketlist(self):
        """tests that bucketlists are updated in the system"""
        # test with a correct id
        update_information = {"name": "new new name"}
        response = self.app.put(
            "/bucketlists/1",
            data=update_information,
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 200)
        # test with a wrong id
        response = self.app.put("/bucketlists/43")
        self.assertEqual(response.status_code, 404)

    def test_delete_bucketlist(self):
        """tests that bucketlists are deleted from the system"""
        # test with a correct id
        response = self.app.delete("/bucketlists/1")
        self.assertEqual(response.status_code, 200)
        # test with an incorrect id 
        response = self.app.delete("/bucketlists/43")
        self.assertEqual(response.status_code, 404)

    def test_create_item(self):
        """tests that items are created in the system"""
        # test with a correct bucketlist id
        item = {"name": "item1"}
        response = self.app.post(
            "/bucketlists/1/items/"
            data=item,
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        # test with an incorrect bucketlist id
        response = self.app.post("/bucketlists/43/items/")
        self.assertEqual(response.status_code, 404)

    def test_update_item(self):
        # test with all correct ids
        update_info = {"done": "true"}
        response = self.app.put(
            "/bucketlists/1/items/1",
            data=update_info,
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        # test with correct bucketlist id, incorrect item id
        response = self.app.put(
            "/bucketlists/1/items/43",
            data=update_info,
            content_type="application/json")
        self.assertEqual(response.status_code, 404)
        # test with incorrect bucketlist id, correct item id
        response = self.app.put(
            "/bucketlists/43/items/1",
            data=update_info,
            content_type="application/json")
        self.assertEqual(response.status_code, 404)
        # test with incorrect ids
        response = self.app.put(
            "/bucketlists/43/items/43",
            data=update_info,
            content_type="application/json")
        self.assertEqual(response.status_code, 404)
    
    def test_delete_item(self):
        # test with all correct ids
        response = self.app.delete("/bucketlists/1/items/1")
        self.assertEqual(response.status_code, 200)
        # test with correct bucketlist id, incorrect item id
        response = self.app.delete("/bucketlists/1/items/43")
        self.assertEqual(response.status_code, 404)
        # test with incorrect bucketlist id, correct item id
        response = self.app.delete("/bucketlists/43/items/1")
        self.assertEqual(response.status_code, 404)
        # test with incorrect ids
        response = self.app.delete("/bucketlists/43/items/43")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()