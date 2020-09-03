from flask import Flask, request, make_response, send_file, jsonify
from flask_cors import CORS

import pyttsx3
import tempfile
import re
import os
import json

# This FLASK server is intended to emulate the MARY-TTS API.
app = Flask("pyttsx3")
CORS(app)

# Initialise the engine - On Windows it'll hook into the Microsoft Speech API.
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.stop()

#----------------------------------------------------------------
# Primary URL to obtain WAV files.

@app.route("/process")
def process():
    text = request.args["INPUT_TEXT"]
    selectedVoice = 0
    rate = 175
    if 'VOICE' in request.args:   
        selectedVoice = int(request.args["VOICE"])
    if 'RATE' in request.args:
        rate = int(request.args["RATE"])

    wavFile = generateWavFile(text, selectedVoice, rate)
    wavData = None

    with open(wavFile, "rb") as wav:
        wavData = wav.read()
        wav.close()

    if (wavData is not None):
        try:
            response = make_response()
            response.headers["Content-Type"] = "audio/wav"
            response.data = wavData

            # Remove the file on the disk, we don't need it on the server.
            os.remove(wavFile)
            return response
        except Exception as e:
            return str(e)

    return str("!!! ERROR: Failed to synthesize speech.")

#----------------------------------------------------------------

@app.route("/voices")
def returnVoices():
    availableVoices = {}
    voiceId = 0
    for voice in voices:
        availableVoices[voiceId] = voice.name
        voiceId += 1
    return jsonify(availableVoices = availableVoices)

#----------------------------------------------------------------

def selectVoice(voice):
    if (voice >= len(voices)) :
        return 0
    return voice

def generateWavFile(text, voice, rate):
    voice = selectVoice(voice)
    engine.setProperty('voice', voices[voice].id)
    engine.setProperty('rate', rate)
    filename = (re.sub('[^A-Za-z0-9]+', '', text)) + ".wav"
    engine.save_to_file(text, filename)

    # Execute the queued speech commands.
    engine.runAndWait()
    return filename
    
