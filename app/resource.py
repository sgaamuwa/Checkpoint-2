from authentication import Authentication 
from bucketlist import BucketlistItem
from app import app
from flask import jsonify, request, g, session
from flask_sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()
auth_token = HTTPBasicAuth()

@app.route('/auth/register', methods=['POST'])
def register_user():
    """end point for registering user
    returns string detailing success of registration
    """
    response = jsonify({
        "status": 200, 
        'result': Authentication.register_user(request.json)
        })
    response.status_code = 200
    return response


@app.route('/auth/login', methods=['POST'])
def login_user():
    """end point for logging in a UserWarning
    returns true or false depending on success of log in
    """
    result = Authentication.login_user(request.json)
    session['logged_in'] = True
    return jsonify({'result': result})


@app.route('/bucketlists/', methods=['POST'])
@auth_token.login_required
def create_bucketlist():
    """end point for creating Bucketlist
    returns the json of the bucketlist created 
    """
    return jsonify({
        "response": BucketlistItem.create_bucketlist(request.json, g.user)
        })


@app.route('/bucketlists/', methods=['GET'])
@auth_token.login_required
def list_bucketlist():
    """end point for listing Bucketlists in the api
    returns all the bucketlists and their items in the database
    """
    return jsonify({"bucketlists": BucketlistItem.list_bucketlists()})


@app.route('/bucketlists/<identifier>', methods=['GET'])
@auth_token.login_required
def get_bucketlist(identifier):
    """end point for listing a particular bucketlist
    returns a specified bucketlist and its items from the database
    """
    return jsonify({"bucketlist": BucketlistItem.get_bucketlist(identifier)})


@app.route('/bucketlists/<id>', methods=['PUT'])
@auth_token.login_required
def update_bucketlist(id):
    """end point for updating a particular bucketlist
    returns the bucketlist with its updated information
    """
    return jsonify({
        "bucketlist": BucketlistItem.update_bucketlist(request.json, id)
        })


@app.route('/bucketlists/<id>', methods=['DELETE'])
@auth_token.login_required
def delete_bucketlist(id):
    """end point for deleting a particular Bucketlist
    returns a message that the delete was successful
    """
    return jsonify(BucketlistItem.delete_bucketlist(id))


@app.route('/bucketlists/<id>/items/', methods=['POST'])
@auth_token.login_required
def create_item(id):
    """end point for creating an item for a certain BucketlistItem
    returns a json of the created item
    """
    return jsonify(BucketlistItem.create_item(request.json, id))


@app.route('/bucketlists/<id>/items/<item_id>', methods=['PUT'])
@auth_token.login_required
def update_item():
    """end point for updating a particular item"""
    pass


@app.route('/bucketlists/<id>/items/<item_id>', methods=['DELETE'])
@auth_token.login_required
def delete_item(id, item_id):
    """end point for deleting a particular item
    returns a message on the success of deletion"""
    return jsonify(BucketlistItem.delete_item(item_id, id))


@auth_token.verify_password
def verify_auth_token(token, unused):
    """verifies the token used to access the api"""
    if Authentication.verify_token(token) is not None:
        g.user = Authentication.verify_token(token)
        return True
    else:
        return False


@auth.verify_password
def verify_password(username, password):
    """verifies the username and password for logging in to the system"""
    if Authentication.verify_user(username, password) is not None:
        g.user = Authentication.verify_user(username, password)
        return True
    else:
        return False


@app.route('/token')
@auth.login_required
def get_auth_token():
    """gets a token for the logged in user"""
    return jsonify({'token': g.user.generate_auth_token()})


if __name__ == "__main__":
    app.secret_key = "SHKJY"
    app.run(debug=True)