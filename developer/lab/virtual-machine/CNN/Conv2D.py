#import libraries
import numpy as np
import matplotlib.pyplot as pit
import matplotlib. image as mpimg
import seaborn as sns
import tensorflow as tf
from tensorflow.python, framework import ops
from tensorflow.examples tutorials.mist import input data
from PIL import Image
from tensor flow.keras.preprocessing. image import ImageDataBenerator

from tensorflow.keras.layers import *

#load data

img_width = 150
img_height = 150
train data dir = 'data/train'
valid_data_dir = 'data/validation'

datagen = ImageDataGenerator (rescale = 1./255)

train_generator = datagen.flow_from_directory(
                directory=train_data_dir,
                target_size=(img_width, img_height),
                classes=['dogs','cats'],
                class_mode='binary'
                batch size=16)

validation_generator = datagen.flow_from_directory(directory=valid_data_dir,
                target size=(img_width, img_height),
                classes=['dogs', 'cats'],
                class_mode='binary'
                batch_size=32)

# build model

model = tf.keras.Sequential()


model.add(Conv2D(32,(3,3), input_shape=(150,150,3), padding='same,
                 activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Dropout(0.25))
model.add(Flatten()
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))
          
model.compile(optimizer=tf.train. AdamOptimizer().
                              loss='sparse_categorical_crossentropy',
                              metrics=['accuracy'])
          
print (model.summary())
       
#train model
       
print('starting training....')
history = model.fit_generator (generator=train_generator,
        steps_per_epoch=2048 // 16, epochs=20,
        validation_data=validation_generator, validation_steps=832//16)
      
print('training finished!!)
      
      
# save coefficients
      
model.save("CatsVersusDogs.trained")
      
# Get training and test loss histories
training_loss = history history['loss']
accuracy = history history['acc']
# Create count of the number of epochs
epoch_count = range(1, len(training loss) + 1)
      
# Visualize loss history
plt.figure(0)
plt.plot(epoch_count, training loss, 'r--')
plt.plot(epoch_count, accuracy, 'b--')
pit.legend( "Training Loss', 'Accuracy'])
plt.xlabel('Epoch)
plt.ylabel('History')
plt.grid(True)
plt.show(block=True);
