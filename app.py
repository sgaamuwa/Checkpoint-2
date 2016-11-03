from authentication import authentication
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bucketlist.db"
db = SQLAlchemy(app)

@app.route('/auth/register', methods=['POST'])
def register_user():
    return jsonify({'result': authentication.Authentication.register_user(request.json)})
    
@app.route('/auth/login', methods=['POST'])
def login_user():
    response = ""
    return response

@app.route('/bucketlists/', methods=['POST'])
@auth.login_required
def create_bucketlist():
    pass

@app.route('/bucketlists/', methods=['GET'])
@auth.login_required
def list_bucketlist():
    pass

@app.route('/bucketlists/<id>', methods=['GET'])
@auth.login_required
def get_bucketlist():
    pass

@app.route('/bucketlists/<id>', methods=['PUT'])
@auth.login_required
def update_bucketlist():
    pass

@app.route('/bucketlists/<id>', methods=['DELETE'])
@auth.login_required
def delete_bucketlist():
    pass 

@app.route('/bucketlists/<id>/items/', methods=['POST'])
@auth.login_required
def create_item():
    pass

@app.route('/bucketlists/<id>/items/<item_id>', methods=['PUT'])
@auth.login_required
def update_item():
    pass

@app.route('/bucketlists/<id>/items/<item_id>', methods=['DELETE'])
@auth.login_required
def delete_item():
    pass

if __name__ == "__main__":
    app.run(debug=True)