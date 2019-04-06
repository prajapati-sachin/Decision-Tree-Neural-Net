import sys
import csv
import math
import time
import numpy as np
import random
# import scipy
# import sklearn.metrics
from sklearn import tree
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score, confusion_matrix


def sig(x):
	return (1 / (1 + np.exp(-x)))

# def sig(x):
# 	return np.where(x >= 0, 1 / (1 + np.exp(-x)), np.exp(x) / (1 + np.exp(x)))

def exp(x):
	return  np.exp(x)

def softmax(x):
    e_x = np.exp(x - np.max(x,axis=0,keepdims = True))
    return e_x / np.sum(e_x,axis=0,keepdims=True) 

def generateY(outputY,ylist):
	y = ylist[0]
	mn = np.zeros([outputY,1])
	mn[y][0] = 1
	for i in range(1,len(ylist)):
		n = np.zeros([outputY,1])
		y = ylist[i]
		n[y][0] = 1
		mn = np.concatenate((mn, n), axis=1)

	return mn




# filename1 = sys.argv[1]
# filename2 = sys.argv[2]
# part = int(sys.argv[3])
filename1 = "poker-hand-training-true.data"
filename2 = "poker-hand-testing.data"
filename3 = "config_file"

file1 = open("filename3","r") 
ff = file1.readlines()

input_count = ff[0]
output_count = ff[1] 
batch_count = ff[2]
hidden_count = ff[3]
file1.close() 


part =2
alpha = 0.1

