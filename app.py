# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 15:44:50 2019

@author: Alan John
"""

from flask import Flask,render_template,url_for,request,redirect,flash
from flask_bootstrap import Bootstrap
import pandas as pd
import numpy as np
import cv2 as cv2
import matplotlib.pyplot as plt
import os
import tensorflow as tf
from tensorflow.keras.models import model_from_json
import boto3
from botocore.client import Config
import urllib

ACCESS_KEY_ID = ''
ACCESS_SECRET_KEY = ''
BUCKET_NAME = 'keanu-reeves'

s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)

def get_image(i):
    req = urllib.request.urlopen(i)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, 0) # 'Load it as it is'
    return img

app = Flask(__name__)
Bootstrap(app)

@app.route("/query")
def query():
	print(request.query_string)
	return "no query received",200

app.config["UPLOAD_FOLDER"] = 'https://keanu-reeves.s3.ap-south-1.amazonaws.com/'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG","JPG","JPEG","GIF"]

def allowed_image(filename):
	if not "." in filename:
		return False

	ext = filename.rsplit(".",1)[1]

	if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
		return True
	else:
		return False

@app.route('/',methods=["GET" , "POST"])
def index():
	if request.method == 'POST':
		if 'image' not in request.files :
			flash('No file part')
			return redirect(request.url)
		file = request.files['image']
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_image(file.filename):
			filename = file.filename
			s3.Bucket(BUCKET_NAME).put_object(Key=filename, Body=file , ACL='public-read')
			print(file.filename)
			#loading model
			json = open('models/model2.json','r')
			model = json.read()
			model = model_from_json(model)
			model.load_weights('models/model2.h5')
			i = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
			img = get_image(i)
			img = cv2.resize(img,(200,200))
			img = tf.keras.utils.normalize(img)
			img = img.reshape(1,200,200,1)
			if model.predict_classes(img):
				flash("ITS BREATHTAKING")
			else:
				flash("NOT SO BREATHTAKING")

			return redirect(request.url)
	return render_template('index.html')


if __name__ == '__main__':
	app.secret_key='12345'
	app.run(debug = "true")
