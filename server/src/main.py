from flask_cors import CORS
from flask import Flask, jsonify, request
from database.db import DB
import uuid

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/peaks'
}

db = DB()

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/peaks', methods=['GET', 'POST'])
def all_peaks():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        db.add_peak(post_data)
        response_object['message'] = 'Peak added!'
    else:
        response_object['peaks'] = db.get_peaks()
    return jsonify(response_object)

@app.route('/peaks/<peak_id>', methods=['PUT', 'DELETE'])
def single_peak(peak_id: int):
    response_object = {'status': 'success'}
    post_data = request.get_json()
    if request.method == 'PUT':
        db.update_peak(peak_id, post_data)
        response_object['message'] = 'Peak updated!'
    if request.method == 'DELETE':
        db.remove_peak(peak_id)
        response_object['peak_id'] = 'Peak removed!'
    return jsonify(response_object)

if __name__ == '__main__':
    app.run()