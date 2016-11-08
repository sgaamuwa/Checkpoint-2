from datetime import datetime
from app.models import Bucketlist, Item
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
        bucketlist_list = {}
        bucketlists = Bucketlist.query.all()
        for bucketlist in bucketlists:
            item_list = []
            items = Item.query.filter_by(bucketlist=bucketlist.id).all()
            for item in items:
                item_dict = {
                    "id": item.id,
                    "name": item.name,
                    "date_created": item.date_created,
                    "date_modified": item.date_modified,
                    "done": item.done
                }
                item_list.append(item_dict)
            bucketlist_dict = {
                "id": bucketlist.id,
                "name": bucketlist.name,
                "items": item_list,
                "date_created": bucketlist.date_created,
                "date_modified": bucketlist.date_modified,
                "created_by": bucketlist.created_by
            }
            bucketlist_list[bucketlist.name] = bucketlist_dict
        return bucketlist_list


    def get_bucketlist(data):
        """returns a particular bucket list and its items"""
        # if "id" in data.keys():
        bucketlist = Bucketlist.query.filter_by(id=data).first()
        # elif "name" in data.keys():
        #     bucketlist = Bucketlist.query.filter_by(name=data["name"]).first()
        item_list = []
        items = Item.query.filter_by(bucketlist=bucketlist.id).all()
        for item in items:
            item_dict = {
                "id": item.id,
                "name": item.name,
                "date_created": item.date_created,
                "date_modified": item.date_modified,
                "done": item.done
            }
            item_list.append(item_dict)
        bucketlist_dict = {
                "id": bucketlist.id,
                "name": bucketlist.name,
                "items": item_list,
                "date_created": bucketlist.date_created,
                "date_modified": bucketlist.date_modified,
                "created_by": bucketlist.created_by
            }
        return bucketlist_dict
        
    def update_bucketlist(data, id):
        """modifies information for a given bucketlist in the database"""
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        bucketlist.name = data["name"]
        bucketlist.date_modified = datetime.now()
        db.session.commit()
        bucketlist_dict = {
                "id": bucketlist.id,
                "name": bucketlist.name,
                "date_created": bucketlist.date_created,
                "date_modified": bucketlist.date_modified,
                "created_by": bucketlist.created_by
            }
        db.session.close()
        return bucketlist_dict

    def delete_bucketlist(id):
        """deletes a particular bucketlist from the database"""
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        db.session.delete(bucketlist)
        db.session.commit()
        db.session.close()
        return {"message": "Bucketlist ID:{} deleted".format(id)}

    def create_item(data, bucketlist_id):
        """creates an item in a particular bucketlist"""
        bucketlist = Bucketlist.query.filter_by(id=bucketlist_id).first()
        item = Item(
            name=data["name"],
            date_created=datetime.now(),
            date_modified=datetime.now(),
            done=False,
            bucketlist=bucketlist.id
        )
        bucketlist.date_modified = datetime.now()
        db.session.add(item)
        db.session.commit()
        new_entry = {
            "id": item.id,
            "name": item.name,
            "date_created": item.date_created,
            "date_modified": item.date_modified,
            "done": item.done,
            "bucketlist": bucketlist.name
        }
        db.session.close()
        return new_entry

    def update_item(data, id, bucketlist_id):
        """updates a specified item in a particular bucketlist"""
        bucketlist = Bucketlist.query.filter_by(id=bucketlist_id).first()
        item = Item.query.filter_by(id=id, bucketlist=bucketlist_id).first()
        if data["done"] == "true":
            item.done = True
        else:
            item.done = False
        item.date_modified = datetime.now()
        bucketlist.date_modified = datetime.now()
        db.session.commit()
        updated_item = {
            "id": item.id,
            "name": item.name,
            "date_created": item.date_created,
            "date_modified": item.date_modified,
            "done": item.done,
            "bucketlist": bucketlist.name
        }
        db.session.close()
        return updated_item

    def delete_item(id, bucketlist_id):
        """deletes a specified item in a particular bucketlist"""
        item = Item.query.filter_by(id=id, bucketlist=bucketlist_id).first()
        db.session.delete(item)
        db.session.commit()
        db.session.close()
        return {
            "message": "Item ID:{} deleted from Bucketlist ID:{}".format(id, bucketlist_id)
            }
    