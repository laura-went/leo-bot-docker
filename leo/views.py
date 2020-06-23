from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sys

from context_recognition import ContextRecognition
from ibm_watson import ToneAnalyzerV3
from ibm_watson.tone_analyzer_v3 import ToneInput
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from joblib import load
from .models import User

import soundfile
import librosa
import pyttsx3
import json
import numpy as np
from scipy.io.wavfile import read as read_wav
import librosa
import speech_recognition as sr

engine = pyttsx3.init()
clf = load('leo/model19.joblib')
clf2 = load('leo/agg.joblib')
vec = load('leo/vec.joblib')
authenticator = IAMAuthenticator('6RDOALhXeOxtJNBvB9DgE7WcpMe_Wda0XeHCg424WD0d')
service = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator)
service.set_service_url('https://gateway-lon.watsonplatform.net/tone-analyzer/api')
context = ContextRecognition()
context.load_corpus("corpus/")
context.load_model()
r = sr.Recognizer()

@csrf_exempt
def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'leo/index.html', {})

@csrf_exempt
#create responding chatbot sentence
def get_sentence(request):
    text = request.POST.get('text', False)
    response, correlation = context.compute_document_similarity(text)
    return HttpResponse(response)

@csrf_exempt
#process incoming speech+text
def get_blob(request):
    data = request.POST.copy()
    video_stream = request.FILES['audio'].read()
    text = request.POST.get('text', False)
    with open('myfile.wav', mode='wb') as f:
        f.write(video_stream)

    text2 = ''
    hellow=sr.AudioFile('myfile.wav')
    with hellow as source:
        audio = r.record(source)
    try:
        text2 = r.recognize_google(audio)
    except Exception as e:
        text2 = e

    emotion = text_emotion(text2)
    prediction = speech_emotion('myfile.wav')
    aggression = agg_detection(text2)
    json_stuff = json.dumps({"list": [prediction, emotion, aggression,text2]})
    return HttpResponse(json_stuff, content_type="application/json")

@csrf_exempt
def get_text(request):
    text = request.POST.get('text', False)
    emotion = text_emotion(text)
    aggression = agg_detection(text)
    json_stuff = json.dumps({"list": ['no voice',emotion, aggression]})
    return HttpResponse(json_stuff, content_type="application/json")

def get_blob_text(request):
    text = request.POST.get('text', False)
    emotion = text_emotion(text)
    aggression = agg_detection(text)
    json_stuff = json.dumps({"list": ["No voice", emotion, aggression]})
    return HttpResponse(json_stuff, content_type="application/json")

@csrf_exempt
def add_to_db(request):
    name1 = request.POST.get('name', False)
    text1 = request.POST.get('text', False)
    emotions1 = request.POST.get('emotions', False)
    user = User(name=name1, text=text1, emotions=emotions1)
    user.save()
    json_stuff = json.dumps({name1: [text1,emotions1]})
    return HttpResponse(json_stuff, content_type="application/json")



# heard emotion
def extract_feature(file_name, mfcc, chroma, mel):

    X,sample_rate= librosa.load(file_name)
    if chroma:
        if len(X.shape) > 1 and X.shape[1] > 1:
            X = X.mean(axis=1)
        stft = np.abs(librosa.stft(X))
    result = np.array([])
    if mfcc:
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
        result = np.hstack((result, mfccs))
    if chroma:
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
        result = np.hstack((result, chroma))
    if mel:
        mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T, axis=0)
        result = np.hstack((result, mel))
    return result


def speech_emotion(file):
    feature = extract_feature(file, mfcc=True, chroma=True, mel=True)
    prediction = clf.predict(feature.reshape(1, -1))
    return prediction[0]


# aggression detection
def predict_aggression1(text,countvector,model):
    return model.predict(countvector.transform([text]))[0]


def agg_detection(text):
    prediction = predict_aggression1(text,vec,clf2)
    return prediction


# read emotion
def text_emotion(text):
    tone_input = ToneInput(text)
    tone_analysis = service.tone(tone_input, content_type='application/json').get_result()
    best_score = 0
    best_emotion = "neutral"
    tones = tone_analysis["document_tone"]
    for tone in tones["tones"]:
        if tone["score"] > best_score:
            best_score = tone["score"]
            best_emotion = tone["tone_id"]
    return best_emotion
