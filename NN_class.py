import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class Neural_net:
    def __init__(self,w1,w2, input = 2, hidden = 6):#1 hidden layer NN; w1,w2 - weight matricies, rows indicate the amount of neurons in next layer
        self.w1 = np.reshape(w1,(hidden,input)) #numpy array
        self.w2 = np.array(w2)
        self.y = 0
        
    def set_y(self,y):
        self.y = y
        
    def get_y(self):
        return self.y
    
    def forwardprop(self,X):
        if np.shape(self.w1)[1] != np.shape(X)[0]:
            print('Error: The weight matrix w1 has an incorrect amount of columns. FORWARDPROPAGATION NOT COMPUTED')
            return

        X = np.array(X)
        h = sigmoid(np.matmul(self.w1,X))

        if np.shape(self.w2)[1] != np.shape(h)[0]:
            print(str(np.shape(self.w2)[1]) + "=/=" + str(np.shape(h)[0]))
            print('Error: The weight matrix w2 has an incorrect amount of columns. FORWARDPROPAGATION NOT COMPUTED')
            return
        
        if np.shape(self.w2)[0] != 1:
           print('Error: The weight matrix w2 does not have one row, the forward propagation will result in more than one neuron in output layer. FORWARDPROPAGATION NOT COMPUTED')
           return
        
        y = float(sigmoid(np.matmul(self.w2,h)))
        self.set_y(y)

