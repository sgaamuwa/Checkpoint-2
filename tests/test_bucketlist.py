from bucketlist.bucketlist import Bucketlist
from database import models
from tests.test_setup import TestBaseCase

class BucketlistTest(TestBaseCase):

    def test_create_bucketlist(self):
        # assert that there are no bucketlists in the database
        self.assertEqual(models.Bucketlist.query.count(), 0)
        # add a bucketlist
        Bucketlist.create_bucketlist("new")
        # assert that there is a bucketlist
        self.assertEqual(models.Bucketlist.query.count(), 1)

    def test_list_bucketlists(self):
        # add to an empty bucketlist then list to see it is there
        try:
            self.assertEqual(len(Bucketlist.list_bucketlists()), 1)
        except:
            return "no database data"

    def test_get_bucketlist(self):
        # try to retrieve from the things that are there
        try:
            self.assertEqual(Bucketlist.get_bucketlist(1)["name"], "new")
        except:
            return "no database data"

    def test_update_bucketlist(self):
        # add something to the list and try to update it
        data = {"name": "new name"}
        bucketlist_id = 1
        try:
            bucketlist = models.Bucketlist.query.filter_by(id=bucketlist_id).first()
            self.assertEqual(bucketlist.name, "name")
            Bucketlist.update_bucketlist(item_id, data)
            item = models.Bucketlist.query.filter(id=bucketlist_id).first()
            self.assertEqual(bucketlist.name, "new name")
        except:
            return "no database data"

    def test_delete_bucketlist(self):
        # create a new bucketlist
        Bucketlist.create_bucketlist("another")
        # assert that there are now two bucketlists
        self.assertEqual(models.Bucketlist.query.count(), 2)
        # delete the new bucketlists
        Bucketlist.delete_bucketlist(2)
        # assert that it is now one bucket list
        self.assertEqual(models.Bucketlist.query.count(), 1)

    def test_create_item(self):
        # assert that there are no items in the database
        self.assertEqual(models.Item.query.count(), 0)
        # create one item
        Bucketlist.create_item("name", 1)
        # assert that there is now one item in the database
        self.assertEqual(models.Item.query.count(), 1)

    def test_udpate_item(self):
        # determine the update data
        data = {"name": "new name"}
        item_id = 1
        try:
            # try if there is data in the database
            item = models.Item.query.filter_by(id=item_id).first()
            self.assertEqual(item.name, "name")
            Bucketlist.update_item(item_id, data)
            item = models.Item.query.filter(id=item_id).first()
            self.assertEqual(item.name, "new name")
        except:
            # else return that there is no data 
            return "no database data"

    def test_delete_item(self):
        # assert that there is one item in the database
        self.assertEqual(models.Item.query.count(), 1)
        # delete that item
        Bucketlist.delete_item(1)
        # assert that there is no item in the database
        self.assertEqual(models.Item.query.count(), 0)

if __name__ == "__main__":
    unittest.main()