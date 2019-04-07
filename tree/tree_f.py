import numpy as np
import sys
import csv
from sklearn import tree
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier


Xtrain = []
Ytrain = []

Xtest = []
Ytest = []

Xval = []
Yval = []

train = "train.csv"
test = "test.csv"
val = "val.csv"

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
				if(i>=6 and i<=11):
					temp.append(float(row[i])+2)
				else:
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
				if(i>=6 and i<=11):
					temp.append(float(row[i])+2)
				else:
					temp.append(float(row[i]))
			Xtest.append(temp)
			Ytest.append(int(row[24]))
		# count+=1		

count = 0
with open(val) as fileX:
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
				if(i>=6 and i<=11):
					temp.append(float(row[i])+2)
				else:
					temp.append(float(row[i]))
			Xval.append(temp)
			Yval.append(int(row[24]))
		# count+=1		


categorical = [1, 2, 3, 5, 6, 7, 8, 9, 10] 

Xfull = Xtrain + Xtest + Xval

enc = OneHotEncoder(categorical_features = categorical)
Xfull = enc.fit_transform(Xfull)

Xtrain = Xfull.toarray()[:len(Xtrain)]
Xtest = Xfull.toarray()[len(Xtrain):len(Xtrain)+len(Xtest)]
Xval = Xfull.toarray()[len(Xtrain)+len(Xtest):]



# classify = tree.DecisionTreeClassifier()
# classify =  classify.fit(Xtrain, Ytrain)


classify = RandomForestClassifier(n_estimators = 50, random_state= 2, max_features=2)
classify = classify.fit(Xtrain, Ytrain)


Ypred = classify.predict(Xtest)

accuracy = accuracy_score(Ytest, Ypred )

print("Accuracy on test: ", accuracy)

############################################
Ypred = classify.predict(Xtrain)

accuracy = accuracy_score(Ytrain, Ypred )

print("Accuracy on test: ", accuracy)


############################################
Ypred = classify.predict(Xval)

accuracy = accuracy_score(Yval, Ypred )

print("Accuracy on test: ", accuracy)
