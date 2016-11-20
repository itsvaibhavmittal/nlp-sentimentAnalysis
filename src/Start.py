'''
Created on Nov 19, 2016

@author: vaibhav
'''
from os import listdir
import sys
import nltkUtil
from naiveBayes import naiveBayes

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
      

def segmentWords( s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()

def readFile(fileName):
    file = open(fileName)
    content = file.read().replace('\n', ' ')
    file.close()
    #tokens = nltkUtil.tokenization(content)
    tokens = segmentWords(content)
    print("Filename:", fileName)
    print("Tokens:", len(tokens))
    return tokens

def tenFoldCrossValidation(parentDir):
    splits = []
    visited = {}
    for fold in range(0, 10):
        split = TrainSplit()
        for fileName in listdir(parentDir + "/pos"):
            fname = parentDir + "/pos/"+ fileName
            if fname in visited:
                example = visited[fname]
            else:
                example = Example()
                example.words = readFile(fname)
                example.klass = 'pos'
                visited[fname] = example
            if(fileName.startswith('doc_'+str(fold)+'_')):
                split.test.append(example)
            else:
                split.train.append(example)
        
        for fileName in listdir(parentDir + "/neg"):
            fname = parentDir + "/neg/"+ fileName
            if fname in visited:
                example = visited[fname]
            else:
                example = Example()
                example.words = readFile(fname)
                example.klass = 'neg'
                visited[fname] = example
            if(fileName.startswith('doc_'+str(fold)+'_')):
                split.test.append(example)
            else:
                split.train.append(example)
                
        for fileName in listdir(parentDir + "/neu"):
            fname = parentDir + "/neu/"+ fileName
            if fname in visited:
                example = visited[fname]
            else:
                example = Example()
                example.words = readFile(fname)
                example.klass = 'neu'
                visited[fname] = example
            if(fileName.startswith('doc_'+str(fold)+'_')):
                split.test.append(example)
            else:
                split.train.append(example)
        splits.append(split)
    return splits

def test10Fold(dirPath):
    splits = tenFoldCrossValidation(dirPath)
    count = 0
    for split in splits:
        nb =  naiveBayes()
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
        
        print("Correctly Classified:", str(nb.getCorrectCount()))
        print("Wrongly Classified:",str(nb.getWrongCount()) )
        
def main():
    if (len(sys.argv) != 2):
        print ('usage:\tstart.py <data path>')
        sys.exit(0)
    else:
        test10Fold(sys.argv[1])

if __name__ == "__main__":
    main()