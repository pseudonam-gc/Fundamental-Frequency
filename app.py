import os
import json
import uuid
from flask import *
from flask import render_template 
from pitches import returnPitches

# creates a Flask application 
def create_app():
    app = Flask(__name__) 
    app.secret_key = os.getenv('AUDI_SECRET_KEY')
    return app

def run_app(app):
    app.run(debug=True)

flaskApp = create_app()

@flaskApp.route("/") 
def start(): 
    return render_template('pitches.html')

"""
@flaskApp.route('/upload', methods = ['POST'])
def uploadImage():
    filename = str(uuid.uuid4())
    f = request.get_data()
    with open(f'temp_audio/{filename}.mp3', 'wb') as audio:
        audio.write(f)
    returnPitches(filename)
    return send_file(f'temp_images/{filename}.png', mimetype = 'image/png')"""

@flaskApp.route('/uploadpitches', methods = ['POST'])
def uploadPitches():
    filename = str(uuid.uuid4())
    f = request.get_data()
    with open(f'temp_audio/{filename}.mp3', 'wb') as audio:
        audio.write(f)
    pitches = returnPitches(filename)
    return jsonify(pitches)

@flaskApp.route('/uploadpitchesnamed', methods = ['POST'])
def uploadPitchesNamed():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    filename = data["name"]
    pitches = returnPitches(filename)
    return jsonify(pitches)

@flaskApp.route('/click', methods = ['POST'])
def clicked():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    # extract the name from the request
    return send_file(f'static/{data["name"]}', mimetype = 'image/png')

@flaskApp.route('/health')
def health():
    return "OK"

# run the application 
if __name__ == "__main__": 
    run_app(flaskApp)