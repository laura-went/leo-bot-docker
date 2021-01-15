from django.shortcuts import render, HttpResponse, redirect
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

before1=[]
after1= []
name1 = ''
text1 = ''
emotions1 = ''


@csrf_exempt
def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'leo/index2.html', {})

@csrf_exempt
def index3(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'leo/index3.html', {})

@csrf_exempt
def index4(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'leo/index4.html', {})

@csrf_exempt
def index5(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'leo/index5.html', {})

@csrf_exempt
def privacy(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'leo/privacy.html', {})


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
    global before1, after1, name1, text1, emotions1
    json_stuff= json.dumps({'start':'start db'})
    if request.POST.get('q_1','')!='':
        q1b = request.POST.get('q_1','')
        q2b = request.POST.get('q_2','')
        q3b = request.POST.get('q_3','')
        q4b = request.POST.get('q_4','')
        q5b = request.POST.get('q_5','')
        q6b = request.POST.get('q_6','')
        q7b = request.POST.get('q_7','')
        q8b = request.POST.get('q_8','')
        q9b = request.POST.get('q_9','')
        q10b = request.POST.get('q_10','')
        before1 = [q1b,q2b,q3b,q4b,q5b,q6b,q7b,q8b,q9b,q10b]
        return redirect("/index4")
    if request.POST.get('name', False)!=False:
        name1 = request.POST.get('name', False)
        text1 = request.POST.get('text', False)
        emotions1 = request.POST.get('emotions', False)
        return redirect("/index5")
    if request.POST.get('question_9','')=="1":
        q1a = request.POST.get('question_1','')
        q2a = request.POST.get('question_2','')
        q3a = request.POST.get('question_3','')
        q4a = request.POST.get('question_4','')
        q5a = request.POST.get('question_5','')
        q6a = request.POST.get('question_6','')
        q7a = request.POST.get('question_7','')
        q8a = request.POST.get('question_8','')
        q10a = request.POST.get('question_10','')
        q11a = request.POST.get('question_11','')
        q12a = request.POST.get('question_12','')
        q13a = request.POST.get('question_13','')
        q14a = request.POST.get('question_14','')
        q15a = request.POST.get('question_15','')
        q16a = request.POST.get('question_16','')
        q17a = request.POST.get('question_17','')
        after1 = [q1a,q2a,q3a,q4a,q5a,q6a,q7a,q8a,q10a,q11a,q12a,q13a,q14a,q15a,q16a,q17a]
        user = User(name=name1, text=text1, emotions=emotions1, before=before1, after=after1)
        user.save()
        json_stuff = json.dumps({name1: [text1,emotions1]})
        return redirect("/#")
    return redirect("/#")


    # return HttpResponse(status=204)



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
