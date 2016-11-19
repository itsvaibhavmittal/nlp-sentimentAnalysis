'''
Created on Nov 19, 2016

@author: vaibhav
'''
from sklearn.neighbors import KNeighborsClassifier

class kNN:
    '''
    This class classifies the data using k-Nearest Neighbor algorithm
    '''

    def __init__(self, k):
        '''
        Constructor
        '''
        self.classifier = KNeighborsClassifier(n_neighbors=k)
        self.correct = 0
        self.wrong = 0
        
    def train(self, trainingFeatures, trainingClasses):
        if(len(trainingFeatures) != len(trainingClasses)):
            print("Length of feature vectors and class vector are different")
            return
        
        X = trainingFeatures
        Y = trainingClasses
        self.classifier.fit(X, Y)
        print("kNN training complete")
        
    def test(self, testFeatures, testClasses):
        if(len(testFeatures) != len(testClasses)):
            print("Length of feature vectors and class vector are different")
            return
        
        predictedClasses = self.predict(testFeatures)
        for i in range(0, len(predictedClasses)):
            if(predictedClasses[i] == testClasses[i]):
                self.correct += 1
            else:
                self.wrong += 1
        
        print("Correctly classified:" + self.correct + " out of " + len(testClasses))
        
    def getCorrectCount(self):
        return self.correct
    
    def getWrongCount(self):
        return self.wrong
