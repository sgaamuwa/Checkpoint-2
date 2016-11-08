import unittest
import json

from app.models import Bucketlist, Item
from resource import app, db


class TestBaseCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../tests/test.db'
        self.app = app.test_client()
        db.create_all()

        
        data = {"username": "samuel", "password": "pass123"}
        # register the User
        self.app.post(
            "/auth/register",
            data=json.dumps(data),
            content_type="application/json"
        )
        # log in the user
        self.app.post(
            "/auth/login",
            data=json.dumps(data),
            content_type="application/json"
        )
        # get a token
        headers = {
            'Authorization': 'Basic ' + 'c2FtdWVsOnBhc3MxMjM='
        }

        response = self.app.get("/token", headers=headers)
        token = json.loads(response.get_data().decode())["token"]

        self.headers = {
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
        # create a test Item
        item = {"name": "item1"}
        response = self.app.post(
            "/bucketlists/1/items/",
            data=json.dumps(item),
            content_type="application/json",
            headers=self.headers)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
