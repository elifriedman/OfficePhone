from __future__ import with_statement   # Only necessary for Python 2.5
from flask import Flask, request, redirect
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud import TextToSpeechV1

import requests
import argparse
from twisted.python import log
import twilio.twiml
import sys
import json

app = Flask(__name__)
speech_to_text = None
text_to_speech = None

# not working for some reason
def say(resp, text):
    with open("say.wav","wb") as f:
        words = text_to_speech.synthesize(text, accept='audio/wav', voice="en-US_AllisonVoice")
        f.write(words)
    resp.play("say.wav")


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    resp = twilio.twiml.Response()
    # Greet the caller by name
    resp.say("Hi, there!")
    resp.record(maxLength="30", action="/handle-recording")
    return str(resp)

@app.route("/handle-recording", methods=['GET', 'POST'])
def handle_recording():
    """Play back the caller's recording."""

    recording_url = request.values.get("RecordingUrl", None) + ".wav"
    recording = requests.get(recording_url)
    res = speech_to_text.recognize(recording,
                                   content_type='audio/wav',
                                   timestamps=True,
                                   word_confidence=True,
                                   model = "en-US_NarrowbandModel")
    print(json.dumps(res, indent=2))

    resp = twilio.twiml.Response()
    resp.say("Thank you!")
    return str(resp)

# function to check the credentials format
def check_credentials(credentials):
   elements = credentials.split(":")
   if (len(elements) == 2):
      return elements
   else:
      raise argparse.ArgumentTypeError("\"%s\" is not a valid format for the credentials " % credentials)


# function to check that a value is a positive integer
def check_positive_int(value):
    ivalue = int(value)
    if ivalue < 1:
         raise argparse.ArgumentTypeError("\"%s\" is an invalid positive int value" % value)
    return ivalue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='client to do speech recognition using the WebSocket interface to the Watson STT service')
    parser.add_argument('-optout', action='store_true', dest='optOut', help='specify opt-out header so user data, such as speech and hypotheses are not logged into the server')
    args = parser.parse_args()

    log.startLogging(sys.stdout)


    speech_to_text = SpeechToTextV1(
        username='036c1f77-f160-45e1-8602-c774a192df1e',
        password='ptUEUTCuJLM7',
        x_watson_learning_opt_out=args.optOut
    )

    text_to_speech = TextToSpeechV1(
        username='8f72101b-61d9-47c8-869b-0fbe31d7f51e',
        password='bJAL1sl4AF45',
        x_watson_learning_opt_out=args.optOut
    ) 

    app.run(debug=True)
