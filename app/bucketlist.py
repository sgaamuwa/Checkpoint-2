from datetime import datetime
from app.models import Bucketlist
from app.app import db


class BucketlistItem(object):
    """BucketList class 
    
    The bucket list class has methods for managing the bucketlists and items
    Bucketlist enables one to create, list, return, update and delete 
    bucketlists 

    Each bucketlist has list items that can be created, updated and deleted
    using the bucket list class
    """

    def create_bucketlist(data, user):
        """creates a bucketlist using information sent using POST"""
        bucketlist = Bucketlist(
            name=data["name"],
            date_created=datetime.now(),
            date_modified=datetime.now(),
            created_by=user
        )
        db.session.add(bucketlist)
        db.session.commit()
        new_entry = {
            "id": bucketlist.id,
            "name": bucketlist.name,
            "date_created": bucketlist.date_created,
            "date_modified": bucketlist.date_modified,
            "created_by": bucketlist.created_by
        }
        db.session.close()
        return new_entry

    def list_bucketlists():
        """lists all the bucketlists that are in the database"""
        pass

    def get_bucketlist(identifier):
        """returns a particular bucket list and its items"""
        pass

    def update_bucketlist():
        """modifies information for a given bucketlist in the database"""
        pass

    def delete_bucketlist(data):
        """deletes a particular bucketlist from the database"""
        bucketlist = Bucketlist.query.filter_by(id=data["id"]).first()
        db.session.delete(bucketlist)
        db.session.commit()
        db.session.close()

    def search_bucketlist():
        """searches for a bucketlist by using its name"""
        pass

    def create_item(name, bucketlist_id):
        """creates an item in a particular bucketlist"""
        pass

    def update_item():
        """updates a specified item in a particular bucketlist"""
        pass

    def delete_item():
        """deletes a specified item in a particular bucketlist"""
        pass
    