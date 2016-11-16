import unittest
import json

from manage import app, db


class TestBaseCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../tests/test.db'
        self.app = app.test_client()
        db.create_all()

        data = {"username": "samuel", "password": "pass123"}
        data2 = {"username": "arnold", "password": "pass123"}
        # register the User
        self.app.post(
            "/auth/register",
            data=json.dumps(data),
            content_type="application/json"
        )
        # register the second User
        self.app.post(
            "/auth/register",
            data=json.dumps(data2),
            content_type="application/json"
        )
        # log in the user
        response = self.app.post(
            "/auth/login",
            data=json.dumps(data),
            content_type="application/json"
        )

        token = json.loads(response.get_data().decode())["token"]

        self.headers = {
            "Authorization": "Bearer " + token
        }
        
        # log in the second user
        response = self.app.post(
            "/auth/login",
            data=json.dumps(data2),
            content_type="application/json"
        )
        
        token = json.loads(response.get_data().decode())["token"]

        self.headers2 = {
            "Authorization": "Bearer " + token
        }
        # create a test bucketlist
        bucketlist = {"name": "New Bucketlist"}
        self.app.post(
            "/bucketlists/",
            data=json.dumps(bucketlist),
            content_type="application/json",
            headers=self.headers
            )
        # create a test bucketlist for second user
        bucketlist = {"name": "Newer Bucketlist"}
        self.app.post(
            "/bucketlists/",
            data=json.dumps(bucketlist),
            content_type="application/json",
            headers=self.headers2
            )
        # create a test Item
        item = {"name": "item1"}
        response = self.app.post(
            "/bucketlists/1/items/",
            data=json.dumps(item),
            content_type="application/json",
            headers=self.headers)
        # create a test Item for second user
        item = {"name": "item3"}
        response = self.app.post(
            "/bucketlists/1/items/",
            data=json.dumps(item),
            content_type="application/json",
            headers=self.headers2)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
