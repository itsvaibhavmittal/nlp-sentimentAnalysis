'''
Created on Nov 21, 2016

'''
from sklearn.ensemble import RandomForestClassifier

class RandomForest:
    '''
    This class classifies the data using Random Forest algorithm
    '''

    def __init__(self, n):
        '''
        Constructor
        '''
        self.classifier = RandomForestClassifier(n_estimators=n)
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
