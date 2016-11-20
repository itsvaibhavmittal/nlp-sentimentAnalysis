'''
Created on Nov 19, 2016

@author: vaibhav
'''
from os import listdir
import sys
import nltkUtil
from naiveBayes import naiveBayes
from nltk.corpus import stopwords
from kNN import kNN
import ctypes

idx = 0
allWordsMap = {}
fileToExample = {}
wordToDoc = {}
stop = set(stopwords.words('english'))

class TrainSplit:
    """Represents a set of training/testing data. self.train is a list of Examples, as is self.test. 
    """
    def __init__(self):
        self.train = []
        self.test = []
        
class Example:
    """Represents a document with a label. klass is 'pos' or 'neg' by convention.
       words is a list of strings.
    """
    def __init__(self):
        self.klass = ''
        self.features = []
        self.tokens = []
        self.name = ''
      

def segmentWords( s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()

def readFile(fileName):
    global idx
    file = open(fileName)
    content = file.read().replace('\n', ' ')
    file.close()
    tokens = nltkUtil.tokenization(content)
    #tokens = segmentWords(content)
    for token in tokens:
        if token in stop:
            continue
        if(token not in wordToDoc):
            wordToDoc[token] = set()
        wordToDoc[token].add(fileName)
    return tokens

def tenFoldCrossValidation():
    splits = []
    print("Splitting")
    for fold in range(0, 10):
        split = TrainSplit()
        for fName, example in fileToExample.items():
            fileName = example.name
            if(fileName.startswith('doc_'+str(fold)+'_')):
                split.test.append(example)
            else:
                split.train.append(example)
        splits.append(split)
    return splits
    print("Splitting Over")


def test10Fold():
    splits = tenFoldCrossValidation()
    count = 0
    total = 0
    print("Training")
    for split in splits:
        nb =  kNN(3)
        trainFeatures = []
        trainClasses = []
        testFeatures = []
        testClasses = []
        print("Training:", count," started" )
        for example in split.train:
            trainFeatures.append(example.features)
            trainClasses.append(example.klass)
        print("Testing:", count," started" )
        for example in split.test:
            testFeatures.append(example.features)
            testClasses.append(example.klass)
        
        nb.train(trainFeatures,trainClasses )
        nb.test(testFeatures, testClasses)
        accuracy = nb.getCorrectCount()/ len(testClasses)
        total = total  + accuracy
        print("Correctly Classified:", str(accuracy))
        #print("Wrongly Classified:",str(nb.getWrongCount()) )
    
    print("Total accuracy = " , str(accuracy/10))
        

def filterFeatures():
    global idx
    for token, fset in wordToDoc.items():
        #print(len(wordToDoc[token]))
        if len(wordToDoc[token]) >= 200:
            allWordsMap[token] = idx
            idx +=1
 
def preProcessExamples():
    print("Preprocesing Examples")
    numFeatures = len(allWordsMap)
    print("Features:", numFeatures)
    for fName, example in fileToExample.items():
        tokens = example.tokens
        features = [0]*numFeatures
        for token in tokens:
            if token in allWordsMap:
                features[allWordsMap[token]] = features[allWordsMap[token]] +1
        example.features = features
        fileToExample[fName] = example
    print("Examples preprocessed")
    
def preProcessExamplesWithHash():
    print("Preprocesing Examples")
    numFeatures = len(allWordsMap)
    print("Features:", numFeatures)
    for fName, example in fileToExample.items():
        tokens = example.tokens
        features = [0]*numFeatures
        for token in tokens:
            if token in allWordsMap:
                features[allWordsMap[token]] = 1
        stringFeature = ''.join(features)    
        example.features = [ctypes.c_size_t(hash(stringFeature)).value]
        fileToExample[fName] = example
    print("Examples preprocessed")
        
def preprocess(parentDir):
    for fileName in listdir(parentDir + "/pos"):
        fname = parentDir + "/pos/" + fileName
        example = Example()
        example.tokens = readFile(fname)
        example.klass = 'pos'
        example.name = fileName
        fileToExample[fname] = example
    
    for fileName in listdir(parentDir + "/neg"):
        fname = parentDir + "/neg/" + fileName
        example = Example()
        example.tokens = readFile(fname)
        example.klass = 'neg'
        example.name = fileName
        fileToExample[fname] = example
            
    for fileName in listdir(parentDir + "/neu"):
        fname = parentDir + "/neu/" + fileName
        example = Example()
        example.tokens = readFile(fname)
        example.klass = 'neu'
        example.name = fileName
        fileToExample[fname] = example
    filterFeatures()
    preProcessExamples()

        
def main():
    if (len(sys.argv) != 2):
        print ('usage:\tstart.py <data path>')
        sys.exit(0)
    else:
        preprocess(sys.argv[1])
        test10Fold()

if __name__ == "__main__":
    main()
