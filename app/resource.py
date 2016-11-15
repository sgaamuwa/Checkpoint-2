from app.authentication import Authentication
from app.bucketlist import BucketlistItem
from flask import jsonify, request, g, session
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_restful import Resource, reqparse


auth = HTTPBasicAuth()
auth_token = HTTPTokenAuth()


class Register(Resource):
    def post(self):
        """end point for registering user
        returns string detailing success of registration
        """
        response = jsonify({
            'result': Authentication.register_user(request.json)
            })
        response.status_code = 200
        return response


class Login(Resource):
    def post(self):
        """end point for logging in a UserWarning
        returns true or false depending on success of log in
        """
        result = Authentication.login_user(request.json)
        session['logged_in'] = True
        return jsonify({'result': result})


class Bucketlists(Resource):
    decorators = [auth_token.login_required]

    def get(self):
        """end point for listing Bucketlists in the api
        returns all the bucketlists and their items in the database
        """
        parser = reqparse.RequestParser()
        parser.add_argument("q", type=str, help='name to search')
        parser.add_argument("page", type=int, help="page of results")
        parser.add_argument("limit", type=int, help="limit for results")
        args = parser.parse_args()
        return jsonify({"bucketlists": BucketlistItem.list_bucketlists(
            args,
            g.user.id)
            })

    def post(self):
        """end point for creating Bucketlist
        returns the json of the bucketlist created
        """
        return jsonify({
            "response": BucketlistItem.create_bucketlist(
                request.json,
                g.user.id)
            })


class Bucketlist(Resource):
    decorators = [auth_token.login_required]

    def get(self, id):
        """end point for listing a particular bucketlist
        returns a specified bucketlist and its items from the database
        """
        try:
            return jsonify({
                "response": BucketlistItem.get_bucketlist(id, g.user.id)
                })
        except Exception:
            response = jsonify({
                "message": "Unauthorized access for bucketlist"
            })
            response.status_code = 401
            return response
        except:
            response = jsonify({
                "message": "Resource not found"
            })
            response.status_code = 404
            return response

    def put(self, id):
        """end point for updating a particular bucketlist
        returns the bucketlist with its updated information
        """
        try:
            return jsonify({
                "response": BucketlistItem.update_bucketlist(
                    request.json,
                    id,
                    g.user.id)
                })
        except Exception:
            response = jsonify({
                "message": "Unauthorized access for bucketlist"
            })
            response.status_code = 401
            return response
        except:
            response = jsonify({
                "message": "Resource not found"
            })
            response.status_code = 404
            return response

    def delete(self, id):
        """end point for deleting a particular Bucketlist
        returns a message that the delete was successful
        """
        try:
            return jsonify(BucketlistItem.delete_bucketlist(id, g.user.id))
        except Exception:
            response = jsonify({
                "message": "Unauthorized access for bucketlist"
            })
            response.status_code = 401
            return response
        except:
            response = jsonify({
                "message": "Resource not found"
            })
            response.status_code = 404
            return response


class Items(Resource):
    decorators = [auth_token.login_required]

    def post(self, id):
        """end point for creating an item for a certain BucketlistItem
        returns a json of the created item
        """
        try:
            return jsonify(
                BucketlistItem.create_item(request.json, id, g.user.id))
        except Exception:
            response = jsonify({
                "message": "Unauthorized access for bucketlist"
            })
            response.status_code = 401
            return response
        except:
            response = jsonify({
                "message": "Resource not found"
            })
            response.status_code = 404
            return response


class Item(Resource):
    decorators = [auth_token.login_required]

    def put(self, id, item_id):
        """end point for updating a particular item"""
        try:
            return jsonify(
                BucketlistItem.update_item(
                    request.json,
                    item_id,
                    id,
                    g.user.id
                ))
        except Exception:
            response = jsonify({
                "message": "Unauthorized access for bucketlist"
            })
            response.status_code = 401
            return response
        except:
            response = jsonify({
                "message": "Resource not found"
            })
            response.status_code = 404
            return response

    def delete(self, id, item_id):
        """end point for deleting a particular item
        returns a message on the success of deletion"""
        try:
            return jsonify(BucketlistItem.delete_item(item_id, id, g.user.id))
        except Exception:
            response = jsonify({
                "message": "Unauthorized access for bucketlist"
            })
            response.status_code = 401
            return response
        except:
            response = jsonify({
                "message": "Resource not found"
            })
            response.status_code = 404
            return response


class Token(Resource):
    decorators = [auth.login_required]

    def get(self):
        """gets a token for the logged in user"""
        response = jsonify({'token': g.user.generate_auth_token()})
        response.status_code = 200
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
