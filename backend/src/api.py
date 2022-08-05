import os
from turtle import title
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# initialize the datbase
db_drop_and_create_all()


@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        return jsonify({
            'success': True,
            'drinks': [drink.short() for drink in Drink.query.all()]
        }), 200
    except:
        abort(422)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        return jsonify({
            'success': True,
            'drinks': [drink.long() for drink in Drink.query.all()]
        }), 200
    except:
        abort(422)



@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    # get the body from request
    body = request.get_json()

    # get parameters of the drink to be added
    newTitle = body.get('title', None)
    newRecipe = json.dumps(body.get('recipe', None))
    try:
        drink = Drink(title=newTitle, recipe=newRecipe)
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200
    except:
        abort(422)


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('post:drinks')
def edit_drink(payload, id):
    drink = Drink.query.filter_by(id=id).one_or_none()
    # if the drink is not found, rise 404 erro
    if drink is None:
        abort(404)
    
    # get the body from request
    body = request.get_json()

    # get parameters of the drink to be edited
    newTitle = body.get('title', None)
    newRecipe = json.dumps(body.get('recipe', None))
    try:
        if newTitle is not None:
            drink.title = newTitle
        if newRecipe is not None:
            drink.recipe = newRecipe
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200
    except:
        abort(422)


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    drink = Drink.query.filter_by(id=id).one_or_none()
    # if the drink is not found, rise 404 erro
    if drink is None:
        abort(404)
    
    try:
        # delete the drink from database
        drink.delete()
        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except:
        abort(422)


# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        'error': 400,
        "message": "Bad request"
    }), 400

@app.errorhandler(404)
def bad_request(error):
    return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
            }), 404

@app.errorhandler(AuthError)
def handle_auth_error(error):

    response = jsonify(error.error)
    response.status_code = error.status_code
    return response

if __name__ == "__main__":
    app.debug = True
    app.run()
