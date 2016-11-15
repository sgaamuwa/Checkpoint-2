from datetime import datetime
from models import Bucketlist, Item, User
from app import db


class BucketlistItem(object):
    """BucketList class

    The bucket list class has methods for managing the bucketlists and items
    Bucketlist enables one to create, list, return, update and delete
    bucketlists

    Each bucketlist has list items that can be created, updated and deleted
    using the bucket list class
    """

    def create_bucketlist(data, user_id):
        """creates a bucketlist using information sent using POST"""
        if len(data["name"]) == 0:
            return {"message": "Enter a name for bucketlist"}
        elif len(data["name"]) < 2:
            return {"message": "Bucketlist name is too short"}
        result = Bucketlist.query.all()
        bl_names = [blists.name for blists in result]
        if data["name"] in bl_names:
            return {"message": "bucketlist already exists"}
        user = User.query.filter_by(id=user_id).first()
        bucketlist = Bucketlist(
            name=data["name"],
            date_created=datetime.now(),
            date_modified=datetime.now(),
            created_by=user.id
        )
        user.bucketlists.append(bucketlist)
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

    def list_bucketlists(data, user_id):
        """lists all the bucketlists that are in the database"""
        page = data.get("page", 1)
        limit = data.get("limit", 20)
        bucketlist_list = {}
        if data["q"] is not None:
            bucketlists = Bucketlist.query.filter(
                Bucketlist.name.ilike("%"+data["q"]+"%")
            ).filter_by(created_by=user_id).paginate(page, limit, False)
            if len(bucketlists.items) == 0:
                return {"message": "User has no matching bucketlists"}
        else:
            bucketlists = Bucketlist.query.filter_by(
                created_by=user_id
            ).paginate(page, limit, False)
            if len(bucketlists.items) == 0:
                return {"message": "User has no bucketlists"}
        for bucketlist in bucketlists.items:
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

    def get_bucketlist(data, user_id):
        """returns a particular bucket list and its items"""
        bucketlist = Bucketlist.query.filter_by(id=data).first()
        if bucketlist.created_by != user_id:
            raise Exception("Not the user")
        item_list = []
        for item in bucketlist.items:
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

    def update_bucketlist(data, id, user_id):
        """modifies information for a given bucketlist in the database"""
        if len(data["name"]) == 0:
            return {"message": "Enter a name for bucketlist"}
        elif len(data["name"]) < 2:
            return {"message": "Bucketlist name is too short"}
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if bucketlist.created_by != user_id:
            raise Exception("Not the user")
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

    def delete_bucketlist(id, user_id):
        """deletes a particular bucketlist from the database"""
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if bucketlist.created_by != user_id:
            raise Exception("Not the user")
        Bucketlist.query.filter_by(id=id).delete()
        db.session.commit()
        db.session.close()

        return {"message": "Bucketlist ID:{} deleted".format(id)}

    def create_item(data, bucketlist_id, user_id):
        """creates an item in a particular bucketlist"""
        bucketlist = Bucketlist.query.filter_by(id=bucketlist_id).first()
        if bucketlist.created_by != user_id:
            raise Exception("Not the user")
        if len(data["name"]) == 0:
            return {"message": "Enter a name for bucketlist item"}
        elif len(data["name"]) < 2:
            return {"message": "Item name is too short"}
        result = Item.query.all()
        item_names = [items.name for items in result]
        if data["name"] in item_names:
            return {"message": "item already exists"}
        item = Item(
            name=data["name"],
            date_created=datetime.now(),
            date_modified=datetime.now(),
            done=False,
            bucketlist=bucketlist.id
        )
        bucketlist.items.append(item)
        bucketlist.date_modified = datetime.now()
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

    def update_item(data, id, bucketlist_id, user_id):
        """updates a specified item in a particular bucketlist"""
        if data["done"] != ("true" or "false"):
            return {"message": "done is either true or false"}
        bucketlist = Bucketlist.query.filter_by(id=bucketlist_id).first()
        if bucketlist.created_by != user_id:
            raise Exception("Not the user")
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

    def delete_item(id, bucketlist_id, user_id):
        """deletes a specified item in a particular bucketlist"""
        item = Item.query.filter_by(id=id, bucketlist=bucketlist_id).first()
        if item.bucketlists.created_by != user_id:
            raise Exception("Not the user")
        db.session.delete(item)
        db.session.commit()
        db.session.close()
        return {
            "message": "Item ID:{} deleted from Bucketlist ID:{}".format(
                id,
                bucketlist_id)
            }
