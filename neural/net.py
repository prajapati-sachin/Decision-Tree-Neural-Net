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

batch = 50
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
  return 1 / (1 + np.exp(-x))


def forwardpass(X):
	examples = X.shape[0]
	temp = X.transpose()
	for i in range(len(layers)):
		temp = sigmoid((Weights[i].dot(temp)) + np.repeat(Bias[i], examples, axis=1))
	return temp

# print(Xtrain[0].reshape(1, 85))

print(forwardpass(Xtrain[0:5].reshape(5, 85)))


# x = Bias[2]

# x = np.repeat(x, 3, axis=1)

# print(x)














