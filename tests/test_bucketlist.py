from app.bucketlist import BucketlistItem
from app.models import Bucketlist, Item
from tests.test_setup import TestBaseCase


class BucketlistTest(TestBaseCase):
    """Tests the BucketlistItem class methods"""

    def test_create_bucketlist(self):
        """tests that a bucketlist is created and added to the database"""
        # assert that there are no bucketlists in the database
        self.assertEqual(Bucketlist.query.count(), 2)
        # add a bucketlist
        BucketlistItem.create_bucketlist({"name": "new"}, 1)
        # assert that there is a bucketlist
        self.assertEqual(Bucketlist.query.count(), 3)

    def test_list_bucketlists(self):
        """tests that all bucketlists in the system are listed"""
        # add to an empty bucketlist then list to see it is there
        BucketlistItem.create_bucketlist({"name": "new"}, 1)
        data_set1 = {"q": None, "page": None, "limit": None}
        data_set2 = {"q": "o", "page": 1, "limit": 2}
        data_set3 = {"q": None, "page": 1, "limit": 3}
        data_set4 = {"q": "o", "page": 1, "limit": 1}
        url_root = {"http://127.0.0.1:5000"}
        self.assertEqual(
            len(BucketlistItem.list_bucketlists(data_set1, 1, url_root)),
            5)
        # assert that there are now two in the list
        BucketlistItem.create_bucketlist({"name": "blood"}, 1)
        self.assertEqual(
            len(BucketlistItem.list_bucketlists(data_set1, 1, url_root)),
            6)
        # assert that there are now three in the list
        BucketlistItem.create_bucketlist({"name": "hounds"}, 1)
        self.assertEqual(
            len(BucketlistItem.list_bucketlists(data_set1, 1, url_root)),
            7)
        # assert can search using substrings
        self.assertEqual(
            len(BucketlistItem.list_bucketlists(data_set2, 1, url_root)),
            5)
        # assert limit in listing bucketlists
        self.assertEqual(
            len(BucketlistItem.list_bucketlists(data_set3, 1, url_root)),
            6)
        # assert limit works for searching with substring
        self.assertEqual(
            len(BucketlistItem.list_bucketlists(data_set4, 1, url_root)),
            4)

    def test_get_bucketlist(self):
        """tests that a particular bucketlist is retrieved"""
        # create new bucketlists
        BucketlistItem.create_bucketlist({"name": "new"}, 1)
        BucketlistItem.create_bucketlist({"name": "blood"}, 1)
        BucketlistItem.create_bucketlist({"name": "hounds"}, 1)
        # assert that you can get the bucketlists
        self.assertEqual(BucketlistItem.get_bucketlist(3, 1)["name"], "new")
        self.assertEqual(BucketlistItem.get_bucketlist(4, 1)["name"], "blood")
        self.assertEqual(BucketlistItem.get_bucketlist(5, 1)["name"], "hounds")

    def test_update_bucketlist(self):
        """tests that a particular bucketlist can be updated"""
        # create a bucketlist
        BucketlistItem.create_bucketlist({"name": "new"}, 1)
        bucketlist = Bucketlist.query.filter_by(id=3).first()
        # assert that the name is the same
        self.assertEqual(bucketlist.name, "new")
        # update bucketlist with a new name
        BucketlistItem.update_bucketlist({"name": "new name"}, 3, 1)
        # assert that the name is the updated name
        self.assertEqual(bucketlist.name, "new name")

    def test_delete_bucketlist(self):
        """tests that a specified bucketlist is deleted from the database"""
        # create a new bucketlist
        BucketlistItem.create_bucketlist({"name": "another"}, 1)
        # assert that there are now two bucketlists
        self.assertEqual(Bucketlist.query.count(), 3)
        # delete the new bucketlists
        BucketlistItem.delete_bucketlist(3, 1)
        # assert that it is now one bucket list
        self.assertEqual(Bucketlist.query.count(), 2)

    def test_create_item(self):
        """tests that a specified item is created"""
        # create bucketlist for item
        BucketlistItem.create_bucketlist({"name": "new"}, 1)
        # assert that there are no items in the database
        self.assertEqual(Item.query.count(), 1)
        # create one item
        BucketlistItem.create_item({"name": "item2"}, 3, 1)
        # assert that there is now one item in the database
        self.assertEqual(Item.query.count(), 2)

    def test_udpate_item(self):
        """tests that a particular bucketlist item can be updated"""
        # create bucketlist and Item
        BucketlistItem.create_bucketlist({"name": "new"}, 1)
        BucketlistItem.create_item({"name": "item2"}, 3, 1)
        # assert that the item is not done
        item = Item.query.filter_by(id=2).first()
        self.assertEqual(item.done, False)
        # update the item
        BucketlistItem.update_item({"done": "true"}, 2, 3, 1)
        # assert the done has changed
        item = Item.query.filter_by(id=2).first()
        self.assertEqual(item.done, True)

    def test_delete_item(self):
        """tests that a particular bucketlist item can be deleted"""
        # create a bucketlist and a bucketlist item
        BucketlistItem.create_bucketlist({"name": "new"}, 1)
        BucketlistItem.create_item({"name": "item2"}, 3, 1)
        # assert that there is one item in the database
        self.assertEqual(Item.query.count(), 2)
        # delete that item
        print(Item.query.count())
        BucketlistItem.delete_item(2, 3, 1)
        # assert that there is no item in the database
        self.assertEqual(Item.query.count(), 1)
