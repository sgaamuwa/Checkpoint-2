from app import db

class User(db.Model):
    """User Database class
    This class defines database fields for the users of the system
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)

class Bucketlist(db.Model):
    """Bucketlist Database class
    This class defines database fields for the bucketlists
    """
    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    date_created = db.Column(db.DateTime(True), nullable=False)
    date_modified = db.Column(db.DateTime(True), nullable=True)
    created_by = db.Column(db.String(250), nullable=False)

class Item(db.Model):
    """Item Database class
    This class defines database fields for the items in the bucketlists
    """
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    date_created = db.Column(db.DateTime(True), nullable=False)
    date_modified = db.Column(db.DateTime(True), nullable=True)
    done = db.Column(db.Boolean, nullable=False)

db.create_all()