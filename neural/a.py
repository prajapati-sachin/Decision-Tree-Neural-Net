import numpy as np
from sklearn import tree
import sys
import csv
from sklearn.preprocessing import OneHotEncoder
from random import shuffle


Xtrain = []
Ytrain = []


# train = sys.argv[1]
# test = sys.argv[2]
# train_hot = sys.argv[3]
# test_hot = sys.argv[4]


train = "train.data"
test = "test.data"

train_hot = "trainhot.data"
test_hot = "testhot.data"

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
			temp.append(int(row[i]))
		Xtrain.append(temp)
		Ytrain.append(int(row[10]))




with open(test) as fileX:
	x_reader = csv.reader(fileX)
	for row in x_reader:
		temp = []
		for i in range(10):
			temp.append(int(row[i]))
		Xtest.append(temp)
		Ytest.append(int(row[10]))


enc = OneHotEncoder(handle_unknown='ignore')
Xtrain = enc.fit_transform(Xtrain).toarray()
Xtest = enc.fit_transform(Xtest).toarray()

f = open(train_hot, "w")
for i in range(len(Xtrain)):
	for j in range(len(Xtrain[i])):
		f.write(str(Xtrain[i][j]))
		f.write(",")
	f.write(str(Ytrain[i]))
	f.write("\n")
f.close()

d = open(test_hot, "w")
for i in range(len(Xtest)):
	for j in range(len(Xtest[i])):
		d.write(str(Xtest[i][j]))
		d.write(",")
	d.write(str(Ytest[i]))
	d.write("\n")
d.close()


# ####################################################
# layers.append(outputs)

# totallayer = len(layers)
# hiddenlayer = len(layers)-1

# Weights = []
# Bias = []

# io = []

# for i in range(len(layers)):
# 	if(i==0):
# 		io.append((layers[0], inputs))
# 	else:
# 		io.append((layers[i], layers[i-1]))

# # print(layers)
# # print(io)

# for i in range(len(layers)):
# 	Weights.append(np.random.normal(0, 1, io[i]))
# 	Bias.append(np.array([np.random.normal(0, 1, layers[i])]).transpose())

# # print(Bias[2])
# def sigmoid(x):
# 	temp = np.where(x >= 0, 1 / (1 + np.exp(-x)), np.exp(x) / (1 + np.exp(x)))
# 	return temp

# def stable_softmax(X):
#     exps = np.exp(X - np.max(X, axis=0, keepdims=True))
#     return exps / np.sum(exps, axis=0, keepdims=True)

# def EncodeY(y):
# 	temp = [0]*10
# 	temp[y]=1
# 	return temp

# def forwardpass(X):
# 	examples = X.shape[0]
# 	Ojs = []
# 	temp = X.transpose()
# 	Ojs.append(temp)
# 	for i in range(len(layers)):
# 		if(i==len(layers)-1):
# 			# temp1 = np.exp((Weights[i].dot(temp)) + np.repeat(Bias[i], examples, axis=1))			
# 			# sum1 = np.sum(temp1, axis=0)
# 			# temp = np.true_divide(temp1, sum1)
# 			temp = stable_softmax((Weights[i].dot(temp)) + np.tile(Bias[i], examples))
# 			Ojs.append(temp)
# 			# print(np.sum(temp, axis=0))
# 		else:
# 			temp = sigmoid((Weights[i].dot(temp)) + np.tile(Bias[i], examples))
# 			Ojs.append(temp)
# 	return Ojs

# # print(Xtrain[0].reshape(1, 85))

# # print(forwardpass(Xtrain[0:3].reshape(3, 85))[2])


# # x = Bias[2]

# # x = np.repeat(x, 3, axis=1)

# # print(Xtrain.shape)

# def testing(X):
# 	examples = X.shape[0]
# 	# Oj = []
# 	temp = X.transpose()
# 	for i in range(len(layers)):
# 		if(i==len(layers)-1):
# 			# temp1 = np.exp((Weights[i].dot(temp)) + np.repeat(Bias[i], examples, axis=1))			
# 			# sum1 = np.sum(temp1, axis=0)
# 			# temp = np.true_divide(temp1, sum1)
# 			temp = stable_softmax((Weights[i].dot(temp)) + np.tile(Bias[i], examples))
# 			# Oj.append(temp)
# 			# print(np.sum(temp, axis=0))
# 		else:
# 			temp = sigmoid((Weights[i].dot(temp)) + np.tile(Bias[i], examples))
# 	# np.argmax(Oj, axis=0)
# 	return np.argmax(temp, axis=0)


