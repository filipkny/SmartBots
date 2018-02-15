import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class Neural_net:
    def __init__(self,w1,w2):#1 hidden layer NN; w1,w2 - weight matricies, rows indicate the amount of neurons in next layer
        self.w1 = w1
        self.w2 = w2
        self.y = 0
    def set_y(self,y):
        self.y = y
        
    def get_y(self):
        return self.y
    
    def forwardprop(self,X):
        h = sigmoid(np.matmul(self.w_1,X))
        y = float(sigmoid(np.matmul(self.w_2,h)))
        self.set_y(y)
