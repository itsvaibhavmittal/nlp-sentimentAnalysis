'''
Created on Nov 19, 2016

'''
from sklearn.neural_network import MLPClassifier

class neuralNetwork:
    '''
    This class classifies the data using Neural Network algorithm
    '''


    def __init__(self, hiddenLayerTuple, maxIter):
        '''
        Constructor
        '''
        self.classifier = MLPClassifier(hidden_layer_sizes=hiddenLayerTuple, max_iter=maxIter)
        self.correct = 0
        self.wrong = 0
        
    def train(self, trainingFeatures, trainingClasses):
        if(len(trainingFeatures) != len(trainingClasses)):
            print("Length of feature vectors and class vector are different")
            return
        
        X = trainingFeatures
        Y = trainingClasses
        self.classifier.fit(X, Y)
        
    def test(self, testFeatures, testClasses):
        if(len(testFeatures) != len(testClasses)):
            print("Length of feature vectors and class vector are different")
            return
        predictedClasses = self.classifier.predict(testFeatures)
        for i in range(0, len(predictedClasses)):
            if(predictedClasses[i] == testClasses[i]):
                self.correct += 1
            else:
                self.wrong += 1
        
        
    def getCorrectCount(self):
        return self.correct
    
    def getWrongCount(self):
        return self.wrong