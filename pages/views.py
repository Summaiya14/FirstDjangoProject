from django.http import HttpResponse
from django.shortcuts import render
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
# To install this module, run:
# python -m pip install Pillow
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person

# Create your views here.
def home_view(request, *args, **kwargs):
    #print(args, kwargs)
    #print(request.user)
    #return HttpResponse("<h1>Hello Summaiya</h1>")
    return render(request, "home.html", {})

def contact_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Hello Contact</h1>")
    return render(request, "contact.html", {})

def about_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Hello Contact</h1>")
    return render(request, "about.html", {})

def expression_view(request):
    a = int(request.POST['text1'])
    b = int(request.POST['text2'])
    c = a + b
    return render(request, "output.html", {"result": c})

def face_view(request):
    KEY = "2cde4012d41d4fc68b38fa20f8633e2d"
    ENDPOINT = "https://native-face-recognition.cognitiveservices.azure.com/"
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
    
    single_face_image_url = 'https://www.biography.com/.image/t_share/MTQ1MzAyNzYzOTgxNTE0NTEz/john-f-kennedy---mini-biography.jpg'
    single_image_name = os.path.basename(single_face_image_url)
    detected_faces = face_client.face.detect_with_url(url=single_face_image_url, detection_model='detection_03')
    if not detected_faces:
        raise Exception('No face detected from image {}'.format(single_image_name))
    print('Detected face ID from', single_image_name, ':')
    for face in detected_faces: print (face.face_id)
    print()
    
    first_image_face_ID = detected_faces[0].face_id

    def getRectangle(faceDictionary):
        rect = faceDictionary.face_rectangle
        left = rect.left
        top = rect.top
        right = left + rect.width
        bottom = top + rect.height
        return ((left, top), (right, bottom))
        
    response = requests.get(single_face_image_url)
    img = Image.open(BytesIO(response.content))
    print('Drawing rectangle around face... see popup for results.')
    draw = ImageDraw.Draw(img)
    
    for face in detected_faces:
        draw.rectangle(getRectangle(face), outline='red')
        
    img.show()
    
    multi_face_image_url = "http://www.historyplace.com/kennedy/president-family-portrait-closeup.jpg"
    multi_image_name = os.path.basename(multi_face_image_url)
    
    detected_faces2 = face_client.face.detect_with_url(url=multi_face_image_url, detection_model='detection_03')
    second_image_face_IDs = list(map(lambda x: x.face_id, detected_faces2))
    
    similar_faces = face_client.face.find_similar(face_id=first_image_face_ID, face_ids=second_image_face_IDs)
    if not similar_faces:
        print('No similar faces found in', multi_image_name, '.')
        
    else:
        print('Similar faces found in', multi_image_name + ':')
        for face in similar_faces:
            first_image_face_ID = face.face_id
            face_info = next(x for x in detected_faces2 if x.face_id == first_image_face_ID)
            if face_info:
                print('  Face ID: ', first_image_face_ID)
                print('  Face rectangle:')
                print('    Left: ', str(face_info.face_rectangle.left))
                print('    Top: ', str(face_info.face_rectangle.top))
                print('    Width: ', str(face_info.face_rectangle.width))
                print('    Height: ', str(face_info.face_rectangle.height))
                
    return render(request, "face.html")

