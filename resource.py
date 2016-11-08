from app.authentication import Authentication 
from app.bucketlist import BucketlistItem
from app.app import app, db
from flask import jsonify, request, g, session
from flask.ext.httpauth import HTTPBasicAuth, HTTPTokenAuth


auth = HTTPBasicAuth()
auth_token = HTTPTokenAuth()

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
        "response": BucketlistItem.create_bucketlist(request.json, g.user.username)
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
    try:
        return jsonify({
            "bucketlist": BucketlistItem.get_bucketlist(identifier)
            })
    except:
        response = jsonify({
            "message": "Resource not found"
        })
        response.status_code = 404
        return response


@app.route('/bucketlists/<id>', methods=['PUT'])
@auth_token.login_required
def update_bucketlist(id):
    """end point for updating a particular bucketlist
    returns the bucketlist with its updated information
    """
    try:
        return jsonify({
            "bucketlist": BucketlistItem.update_bucketlist(request.json, id)
            })
    except:
        response = jsonify({
            "message": "Resource not found"
        })
        response.status_code = 404
        return response


@app.route('/bucketlists/<id>', methods=['DELETE'])
@auth_token.login_required
def delete_bucketlist(id):
    """end point for deleting a particular Bucketlist
    returns a message that the delete was successful
    """
    try:
        return jsonify(BucketlistItem.delete_bucketlist(id))
    except:
        response = jsonify({
            "message": "Resource not found"
        })
        response.status_code = 404
        return response


@app.route('/bucketlists/<id>/items/', methods=['POST'])
@auth_token.login_required
def create_item(id):
    """end point for creating an item for a certain BucketlistItem
    returns a json of the created item
    """
    try:
        return jsonify(BucketlistItem.create_item(request.json, id))
    except:
        response = jsonify({
            "message": "Resource not found"
        })
        response.status_code = 404
        return response


@app.route('/bucketlists/<id>/items/<item_id>', methods=['PUT'])
@auth_token.login_required
def update_item(id, item_id):
    """end point for updating a particular item"""
    try:
        return jsonify(BucketlistItem.update_item(request.json, item_id, id))
    except:
        response = jsonify({
            "message": "Resource not found"
        })
        response.status_code = 404
        return response


@app.route('/bucketlists/<id>/items/<item_id>', methods=['DELETE'])
@auth_token.login_required
def delete_item(id, item_id):
    """end point for deleting a particular item
    returns a message on the success of deletion"""
    try:
        return jsonify(BucketlistItem.delete_item(item_id, id))
    except:
        response = jsonify({
            "message": "Resource not found"
        })
        response.status_code = 404
        return response


@auth_token.verify_token
def verify_auth_token(token):
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
    response = jsonify({'token': g.user.generate_auth_token()})
    response.status_code = 200
    return response


if __name__ == "__main__":
    app.secret_key = "SHKJY"
    app.run(debug=True)