# def backwardpass(X, Y, Outputs):
# 	examples = X.shape[0]
# 	temp = X.transpose()
# 	labels = []
# 	delW = []
# 	delB = []
# 	for i in range(len(Y)):
# 		labels.append(EncodeY(Y[i]))
# 	labels = np.array(labels)
# 	labels = labels.transpose()
# 	lastindex = len(layers)
# 	delJ = (Outputs[lastindex] - labels)
# 	# print(delJ.shape)
# 	# print(Outputs[lastindex-1].shape)
# 	delW.append(delJ.dot(Outputs[lastindex-1].transpose()))
# 	delB.append(np.sum(delJ, axis=1, keepdims=True))
# 	# print(delW[0].shape)
# 	# print(delB[0].shape)
# 	# print(Outputs[0].shape)
# 	for i in range(lastindex-2, -1, -1):
# 		# print(delJ.shape)
# 		units = layers[i]
# 		tempW = ((Weights[i+1].transpose()).dot(delJ))*((Outputs[i+1]*(1-(Outputs[i+1]))))
# 		delJ = tempW
# 		# print(i, tempW.shape)
# 		# print(i, Outputs[i].shape)
# 		delW.append(tempW.dot(Outputs[i].transpose()))
# 		delB.append(np.sum(delJ, axis=1, keepdims=True))

# 		# print(i, delW[i].shape)
# 		# print(i, delB[i].shape)

# 	# print(delW[1].shape)
# 	# print(delB[1].shape)
# 	# print(delW[2].shape)
# 	# print(delB[2].shape)
# 	delW.reverse()
# 	delB.reverse()

# 	for i in range(len(Weights)):
# 		Weights[i] = Weights[i] - 0.1*(delW[i]) 
# 		Bias[i] = Bias[i] - 0.1*(delB[i]) 


# 	# return delJ


# oo = forwardpass(Xtrain[0:3].reshape(3, 85))
# # (backwardpass((Xtrain[0:3].reshape(3, 85)), Ytrain[0:3], oo))

# # print((Ytrain[0:3]))


# def oneEpoch():
# # 	# c = list(zip(Xtrain, Ytrain))
# # 	# random.shuffle(c)
# # 	# a, b = zip(*c)
# # 	# print((a[0]))
# # 	# Given list1 and list2
# 	a = []
# 	b = []
# 	index_shuf = list(range(Xtrain.shape[0]))
# 	# index_shuf = list(range(5))
# 	shuffle(index_shuf)
# 	for i in index_shuf:
# 	    a.append(Xtrain[i])
# 	    b.append(Ytrain[i])
# # 	# indices = np.arange(Xtrain.shape[0])
# # 	# np.random.shuffle(indices)

# 	# print((a[0]))
# 	# print((b[0:3]))
# 	# newY = np.array(b[(i*batch):(i*batch) + batch])
# 	# print(newY)

# # 	# a = Xtrain[indices]
# # 	# b = Ytrain[indices]
# 	for i in range(batch):
# 		newX = np.array(a[(i*batch):(i*batch) + batch])
# 		newY = (b[(i*batch):(i*batch) + batch])
# 		temp = forwardpass((newX.reshape(batch, 85)))
# 		(backwardpass((newX.reshape(batch, 85)), newY, temp))

# for i in range(500):
# 	if(i%100==0):
# 		print("Epoch: ", i)
# 	oneEpoch()


# # prediction = a.tolist(testing(Xtest))

# Ytest = np.array(Ytest)

# # a = np.array([0,0,1,1,1])   # actual labels
# # b = np.array([1,1,0,0,1])   # predicted labels

# correct = (testing(Xtest) == Ytest)
# accuracy = correct.sum() / correct.size

# print(accuracy)