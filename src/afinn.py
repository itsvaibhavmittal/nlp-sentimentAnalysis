'''
Created on Nov 19, 2016

@author: rahul
'''
class afinn:
    '''
    This class classifies the data using Neural Network algorithm
    '''


    def __init__(self, featureSet):
        '''
        Constructor
        '''
        self.featurePolarity = [0]*len(featureSet)
        #print(len(featureSet))
        afinn = {}
        for line in open("/Users/Rahul/Downloads/AFINN/myList.txt"):
            keyValue = line.split()
            afinn[keyValue[0]] = int(keyValue[1])
        count = 0
        for feature in featureSet:
            if feature in afinn:
                self.featurePolarity[count] = afinn[feature]
            count+=1
        self.correct = 0
        self.wrong = 0
    
    def classify(self, featureVector):
        sumSO = 0
        count = 0
        idx = 0
        for feature in featureVector:
            sumSO += feature*self.featurePolarity[idx]
            if feature !=0 :
                count +=1
            idx +=1
        return sumSO/count
    
    def train(self, trainingFeatures, trainingClasses):
        if(len(trainingFeatures) != len(trainingClasses)):
            print("Length of feature vectors and class vector are different")
            return
        
        n = len(trainingClasses)
        for i in range(0, n):
            if trainingClasses[i] == 'neg':
                count  = 0
                #print( len(trainingFeatures[i]))
                for feature in trainingFeatures[i]:
                    self.featurePolarity[count] -= feature
                    count +=1
            elif trainingClasses[i] == 'pos':
                count  = 0
                #print( len(trainingFeatures[i]))
                for feature in trainingFeatures[i]:
                    self.featurePolarity[count] += feature
                    count +=1
                
        print("AFINN training complete")
        
    def test(self, testFeatures, testClasses):
        if(len(testFeatures) != len(testClasses)):
            print("Length of feature vectors and class vector are different")
            return
        print("Predicting Classes")
        predictedClasses = []
        for feature in testFeatures:
            klass = self.classify(feature)
            if klass < -3:
                predictedClasses.append('neg')
            elif klass > 3:
                predictedClasses.append('pos')
            else:
                predictedClasses.append('neu')
            
        print("Predicted Classes")
        for i in range(0, len(predictedClasses)):
            if(predictedClasses[i] == testClasses[i]):
                self.correct += 1
            else:
                self.wrong += 1
        
        #print("Correctly classified:" + self.correct + " out of " + len(testClasses))
        
    def getCorrectCount(self):
        return self.correct
    
    def getWrongCount(self):
        return self.wrong