import numpy as np
from sklearn import tree
import sys
import csv

Xtrain = []
Ytrain = []

Xtest = []
Ytest = []

train = "train.csv"
test = "test.csv"

count = 0

with open(train) as fileX:
	x_reader = csv.reader(fileX)
	for row in x_reader:
		temp = []
		if(count<2):
			count+=1
			continue
		else:
			for i in range(1,24):
				temp.append(float(row[i]))
			Xtrain.append(temp)
			Ytrain.append(int(row[24]))

count = 0

with open(test) as fileX:
	x_reader = csv.reader(fileX)
	for row in x_reader:
		# print(row)
		temp = []
		if(count<2):
			count+=1
			continue
		else:
			# print("done")
			for i in range(1,24):
				temp.append(float(row[i]))
			Xtest.append(temp)
			Ytest.append(int(row[24]))
		# count+=1		


# print((Xtrain[0]))
# print((Ytrain[0]))
# print((Xtest[0]))
# print((Ytest[0]))

classify = tree.DecisionTreeClassifier()
classify =  classify.fit(Xtrain, Ytrain)

Ypred = classify.predict(Xtest)

correct = (Ypred==Ytest)

accuracy = correct.sum()/correct.size

print(accuracy)
