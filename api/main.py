from lib.postgre_connection import PostgreeDatabase
from flask import Flask, jsonify, abort

import uuid

app = Flask(__name__)

## DB Connection
def get_db_connection():
    try:
        return PostgreeDatabase()
    except Exception as exception:
        raise Exception("Could not connect with the database") from exception
    
def handle_invalid_uuid():
    return jsonify({ "error": "Invalid UUID format" }), 400

def handle_db_error(exception):
    return jsonify({ "error": f"Database error: {exception}" }), 500

@app.route("/random")
def get_random():
    try:
        with get_db_connection() as conn:
            the_random_word = conn.find_random()
            if not the_random_word:
                return jsonify({ "error": "No words in the database" }), 404
            return jsonify(the_random_word), 200
    except Exception as exception:
        return handle_db_error(exception)
    
@app.route("/find_by_id/<string:id>")
def get_by_id(id):
    try:
        uuid_obj = uuid.UUID(id)
    except ValueError:
        return handle_invalid_uuid()
    
    try:
        with get_db_connection() as conn:
            the_word = conn.find_by_id(uuid_obj)
            if not the_word:
                return jsonify({ "error": f"Word with UUID '{id}' not found" }), 404
            return jsonify(the_word), 200
    except Exception as exception:
        return handle_db_error(exception)
    
@app.route("/word_of_the_day")
def get_word_of_the_day():
    try:
        with get_db_connection() as conn:
            the_word = conn.get_word_of_the_day()
            if not the_word:
                return jsonify({ "error": "Word of the day not found" }), 404
            return jsonify(the_word), 200
    except Exception as exception:
        return handle_db_error(exception)
    
if __name__ == "__main__":
    app.run()
