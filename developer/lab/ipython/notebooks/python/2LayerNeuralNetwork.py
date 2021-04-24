# 2 Layer Neural Network in Numpy



import numpy as np

# X = input of our 3 input XOR gate
* set up the inputs of the neural network (right from the table)
X = np.array( ([0,0,0],[0,0,1],[0,1,0],
    [0,1,1). (1,0,0],[1,0,11,[1,1,01,[1,1,11), dtype=float)
+ y = our output of our neural network
y = np.array(([1], [0], [@], [@], [],
     [0], [0], [1], dtype=float)
             
#what value we want to predict
xPredicted = np.array(([0,0,1]), dtype=float)
             
X = X/np.amax(X, axis=0) # maximum of X input array
# maximum of xPredicted (our input data for the prediction)
xPredicted = xPredicted/np.amax(xPredicted, axis=0)
             
# set up our Loss file for graphing
             
lossFile = open("SumSquared LossList.csv", "W")
             
class Neural_Network (object):
  def __init__(self):
    #parameters
    self.inputLayerSize = 3 # X1, X2, X3
    self.outputLayerSize= 1 # Y1
    self.hiddenLayerSize 4 # Size of the hidden layer
             
    * build weights of each layer
    # set to random values
    * look at the interconnection diagram to make sense of this
    # 3x4 matrix for input to hidden
    self.W1 = 1
             np.random.randn(self.inputLayerSize, self.hiddenlayerSine)
    # 4x1 matrix for hidden layer to output
    self.W2 = 1

             np.random.randn(self.hiddenlayerSize, self.outputLayerSize)
def feedForward(self, X):
    # feedForward propagation through our network
    #dot product of X (input) and first set of 3x4 weights
    self.z = np. dot(X, self.wi)
             
    # the activationSigmoid activation function - neural magia
    o = self.z2 = self.activationSigmoid(self.z.)
             
    # dot product of hidden layer (22) and second set of 4x1 weights
    self.23 = np. dot (self.z2, self.w2)
             
    # final activation function - more neural magic
    o = self.activationSigmoid(self.z3)
    return o
             
def backwardPropagate(self, x, y, o):
 # backward propagate through the network
 # calculate the error in output
 self.o_error = y - o
             
 # apply derivative of activationSigmoid to error
 self.o_delta = self.o_error*self.activationSigmoidPrime(o)
             
 # z2 error: how much our hidden layer weights contributed to output
 # error
 self.z2_error = self.o_delta.dot(self.W2.T)
             
 # applying derivative of activationSigmoid to z2 error
 self.z2_delta = self.z2_error*self.activationSigmoidPrime(self.22)

 # adjusting first set (inputLayer --> hiddenLayer) weights
 self.W1 += X.T.dot (self.22_delta)
 # adjusting second set (hiddenLayer --> outputLayer) weights
 self.W2 ts self.z2.T. dot (self.o_delta)
             
def trainNetwork(self, x, y):
  # feed forward the loop
  O = self.feedForward(X)
  # and then back propagate the values (feedback)
  self.backwardPropagate(x, y, o)
             
  def activationSigmoid(self, s):
    # activation function
    # simple activation Sigmoid curve as in the book
    return 1/(1+np.exp(-s))
             
  def activationSigmoidPrime(self, s):
    # First derivative of activationSigmoid
    # calculus time!
    return s + (1 - s)
             
  def saveSumSquaredLossList(self, i, error):
    lossFile.write(str(i)+","+str(error. tolist())+'\n')
             
  def saveWeights(self):
    # save this in order to reproduce our cool network
    np. savetxt("weightsLayer1.txt", self.W1, fmt="%s")
    np. savetxt("weightsLayer2.txt", self.W2, fmt="%s").
             
  def predictOutput (self):
    print ("Predicted XOR output data based on trained weights: ")
    print ("Expected (X1-X3): \n" + str(xPredicted))
    print ("Output (91): \n" + str(self.feedForward(xPredicted)))
             
myNeural Network = Neural_Network
trainingEpochs = 1000
#trainingEpochs = 100000
             
for i in range(trainingEpochs): # train my Neural Network 1,000 times
  print ("Epoch # " + str(i) + "\n")
  print ("Network Input : \n" + str(x))
  print ("Expected Output of XOR Gate Neural Network: \n" + str(y))
  print ("Actual Output from XOR Gate Neural Network: \n" +
          str(myNeural Network. feedForward()))
  # mean sum squared loss
  Loss = np.mean(np.square(y - myNeuralNetwork. feedForward()))
  myNeural Network.saveSumSquaredLossList(i, Loss)
  print ("Sum Squared Loss: \n" + str(Loss))
  print ("\n")
  myNeural Network.trainNetwork(x, y)
             
myNeural Network.saveWeights()
myNeural Network.predictoutput()
