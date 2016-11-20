'''
Created on Nov 19, 2016

@author: vaibhav
'''
from sklearn.naive_bayes import MultinomialNB

class naiveBayes:
    '''
    This class classifies the data using Multinomial Naive Bayes algorithm
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.classifier = MultinomialNB()
        self.correct = 0
        self.wrong = 0
        
    def train(self, trainingFeatures, trainingClasses):
        #print(trainingFeatures[0])
        #print(trainingClasses[0])
        if(len(trainingFeatures) != len(trainingClasses)):
            print("Length of feature vectors and class vector are different")
            return
        
        X = trainingFeatures
        Y = trainingClasses
        self.classifier.fit(X, Y)
        print("MultinomialNB training complete")
        
    def test(self, testFeatures, testClasses):
        if(len(testFeatures) != len(testClasses)):
            print("Length of feature vectors and class vector are different")
            return
        print("Predicting Classes")
        predictedClasses = self.classifier.predict(testFeatures)
        print("Predicted Classes")
        for i in range(0, len(predictedClasses)):
            if(predictedClasses[i] == testClasses[i]):
                self.correct += 1
            else:
                self.wrong += 1
        
        #print("Correctly classified:" + self.correct + " out of " + str(len(testClasses)))
        
    def getCorrectCount(self):
        return self.correct
    
    def getWrongCount(self):
        return self.wrong