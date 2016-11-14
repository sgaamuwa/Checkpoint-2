import json

from tests.test_setup import TestBaseCase


class EndpointTests(TestBaseCase):
    """Tests the endpoints in the application"""

    def test_valid_login(self):
        """tests that valid login information enables one to login"""
        login_data = {"username": "samuel", "password": "pass123"}
        response = self.app.post(
            "/auth/login",
            data=json.dumps(login_data),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertEqual(data, '{\n  "result": true\n}\n')

    def test_register_user(self):
        """tests that register responses with correct data"""
        register_data = {"username": "Samuel", "password": "incorrect"}
        response = self.app.post(
            '/auth/register',
            data=json.dumps(register_data),
            content_type='application/json'
            )
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn(data, '{\n  "result": "success"\n}\n')

    def test_create_bucketlist(self):
        """tests that a new bucketlist is created and the response received"""
        bucketlist = {"name": "New Bucketlist"}
        response = self.app.post(
            "/bucketlists/",
            data=json.dumps(bucketlist),
            content_type="application/json",
            headers=self.headers
            )
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn("New Bucketlist", data)
        # test you can't create without a token
        response = self.app.post(
            "/bucketlists/",
            data=json.dumps(bucketlist),
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized Access", data)

    def test_list_bucketlist(self):
        """tests that list bucketlist returns a list of bucketlists"""
        response = self.app.get(
            "/bucketlists/",
            headers=self.headers
            )
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn("New Bucketlist", data)
        # test cant lists without token
        response = self.app.get(
            "/bucketlists/",
            )
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized Access", data)
        # test with limit arguments
        response = self.app.get(
            "/bucketlists/?limit=1",
            headers=self.headers
            )
        print(response.headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn("New Bucketlist", data)
        # test with q argument
        response = self.app.get(
            "/bucketlists/?q=ucke",
            headers=self.headers
            )
        print(response.headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn("New Bucketlist", data)

    def test_get_bucketlist(self):
        """tests that a bucketlist is returned when its id is passed"""
        # test with a correct id
        response = self.app.get(
            "/bucketlists/1",
            headers=self.headers
            )
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn("New Bucketlist", data)
        # test with a wrong id
        response = self.app.get(
            "/bucketlists/48",
            headers=self.headers)
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access", data)
        # test cant lists without token
        response = self.app.get(
            "/bucketlists/1",
            )
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized Access", data)

    def test_update_bucketlist(self):
        """tests that bucketlists are updated in the system"""
        # test with a correct id
        update_information = {"name": "new new name"}
        response = self.app.put(
            "/bucketlists/1",
            data=json.dumps(update_information),
            content_type="application/json",
            headers=self.headers
            )
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn("new new name", data)
        # test with a wrong id
        response = self.app.put(
            "/bucketlists/43",
            headers=self.headers)
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access", data)

    def test_delete_bucketlist(self):
        """tests that bucketlists are deleted from the system"""
        # test with a correct id
        response = self.app.delete(
            "/bucketlists/1",
            headers=self.headers
            )
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn("Bucketlist ID:1 deleted", data)
        # test with an incorrect id
        response = self.app.delete(
            "/bucketlists/43",
            headers=self.headers)
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access", data)

    def test_create_item(self):
        """tests that items are created in the system"""
        # test with a correct bucketlist id
        item = {"name": "item1"}
        response = self.app.post(
            "/bucketlists/1/items/",
            data=json.dumps(item),
            content_type="application/json",
            headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn("item1", data)
        # test with an incorrect bucketlist id
        response = self.app.post(
            "/bucketlists/43/items/",
            data=json.dumps(item),
            content_type="application/json",
            headers=self.headers)
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access", data)

    def test_update_item(self):
        # test with all correct ids
        update_info = {"done": "true"}
        response = self.app.put(
            "/bucketlists/1/items/1",
            data=json.dumps(update_info),
            content_type="application/json",
            headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn("true", data)
        # test with correct bucketlist id, incorrect item id
        response = self.app.put(
            "/bucketlists/1/items/43",
            data=json.dumps(update_info),
            content_type="application/json",
            headers=self.headers)
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access", data)
        # test with incorrect bucketlist id, correct item id
        response = self.app.put(
            "/bucketlists/43/items/1",
            data=json.dumps(update_info),
            content_type="application/json",
            headers=self.headers)
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access", data)
        # test with incorrect ids
        response = self.app.put(
            "/bucketlists/43/items/43",
            data=json.dumps(update_info),
            content_type="application/json",
            headers=self.headers)
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access", data)

    def test_delete_item(self):
        # test with all correct ids
        response = self.app.delete(
            "/bucketlists/1/items/1",
            headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn("Item ID:1 deleted from Bucketlist ID:1", data)
        # test with correct bucketlist id, incorrect item id
        response = self.app.delete(
            "/bucketlists/1/items/43",
            headers=self.headers)
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access", data)
        # test with incorrect bucketlist id, correct item id
        response = self.app.delete(
            "/bucketlists/43/items/1",
            headers=self.headers)
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access", data)
        # test with incorrect ids
        response = self.app.delete(
            "/bucketlists/43/items/43",
            headers=self.headers)
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access", data)
