import numpy as np
from sklearn import tree
import sys
import csv
from sklearn.preprocessing import OneHotEncoder

Xtrain = []
Ytrain = []

train = "train.data"
test = "test.data"

Xtest = []
Ytest = []

batch = 100
inputs = 85
layers = [100, 50]
outputs = 10

##################################################
with open(train) as fileX:
	x_reader = csv.reader(fileX)
	for row in x_reader:
		temp = []
		for i in range(10):
			temp.append(float(row[i]))
		Xtrain.append(temp)
		Ytrain.append(int(row[10]))




# with open(test) as fileX:
# 	x_reader = csv.reader(fileX)
# 	for row in x_reader:
# 		temp = []
# 		for i in range(10):
# 			temp.append(float(row[i]))
# 		Xtest.append(temp)
# 		Ytest.append(int(row[10]))


enc = OneHotEncoder(handle_unknown='ignore')
Xtrain = enc.fit_transform(Xtrain).toarray()


####################################################
layers.append(outputs)

totallayer = len(layers)
hiddenlayer = len(layers)-1

Weights = []
Bias = []

io = []

for i in range(len(layers)):
	if(i==0):
		io.append((layers[0], inputs))
	else:
		io.append((layers[i], layers[i-1]))

# print(layers)
# print(io)

for i in range(len(layers)):
	Weights.append(np.random.normal(0, 1, io[i]))
	Bias.append(np.array([np.random.normal(0, 1, layers[i])]).transpose())

# print(Bias[2])
def sigmoid(x):
	temp = np.where(x >= 0, 1 / (1 + np.exp(-x)), np.exp(x) / (1 + np.exp(x)))
	return temp

def stable_softmax(X):
    exps = np.exp(X - np.max(X, axis=0, keepdims=True))
    return exps / np.sum(exps, axis=0)

def EncodeY(y):
	temp = [0]*10
	temp[y]=1
	return temp

def forwardpass(X):
	examples = X.shape[0]
	Ojs = []
	temp = X.transpose()
	Ojs.append(temp)
	for i in range(len(layers)):
		if(i==len(layers)-1):
			# temp1 = np.exp((Weights[i].dot(temp)) + np.repeat(Bias[i], examples, axis=1))			
			# sum1 = np.sum(temp1, axis=0)
			# temp = np.true_divide(temp1, sum1)
			temp = stable_softmax((Weights[i].dot(temp)) + np.repeat(Bias[i], examples, axis=1))
			Ojs.append(temp)
			# print(np.sum(temp, axis=0))
		else:
			temp = sigmoid((Weights[i].dot(temp)) + np.repeat(Bias[i], examples, axis=1))
			Ojs.append(temp)
	return Ojs

# print(Xtrain[0].reshape(1, 85))

# print(forwardpass(Xtrain[0:3].reshape(3, 85))[2])


# x = Bias[2]

# x = np.repeat(x, 3, axis=1)

# print(Xtrain.shape)

def backwardpass(X, Y, Outputs):
	examples = X.shape[0]
	temp = X.transpose()
	labels = []
	delW = []
	delB = []
	for i in range(len(Y)):
		labels.append(EncodeY(Y[i]))
	labels = np.array(labels)
	labels = labels.transpose()
	lastindex = len(layers)
	delJ = (Outputs[lastindex] - labels)
	# print(delJ.shape)
	# print(Outputs[lastindex-1].shape)
	delW.append(delJ.dot(Outputs[lastindex-1].transpose()))
	delB.append(np.sum(delJ, axis=1, keepdims=True))
	# print(delW[0].shape)
	# print(delB[0].shape)
	# print(Outputs[0].shape)
	for i in range(lastindex-2, -1, -1):
		# print(delJ.shape)
		units = layers[i]
		tempW = ((Weights[i+1].transpose()).dot(delJ))*((Outputs[i+1]*(1-(Outputs[i+1]))))
		delJ = tempW
		# print(i, tempW.shape)
		# print(i, Outputs[i].shape)
		delW.append(tempW.dot(Outputs[i].transpose()))
		delB.append(np.sum(delJ, axis=1, keepdims=True))

		# print(i, delW[i].shape)
		# print(i, delB[i].shape)

	# print(delW[1].shape)
	# print(delB[1].shape)
	# print(delW[2].shape)
	# print(delB[2].shape)
	delW.reverse()
	delB.reverse()

	for i in range(len(Weights)):
		Weights[i] = Weights[i] - 0.1*(delW[i]) 
		Bias[i] = Bias[i] - 0.1*(delB[i]) 


	# return delJ


oo = forwardpass((Xtrain[0:3].reshape(3, 85)))

(backwardpass((Xtrain[0:3].reshape(3, 85)), Ytrain[0:3], oo))








