import os
import json
import uuid
from flask import *
from flask import render_template 
from pitches import generateImage
# creates a Flask application 
app = Flask(__name__) 
app.secret_key = os.getenv('AUDI_SECRET_KEY')

@app.route("/") 
def start(): 
    return render_template('pitches.html')

@app.route('/upload', methods = ['POST'])
def uploadImage():
    filename = str(uuid.uuid4())
    print (filename)
    f = request.get_data()
    with open(f'temp_audio/{filename}.mp3', 'wb') as audio:
        audio.write(f)
    generateImage(filename)
    return send_file(f'temp_images/{filename}.png', mimetype = 'image/png')

@app.route('/uploadpitches', methods = ['POST'])
def uploadPitches():
    filename = str(uuid.uuid4())
    f = request.get_data()
    with open(f'temp_audio/{filename}.mp3', 'wb') as audio:
        audio.write(f)
    pitches = generateImage(filename)
    return jsonify(pitches)

@app.route('/click', methods = ['POST'])
def clicked():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    # extract the name from the request
    return send_file(f'static/{data["name"]}', mimetype = 'image/png')

# run the application 
if __name__ == "__main__": 
    app.run(debug=True)