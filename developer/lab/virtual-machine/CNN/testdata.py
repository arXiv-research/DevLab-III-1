#import libraries
import numpy as np
import tensorflow as tf
from tensorflow.python.framework import ops
from PIL import Image

print("import complete")
# load model

img width = 150
img_height = 150

class_names = ["Dog", "Cat")
               
model = tf keras.models.load_model(
     "CatsVersusDogs, trained",compile=True)
print (model summary()
       
# do cat single image
imageName = "Cat150x150.jpeg"
test Img = Image.open( imageName)
testimg.load()
data = np.asarray( test Img, dtype="float")
       
data = np.expand_dims(data, axis=0)
singlePrediction = model predict(data, steps=1)
       
NumberElement = singlePrediction argmax()
Element = np.amax(singlePrediction)
print(NumberElement)
print(Element)
print(singlePrediction)
       
print ("Our Network has concluded that the file
        +imageName+" is a "+class_names [Number Element])
print (str(int(Element+100)) + "% Confidence Level")
       
# do dog single image
imageName = "Dog150x150.JPG"
test Img = Image.open(imageName)
testimg.load()
data = np.asarray( test Img, dtype="float" )
       
data = np.expand_dims(data, axis=0)
singlePrediction = model.predict(data, steps=1)
       
Number Element = singlePrediction argmax()
Element = np.amax(singlePrediction)
print(Number Element)
print(Element)
print(singlePrediction)
       
print ("Our Network has concluded that the file »
        +imageName+" is a "class_names [Number Element])
print (str(int(Element=109)) + " Confidence Level")
