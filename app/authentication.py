from app.models import User
from app.app import db


class Authentication(object):
    """Authentication class

    The authentication class is used to manage users of the System
    Users can be registered with a username and password and added to
    the database
    Logs in users into the system
    Verifies passwords and token keys for users
    """

    def register_user(user_data):
        """registers and adds new users the database"""
        if len(user_data['username']) == 0:
            return "username required"
        elif len(user_data['username']) < 4:
            return "username is too short"
        elif len(user_data['password']) == 0:
            return "password required"
        elif len(user_data['password']) < 4:
            return "password is too short"
        user = User(username=user_data['username'])
        # give the user password a hash value and store it
        user.set_password(password=user_data['password'])
        result = User.query.all()
        usernames = [users.username for users in result]
        if user_data["username"] in usernames:
            return "username already exists"
        if user in User.query.filter_by(username=user_data['username']):
            status = "success"
        try:
            db.session.add(user)
            db.session.commit()
            status = 'success'
        except:
            status = 'this user is already registered'
        db.session.close()
        return status

    def login_user(user_data):
        """logs in users to the System
        returns an error if the credentials are not valid
        """
        if len(user_data['username']) == 0:
            return "username required"
        elif len(user_data['password']) == 0:
            return "password required"
        user = User.query.filter_by(username=user_data['username']).first()
        # check if the user and password exist and are right
        if user and user.verify_password(user_data['password']):
            return True
        else:
            return False

    def verify_user(username, password):
        """checks if a user exists and verifies their password"""
        user = User.query.filter_by(username=username).first()
        if not user or not user.verify_password(password):
            return None
        return user

    def verify_token(token):
        """verifies tokens used in the system for access"""
        user = User.verify_auth_token(token)
        if user:
            return user
