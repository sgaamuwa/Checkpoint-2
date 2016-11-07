from app.bucketlist import BucketlistItem
from app.models import Bucketlist, Item
from tests.test_setup import TestBaseCase


class BucketlistTest(TestBaseCase):
    """Tests the BucketlistItem class methods"""

    def test_create_bucketlist(self):
        """tests that a bucketlist is created and added to the database"""
        # assert that there are no bucketlists in the database
        self.assertEqual(Bucketlist.query.count(), 0)
        # add a bucketlist
        BucketlistItem.create_bucketlist({"name": "new"}, "samuel")
        # assert that there is a bucketlist
        self.assertEqual(Bucketlist.query.count(), 1)

    def test_list_bucketlists(self):
        """tests that all bucketlists in the system are listed"""
        # add to an empty bucketlist then list to see it is there
        BucketlistItem.create_bucketlist({"name": "new"}, "samuel")
        self.assertEqual(len(BucketlistItem.list_bucketlists()), 1)
        # assert that there are now two in the list
        BucketlistItem.create_bucketlist({"name": "blood"}, "samuel")
        self.assertEqual(len(BucketlistItem.list_bucketlists()), 2)
        # assert that there are now three in the list
        BucketlistItem.create_bucketlist({"name": "hounds"}, "samuel")
        self.assertEqual(len(BucketlistItem.list_bucketlists()), 3)

    def test_get_bucketlist(self):
        """tests that a particular bucketlist is retrieved"""
        # create new bucketlists 
        BucketlistItem.create_bucketlist({"name": "new"}, "samuel")
        BucketlistItem.create_bucketlist({"name": "blood"}, "samuel")
        BucketlistItem.create_bucketlist({"name": "hounds"}, "samuel")
        # assert that you can get the bucketlists
        self.assertEqual(BucketlistItem.get_bucketlist(1)["name"], "new")
        self.assertEqual(BucketlistItem.get_bucketlist(2)["name"], "blood")
        self.assertEqual(BucketlistItem.get_bucketlist(3)["name"], "hounds")
        # assert that you can get by name
        self.assertEqual(BucketlistItem.get_bucketlist({"name": "new"})["name"], "new")
        self.assertEqual(BucketlistItem.get_bucketlist({"name": "blood"})["name"], "blood")
        self.assertEqual(BucketlistItem.get_bucketlist({"name": "hounds"})["name"], "hounds")

    def test_update_bucketlist(self):
        """tests that a particular bucketlist can be updated"""
        # create a bucketlist
        BucketlistItem.create_bucketlist({"name": "new"}, "samuel")
        bucketlist = Bucketlist.query.filter_by(id=1).first()
        # assert that the name is the same 
        self.assertEqual(bucketlist.name, "new")
        # update bucketlist with a new name
        BucketlistItem.update_bucketlist({"name": "new name"}, 1)
        item = Bucketlist.query.filter_by(id=1).first()
        # assert that the name is the updated name
        self.assertEqual(bucketlist.name, "new name")

    def test_delete_bucketlist(self):
        """tests that a specified bucketlist can be deleted from the database"""
        # create a new bucketlist
        BucketlistItem.create_bucketlist({"name": "another"}, "samuel")
        # assert that there are now two bucketlists
        self.assertEqual(Bucketlist.query.count(), 1)
        # delete the new bucketlists
        BucketlistItem.delete_bucketlist(1)
        # assert that it is now one bucket list
        self.assertEqual(Bucketlist.query.count(), 0)

    def test_create_item(self):
        """tests that a specified item is created"""
        # create bucketlist for item
        BucketlistItem.create_bucketlist({"name": "new"}, "samuel")
        # assert that there are no items in the database
        self.assertEqual(Item.query.count(), 0)
        # create one item
        BucketlistItem.create_item({"name": "item1"}, 1)
        # assert that there is now one item in the database
        self.assertEqual(Item.query.count(), 1)

    def test_udpate_item(self):
        """tests that a particular bucketlist item can be updated"""
        # create bucketlist and Item
        BucketlistItem.create_bucketlist({"name": "new"}, "samuel")
        BucketlistItem.create_item({"name": "item1"}, 1)
        # assert that the item is not done
        item = Item.query.filter_by(id=1).first()
        self.assertEqual(item.done, False)
        # update the item
        BucketlistItem.update_item({"done": True}, 1, 1)
        # assert the done has changed
        item = Item.query.filter_by(id=1).first()
        self.assertEqual(item.done, True)

    def test_delete_item(self):
        """tests that a particular bucketlist item can be deleted"""
        # create a bucketlist and a bucketlist item
        BucketlistItem.create_bucketlist({"name": "new"}, "samuel")
        BucketlistItem.create_item({"name": "item1"}, 1)
        # assert that there is one item in the database
        self.assertEqual(Item.query.count(), 1)
        # delete that item
        BucketlistItem.delete_item(1, 1)
        # assert that there is no item in the database
        self.assertEqual(Item.query.count(), 0)

if __name__ == "__main__":
    unittest.main()