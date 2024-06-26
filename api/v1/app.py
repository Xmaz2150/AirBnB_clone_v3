#!/usr/bin/python3

"""
Flask entry point
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def clean_up(e):
    """ close storage """
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """ error 404 """
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    import os

    host = os.getenv('HBNB_API_HOST') if os.getenv('HBNB_API_HOST') else '0.0.0.0'
    port = os.getenv('HBNB_API_PORT') if os.getenv('HBNB_API_PORT') else 5000
    app.run(host=host, port=port, threaded=True)
