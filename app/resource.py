from authentication import Authentication 
from bucketlist import BucketlistItem
from app.app import app
from flask import jsonify, request, g, session
from flask_sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()
auth_token = HTTPBasicAuth()

@app.route('/auth/register', methods=['POST'])
def register_user():
    response = jsonify({
        "status": 200, 
        'result': authentication.Authentication.register_user(request.json)
        })
    response.status_code = 200
    return response


@app.route('/auth/login', methods=['POST'])
def login_user():
    result = authentication.Authentication.login_user(request.json)
    session['logged_in'] = True
    return jsonify({'result': result})


@app.route('/bucketlists/', methods=['POST'])
@auth_token.login_required
def create_bucketlist():
    user = request.user
    return jsonify({""})


@app.route('/bucketlists/', methods=['GET'])
@auth_token.login_required
def list_bucketlist():
    pass


@app.route('/bucketlists/<id>', methods=['GET'])
@auth_token.login_required
def get_bucketlist():
    pass


@app.route('/bucketlists/<id>', methods=['PUT'])
@auth_token.login_required
def update_bucketlist():
    pass


@app.route('/bucketlists/<id>', methods=['DELETE'])
@auth_token.login_required
def delete_bucketlist():
    pass 


@app.route('/bucketlists/<id>/items/', methods=['POST'])
@auth_token.login_required
def create_item():
    pass


@app.route('/bucketlists/<id>/items/<item_id>', methods=['PUT'])
@auth_token.login_required
def update_item():
    pass


@app.route('/bucketlists/<id>/items/<item_id>', methods=['DELETE'])
@auth_token.login_required
def delete_item():
    pass


@auth_token.verify_password
def verify_auth_token(token, unused):
    if authentication.Authentication.verify_token(token) is not None:
        g.user = authentication.Authentication.verify_token(token)
        return True
    else:
        return False


@auth.verify_password
def verify_password(username, password):
    if authentication.Authentication.verify_user(username, password) is not None:
        g.user = authentication.Authentication.verify_user(username, password)
        return True
    else:
        return False


@app.route('/token')
@auth.login_required
def get_auth_token():
    return jsonify({'token': g.user.generate_auth_token()})


if __name__ == "__main__":
    app.secret_key = "SHKJY"
    app.run(debug=True)