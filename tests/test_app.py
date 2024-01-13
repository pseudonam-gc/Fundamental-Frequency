import pytest
from app import flaskApp

@pytest.fixture
def client():
    flaskApp.config['TESTING'] = True
    with flaskApp.test_client() as client:
        yield client

def test_start(client):
    response = client.get('/')
    assert response.status_code == 200

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.data == b'OK'

def test_uploadPitches(client):
    #TODO: actually test the return values
    data = {'file': open('temp_audio/tf.mp3', 'rb')}
    response = client.post('/uploadpitches', data=data)
    assert response.status_code == 200

def test_uploadPitchesNamed(client):
    response = client.post('/uploadpitchesnamed', json={'name': 'tf'})
    assert response.status_code == 200
    # convert the response to a list of timed pitches
    response = response.data.decode("utf-8")
    pitches = "[[0.0,448.3529890199268],[0.04081632653061224,441.26743480897517],"
    assert response[:len(pitches)] == pitches