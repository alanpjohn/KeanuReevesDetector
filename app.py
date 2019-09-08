# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 15:44:50 2019

@author: Vinay Valson
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

# import pandas as pd
# import numpy as np 

# #ML packages
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.extenals import joblib


app = Flask(__name__)
Bootstrap(app)

@app.route("/query")
def query():
	print(request.query_string)
	return "no query received",200

app.config["IMAGE_UPLOADS"] = 'C:/Users/Vinay Valson/Desktop/syndicate/static/img/uploads'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG","JPG","JPEG","GIF"]

def allowed_image(filename):
	if not "." in filename:
		return False

	ext = filename.rsplit(".",1)[1]

	if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
		return True
	else:
		return False
   
# def predict(i):
# #     img = cv2.imread(i,0)
# #     plt.imshow(img, cmap='gray')
# #     plt.show()

# 	#loading model
# 	json = open('models/model2.json','r')
# 	model = json.read()
# 	model = model_from_json(model)
# 	model.load_weights('models/model2.h5')
# 	# img = cv2.imread(i,0)
# 	# plt.imshow(img, cmap='gray')
# 	# plt.show()
# 	img = cv2.imread(i,0)
# 	img = cv2.resize(img,(200,200))
# 	img = tf.keras.utils.normalize(img)
# 	img = img.reshape(1,200,200,1)
# 	if model.predict_classes(img):
# 		return(1)
# 	else:
# 		return(0)
@app.route('/',methods=["GET" , "POST"])
def index():
	if request.method=="POST":
		if request.files:
			image = request.files["image"]
			if image.filename == "":
				print("image must have a filename")
				return redirect(request.url)
			if not allowed_image(image.filename):
				print("That image extension is not allowed")
				return redirect(request.url)

			print(image.filename)
			image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
			print("image saved")
			#loading model
			json = open('models/model2.json','r')
			model = json.read()
			model = model_from_json(model)
			model.load_weights('models/model2.h5')
			i = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
			# img = cv2.imread(i,0)
			# plt.imshow(img, cmap='gray')
			# plt.show()
			img = cv2.imread(i,0)
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
	app.run(debug = True)
