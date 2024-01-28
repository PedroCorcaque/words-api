from lib.postgre_connection import PostgreeDatabase
from flask import Flask, jsonify

import uuid

app = Flask(__name__)

## DB Connection
def get_db_connection():
    try:
        return PostgreeDatabase()
    except Exception as exception:
        raise Exception("Could not connect with the database") from exception

@app.route("/random")
def get_random():
    try:
        with get_db_connection() as conn:
            the_random_word = conn.find_random()
            if not the_random_word:
                return jsonify({ "error": "No words in the database" }), 500
            return jsonify(the_random_word), 200
    except Exception as exception:
        return jsonify({ "error": str(exception) }), 500
    
@app.route("/by_id/<string:id>")
def get_by_id(id):
    try:
        uuid_obj = uuid.UUID(id)
    except ValueError:
        return jsonify({ "error": "Invalid UUID format" }), 400
    
    try:
        with get_db_connection() as conn:
            the_word = conn.find_by_id(uuid_obj)
            if not the_word:
                return jsonify({ "error": f"Could not find the word with the UUID: {id}" }), 404
            return jsonify(the_word), 200
    except Exception as exception:
        return jsonify({ "error": str(exception) }), 500
    
if __name__ == "__main__":
    app.run()