def reader(a):
	ret = []
	xlist = []
	ylist = []
	m=0
	with open(a, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			xl = []
			i = 0
			for col in row:
				
				if(i==10):
					x = int(col)
					ylist.append(x)
				else:
					x = int(col)    
					xl.append(x)
				i+=1

			xlist.append(xl)
			m+=1
			# if(a==filename2):
			# 	if(m>=100):
			# 		break
	ret.append(xlist)
	ret.append(ylist)
	ret.append(m)
	return ret

start = time.time()

inp = reader(filename1)
x_train = inp[0]
y_train = inp[1]
training_examples = inp[2]

outp = reader(filename2)
x_test = outp[0]
y_test = outp[1]
testing_examples = outp[2]

enc = OneHotEncoder()
x_com = enc.fit_transform(x_train)

x_train = x_com.toarray()

x_com1 = enc.fit_transform(x_test)

x_test = x_com1.toarray()

end1 = time.time()
# print(x_train)


def forward(X,WEIGHTS,BIAS):
	temp = X

	ln = temp.shape[1]
	Netj = []
	Oj = []
	Oj.append(temp)
	layers = len(WEIGHTS)
	for i in range(0,layers):
		W = WEIGHTS[i]
		B = BIAS[i]
		temp = np.matmul(W,temp) + np.tile(B,ln)
		Netj.append(temp)
		if(i==layers-1):
			# print(temp.shape)
			temp = softmax(temp)
		else:
			temp = sig(temp)
		Oj.append(temp)
	return temp,Netj,Oj

def prediction(X,WEIGHTS,BIAS):
	temp = X

	ln = temp.shape[1]
	layers = len(WEIGHTS)
	y_pred = []
	for i in range(0,layers):
		W = WEIGHTS[i]
		B = BIAS[i]
		temp = np.matmul(W,temp) + np.tile(B,ln)
		# Netj.append(temp)
		if(i==layers-1):
			# print(temp.shape)
			temp = softmax(temp)
		else:
			temp = sig(temp)
		# Oj.append(temp)

	y_pred = np.argmax(temp,axis =0)
	# print(y_pred.shape)
	return y_pred.tolist()

def BackPropagation(MATY,MATY_o,Netj,Oj,WEIGHTS):
	Change_Netj = []
	layers = len(Netj)
	change_net = np.zeros([1,1])
	Change_W = []
	Change_B = []
	for p in range(0,layers):
		i=layers-p-1
		if(i==layers-1):
			# print(Oj[i+1].shape)
			# print(Oj[i].shape)
			# print(MATY_o.shape)
			
			change_net = Oj[i+1] - MATY_o
			# print(change_net.shape)
			outY = change_net.shape[0]
			Change_Netj.append(change_net)
			change_b = np.sum(change_net,axis=1).reshape(outY,1)
			change_w = np.matmul(change_net,Oj[i].T)
			Change_W.append(change_w)
			Change_B.append(change_b)
			# print(change_b.shape)
		else:
			# w.T x chan_net  * Oj(1-Oj)
			W = WEIGHTS[i+1]
			
			change_net = np.multiply(np.multiply(Oj[i+1],1-Oj[i+1]),np.matmul(W.T,change_net))
			outY = change_net.shape[0]
			Change_Netj.append(change_net)
			change_b = np.sum(change_net,axis=1).reshape(outY,1)
			change_w = np.matmul(change_net,Oj[i].T)
			Change_W.append(change_w)
			Change_B.append(change_b)
			# print(change_b.shape)

	return Change_W,Change_B
			



inputX = len(x_train[0])
outputY = 10

BATCH_SIZE = 100
LIST_HIDDEN = [50,50]

LAYERS = len(LIST_HIDDEN)

WEIGHTS = []
BIAS = []

mu = 0
si = 1
prev = len(x_train[0])
for i in range(0,LAYERS):
	W = np.random.normal(mu,si,(LIST_HIDDEN[i],prev))
	B = np.random.normal(mu,si,(LIST_HIDDEN[i],1))
	WEIGHTS.append(W)
	BIAS.append(B)
	prev = LIST_HIDDEN[i]

W = np.random.normal(mu,si,(outputY,prev))
B = np.random.normal(mu,si,(outputY,1))
WEIGHTS.append(W)
BIAS.append(B)

# for i in range(0,len(WEIGHTS)):
# 	print(WEIGHTS[i].shape)

# for i in range(0,len(WEIGHTS)):
# 	print(np.tile(BIAS[i],1).shape)

# print(BIAS)

MATX1 = np.array(x_test).T

# x_sub = x_train[0:BATCH_SIZE]
# y_sub = y_train[0:BATCH_SIZE]
# print(y_sub)

# MATX = np.array(x_sub).T
# # print(MATX.shape)

# 

# MATY_given = generateY(outputY,y_sub);

# print(MATY)
# print(MATY_given)
end2 = time.time()
for epoch in range(0,500):
	comb = list(zip(x_train,y_train))
	random.shuffle(comb)
	x_train,y_train = zip(*comb)

	for batch in range (0,int(training_examples/BATCH_SIZE)):
		bb = batch*BATCH_SIZE
		x_sub = x_train[bb:min(bb + BATCH_SIZE,training_examples)]
		y_sub = y_train[bb:min(bb + BATCH_SIZE,training_examples)]

		MATX = np.array(x_sub).T

		MATY, Netj, Oj = forward(MATX,WEIGHTS,BIAS)

		# print(Oj)

		MATY_o = generateY(outputY,y_sub)

		Change_W,Change_B = BackPropagation(MATY,MATY_o,Netj,Oj,WEIGHTS)

		# print(len(WEIGHTS))
		# print(len(Change_W))
		for i in range(0,len(WEIGHTS)):
			WEIGHTS[i] -= alpha*Change_W[len(WEIGHTS)-i-1]
			BIAS[i] -= alpha*Change_B[len(WEIGHTS)-i-1]
		# print(batch)

		# break;
	print(epoch)


end3 = time.time()

y_pred = prediction(MATX1,WEIGHTS,BIAS)


accuracy = accuracy_score(y_test, y_pred)
print(accuracy)
confusion_matrix = confusion_matrix(y_test,y_pred)
print(confusion_matrix)
end4 = time.time()


print("reading time" , end2-start)
print("training time" , end3-end2)
print("testing time" , end4-end3)

