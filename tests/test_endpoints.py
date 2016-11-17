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
        self.assertIn('Login Successful', data)

    def test_invalid_login(self):
        """tests that invalid login information not logged in"""
        login_data = {"username": "samuel", "password": "pass"}
        response = self.app.post(
            "/auth/login",
            data=json.dumps(login_data),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn('Please enter the right credentials', data)
        # test with no data
        login_data = {"username": "", "password": ""}
        response = self.app.post(
            "/auth/login",
            data=json.dumps(login_data),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertEqual(data, '{"result": "username required"}\n')

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
        self.assertIn('User successfully registered', data)
        # test with no data
        register_data = {"username": "", "password": ""}
        response = self.app.post(
            '/auth/register',
            data=json.dumps(register_data),
            content_type='application/json'
            )
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn('{\n  "result": "username required"\n}\n', data)
        # test with username and no password
        register_data = {"username": "mechanic", "password": ""}
        response = self.app.post(
            '/auth/register',
            data=json.dumps(register_data),
            content_type='application/json'
            )
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn('{\n  "result": "password required"\n}\n', data)
        # test registration with short username
        register_data = {"username": "xy", "password": "pass123"}
        response = self.app.post(
            '/auth/register',
            data=json.dumps(register_data),
            content_type='application/json'
            )
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn('username is too short', data)
        # test registration with short password
        register_data = {"username": "ocean", "password": "pas"}
        response = self.app.post(
            '/auth/register',
            data=json.dumps(register_data),
            content_type='application/json'
            )
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn('password is too short', data)
        # test registration with user in system
        register_data = {"username": "Samuel", "password": "incorrect"}
        response = self.app.post(
            '/auth/register',
            data=json.dumps(register_data),
            content_type='application/json'
            )
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn('username already exists', data)

    def test_create_bucketlist(self):
        """tests that a new bucketlist is created and the response received"""
        bucketlist = {"name": "New Bucketlist 2"}
        response = self.app.post(
            "/bucketlists/",
            data=json.dumps(bucketlist),
            content_type="application/json",
            headers=self.headers
            )
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn("New Bucketlist 2", data)
        # test you can't create without a token
        response = self.app.post(
            "/bucketlists/",
            data=json.dumps(bucketlist),
            content_type="application/json"
            )
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized Access", data)
        # test cant create without data
        bucketlist = {"name": ""}
        response = self.app.post(
            "/bucketlists/",
            data=json.dumps(bucketlist),
            content_type="application/json",
            headers=self.headers
            )
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        print(data)
        self.assertIn("Enter a name for bucketlist", data)

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
        self.assertEqual(response.status_code, 404)
        data = response.get_data().decode("utf-8")
        self.assertIn("Resource not found", data)
        # test cant lists without token
        response = self.app.get(
            "/bucketlists/1",
            )
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized Access", data)
        # test get bucketlist not owned
        response = self.app.get(
            "/bucketlists/1",
            headers=self.headers2)
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access for bucketlist", data)

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
        # test with no data
        update_information = {"name": ""}
        response = self.app.put(
            "/bucketlists/1",
            data=json.dumps(update_information),
            content_type="application/json",
            headers=self.headers
            )
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn("Enter a name for bucketlist", data)
        # test with a wrong id
        response = self.app.put(
            "/bucketlists/43",
            headers=self.headers)
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access", data)
        # test cant update without token
        response = self.app.put(
            "/bucketlists/1",
            )
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized Access", data)
        # test can't update bucketlist not owned
        update_information = {"name": "new new name"}
        response = self.app.put(
            "/bucketlists/1",
            data=json.dumps(update_information),
            content_type="application/json",
            headers=self.headers2
            )
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access for bucketlist", data)

    def test_delete_bucketlist(self):
        """tests that bucketlists are deleted from the system"""
        # test cant delete bucketlist not owned
        response = self.app.delete(
            "/bucketlists/1",
            headers=self.headers2
            )
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access for bucketlist", data)
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
        self.assertEqual(response.status_code, 404)
        data = response.get_data().decode("utf-8")
        self.assertIn("Resource not found", data)
        # test cant delete without token
        response = self.app.delete(
            "/bucketlists/1",
            )
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized Access", data)

    def test_create_item(self):
        """tests that items are created in the system"""
        # test with a correct bucketlist id
        item = {"name": "item2"}
        response = self.app.post(
            "/bucketlists/1/items/",
            data=json.dumps(item),
            content_type="application/json",
            headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn("item2", data)
        # test with an incorrect bucketlist id
        response = self.app.post(
            "/bucketlists/43/items/",
            data=json.dumps(item),
            content_type="application/json",
            headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = response.get_data().decode("utf-8")
        self.assertIn("Resource not found", data)
        # test cant create if not owner
        item = {"name": "item4"}
        response = self.app.post(
            "/bucketlists/1/items/",
            data=json.dumps(item),
            content_type="application/json",
            headers=self.headers2)
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access for bucketlist", data)

    def test_update_item(self):
        update_info = {"name": "supernew", "done": "true"}
        # test cant update if not owner
        response = self.app.put(
            "/bucketlists/1/items/1",
            data=json.dumps(update_info),
            content_type="application/json",
            headers=self.headers2)
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access for bucketlist", data)
        # test with all correct ids
        response = self.app.put(
            "/bucketlists/1/items/1",
            data=json.dumps(update_info),
            content_type="application/json",
            headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode("utf-8")
        self.assertIn("true", data)
        self.assertIn("supernew", data)
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
        self.assertEqual(response.status_code, 404)
        data = response.get_data().decode("utf-8")
        self.assertIn("Resource not found", data)
        # test with incorrect ids
        response = self.app.put(
            "/bucketlists/43/items/43",
            data=json.dumps(update_info),
            content_type="application/json",
            headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = response.get_data().decode("utf-8")
        self.assertIn("Resource not found", data)

    def test_delete_item(self):
        # test cant delete if not owner
        response = self.app.delete(
            "/bucketlists/1/items/1",
            headers=self.headers2)
        self.assertEqual(response.status_code, 401)
        data = response.get_data().decode("utf-8")
        self.assertIn("Unauthorized access for bucketlist", data)
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
        self.assertEqual(response.status_code, 404)
        data = response.get_data().decode("utf-8")
        self.assertIn("Resource not found", data)
        # test with incorrect bucketlist id, correct item id
        response = self.app.delete(
            "/bucketlists/43/items/1",
            headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = response.get_data().decode("utf-8")
        self.assertIn("Resource not found", data)
        # test with incorrect ids
        response = self.app.delete(
            "/bucketlists/43/items/43",
            headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = response.get_data().decode("utf-8")
        self.assertIn("Resource not found", data)
