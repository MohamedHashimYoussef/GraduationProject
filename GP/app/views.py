from PIL.Image import Image
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# Create your views here.
from django.conf import settings
import os
import cv2
from .skincancer import image_clean , GLCM
from numpy import asarray
import pandas as pd
import joblib
from PIL import Image
from .BrainTumor.main import Predict_Brain
from .Malaria.malaria import pre_extract
def index(request):
    return render(request, "static_pages/index.html")
@csrf_exempt
def skin(request):
    save_path = os.path.join(settings.MEDIA_ROOT, 'uploads/skin', request.FILES['photo'].name)
    path = default_storage.save(save_path, request.FILES['photo'])
    imgname = request.FILES['photo'].name
    img = cv2.imread('media/uploads/skin/' + imgname)
    img = image_clean.hair_removal(img)
    img = Image.fromarray(img)
    img = image_clean.preprocessing(img)
    df = pd.DataFrame([GLCM.GLCM(img)], columns = ['contrast','homo', 'energy', 'correlation'])
    svc_from_file = joblib.load('app/skincancer/saved_model_pkl.pkl')  # LOADING THE SAVED MODEL
    prediction = svc_from_file.predict(df)
    if prediction ==  0 :
        return HttpResponse('false')
    else:
        return HttpResponse('true')

@csrf_exempt
def malaria(request):
    save_path = os.path.join(settings.MEDIA_ROOT, 'uploads/malaria', request.FILES['photo'].name)
    path = default_storage.save(save_path, request.FILES['photo'])
    imgname = request.FILES['photo'].name
    img = cv2.imread('media/uploads/malaria/' + imgname)
    prediction = pre_extract(img)
    print(prediction[0])
    if prediction[0] != 'U' :
        return HttpResponse(prediction[0])
    else:
        return HttpResponse(prediction[0])

@csrf_exempt
def brain(request):
    save_path = os.path.join(settings.MEDIA_ROOT, 'uploads/brain', request.FILES['photo'].name)
    path = default_storage.save(save_path, request.FILES['photo'])
    imgname = request.FILES['photo'].name
    img = cv2.imread('media/uploads/brain/' + imgname)
    res = Predict_Brain(photo=img)
    svc_from_file = joblib.load('app/BrainTumor/SVM_BRAIN.pkl')  # LOADING THE SAVED MODEL
    prediction = svc_from_file.predict(res)
    print(prediction[0])
    if prediction[0] != 'Y':
        return HttpResponse('false')
    else:
        return HttpResponse('true')