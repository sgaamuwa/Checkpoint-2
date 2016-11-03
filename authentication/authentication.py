from database.models import User
from app import db
class Authentication(object):
    """Authentication class
    
    The authentication class is used to manage users of the System 
    Users can be registered with a username and password and added to 
    the database
    Logs in users into the system
    """

    def register_user(user_data):
        """registers and adds new users the database"""
        user = User(
            username=user_data['username'],
            password=user_data['password']
        )
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

    def login_user():
        """logs in users to the System
        returns an error if the credentials are not valid
        """
        pass