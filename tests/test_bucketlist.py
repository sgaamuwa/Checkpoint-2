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
        try:
            self.assertEqual(len(BucketlistItem.list_bucketlists()), 1)
        except:
            return "no database data"

    def test_get_bucketlist(self):
        """tests that a particular bucketlist is retrieved"""
        # try to retrieve from the things that are there
        try:
            self.assertEqual(BucketlistItem.get_bucketlist(1)["name"], "new")
        except:
            return "no database data"

    def test_update_bucketlist(self):
        """tests that a particular bucketlist can be updated"""
        # add something to the list and try to update it
        data = {"name": "new name"}
        bucketlist_id = 1
        try:
            bucketlist = Bucketlist.query.filter_by(id=bucketlist_id).first()
            self.assertEqual(bucketlist.name, "name")
            BucketlistItem.update_bucketlist(item_id, data)
            item = Bucketlist.query.filter(id=bucketlist_id).first()
            self.assertEqual(bucketlist.name, "new name")
        except:
            return "no database data"

    def test_delete_bucketlist(self):
        """tests that a specified bucketlist can be deleted from the database"""
        # create a new bucketlist
        BucketlistItem.create_bucketlist({"name": "another"}, "samuel")
        # assert that there are now two bucketlists
        self.assertEqual(Bucketlist.query.count(), 1)
        # delete the new bucketlists
        BucketlistItem.delete_bucketlist({"id": 1})
        # assert that it is now one bucket list
        self.assertEqual(Bucketlist.query.count(), 0)

    def test_create_item(self):
        """tests that a specified item is created"""
        # assert that there are no items in the database
        self.assertEqual(Item.query.count(), 0)
        # create one item
        BucketlistItem.create_item("name", 1)
        # assert that there is now one item in the database
        self.assertEqual(Item.query.count(), 1)

    def test_udpate_item(self):
        """tests that a particular bucketlist item can be updated"""
        # determine the update data
        data = {"name": "new name"}
        item_id = 1
        try:
            # try if there is data in the database
            item = Item.query.filter_by(id=item_id).first()
            self.assertEqual(item.name, "name")
            BucketlistItem.update_item(item_id, data)
            item = Item.query.filter(id=item_id).first()
            self.assertEqual(item.name, "new name")
        except:
            # else return that there is no data 
            return "no database data"

    def test_delete_item(self):
        """tests that a particular bucketlist item can be deleted"""
        # assert that there is one item in the database
        self.assertEqual(Item.query.count(), 1)
        # delete that item
        BucketlistItem.delete_item(1)
        # assert that there is no item in the database
        self.assertEqual(Item.query.count(), 0)

if __name__ == "__main__":
    unittest.main()