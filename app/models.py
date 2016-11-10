from app.app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(db.Model):
    """User Model class
    This class defines database fields for the users of the system
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(250), nullable=False)
    password_hash = db.Column(db.String(250))
    bucketlists = db.relationship("Bucketlist", backref="user", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_in=expires_in)
        return s.dumps({"id": self.id}).decode("utf-8")
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])
        

class Bucketlist(db.Model):
    """Bucketlist Model class
    This class defines database fields for the bucketlists
    """
    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    date_created = db.Column(db.DateTime(True), nullable=False)
    date_modified = db.Column(db.DateTime(True), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    items = db.relationship('Item', backref="bucketlists", lazy="dynamic")


class Item(db.Model):
    """Item Model class
    This class defines database fields for the items in the bucketlists
    """
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    date_created = db.Column(db.DateTime(True), nullable=False)
    date_modified = db.Column(db.DateTime(True), nullable=True)
    done = db.Column(db.Boolean, nullable=False)
    bucketlist = db.Column(db.Integer, db.ForeignKey('bucketlist.id', ondelete='CASCADE'), nullable=False)

db.create_all()