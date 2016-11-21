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
from neuralNetwork import neuralNetwork
from svm import svm
from afinn import afinn
import Processing

idx = 0
allWordsMap = {}
fileToExample = {}
wordToDoc = {}
allWords = []
stop = set(stopwords.words('english'))
phrasesScore = {}
tokensScore = {}
phrasesOccurence = {}
phraseOccurence1 = {}
phraseOccurence2 = {}
phraseOccurence3 = {}
phraseOccurence4 = {}
phraseOccurence5 = {}
tokensOccurence = {}
tokenOccurence1 = {}
tokenOccurence2 = {}
tokenOccurence3 = {}
tokenOccurence4 = {}
tokenOccurence5 = {}


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
        self.content = ''
        self.rating = 0
        self.phrases = []
      

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
    #print(nltkUtil.posTag(tokens))
    #tokens = segmentWords(content)
    for token in tokens:
        if token ==  "n't":
            token = "not"
        if token in stop:
            continue
        if(token not in wordToDoc):
            wordToDoc[token] = set()
        wordToDoc[token].add(fileName)
    return tokens

def readFileContent(fileName):
    file = open(fileName)
    content = file.read()
    file.close()
    return content



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
    global allWords
    splits = tenFoldCrossValidation()
    count = 0
    total = 0
    print("Training")
    for split in splits:
        nb =  naiveBayes()
        #nb = neuralNetwork((5,),1000)
        #nb = afinn(allWords)
        #nb = svm()
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
    
    print("Total accuracy = " , str(total/10))
        

def filterFeatures():
    global idx
    global allWords
    for token, fset in wordToDoc.items():
        #print(len(wordToDoc[token]))
        if len(wordToDoc[token]) >= 200 and len(wordToDoc[token]) <= 10000:
            allWordsMap[token] = idx
            idx +=1
    allWords = [None]*len(allWordsMap)
    for token, index in allWordsMap.items():
        allWords[index] = token


def addPhrase(phrase, rating):
    if phrase not in phrasesOccurence:
        phrasesOccurence[phrase] = 0
    phrasesOccurence[phrase] = phrasesOccurence[phrase] +1
    if rating ==1:
        if phrase not in phraseOccurence1:
            phraseOccurence1[phrase] = 0
        phraseOccurence1[phrase] = phraseOccurence1[phrase] +1
    elif rating ==2:
        if phrase not in phraseOccurence2:
            phraseOccurence2[phrase] = 0
        phraseOccurence2[phrase] = phraseOccurence2[phrase] +1
    elif rating ==3:
        if phrase not in phraseOccurence3:
            phraseOccurence3[phrase] = 0
        phraseOccurence3[phrase] = phraseOccurence3[phrase] +1
    elif rating ==4:
        if phrase not in phraseOccurence4:
            phraseOccurence4[phrase] = 0
        phraseOccurence4[phrase] = phraseOccurence4[phrase] +1
    else:
        if phrase not in phraseOccurence5:
            phraseOccurence5[phrase] = 0
        phraseOccurence5[phrase] = phraseOccurence5[phrase] +1

def addToken(token, rating, posWords, negWords):
    if token[0] not in posWords and token[0] not in negWords:
        return
    if token not in tokensOccurence:
        tokensOccurence[token] = 0
    tokensOccurence[token] = tokensOccurence[token] +1
    if rating ==1:
        if token not in tokenOccurence1:
            tokenOccurence1[token] = 0
        tokenOccurence1[token] = tokenOccurence1[token] +1
    elif rating ==2:
        if token not in tokenOccurence2:
            tokenOccurence2[token] = 0
        tokenOccurence2[token] = tokenOccurence2[token] +1
    elif rating ==3:
        if token not in tokenOccurence3:
            tokenOccurence3[token] = 0
        tokenOccurence3[token] = tokenOccurence3[token] +1
    elif rating ==4:
        if token not in tokenOccurence4:
            tokenOccurence4[token] = 0
        tokenOccurence4[token] = tokenOccurence4[token] +1
    else:
        if token not in tokenOccurence5:
            tokenOccurence5[token] = 0
        tokenOccurence5[token] = tokenOccurence5[token] +1
        

def filterPhrasesAndTokens():
    print("Filtering Phrases and Tokens")
    print("Initial Phrases:", len(phrasesOccurence))
    for phrase, occurence in phrasesOccurence.items():
        if occurence >=30:
            phrasesScore[phrase] = 0
    print("Remaining Phrases:", len(phrasesScore))
    
    print("Initial Tokens:", len(tokensOccurence))
    for token, occurence in tokensOccurence.items():
        if occurence >=30:
            tokensScore[token] = 0
    print("Remaining Tokens:", len(tokensScore))

        
        
def preProcessExamples(posWords, negWords):
    print("Preprocesing Examples")
    for fName, example in fileToExample.items():
        phrases, tokens = Processing.getPhrasesAndTokens(example.content, posWords, negWords)
        example.phrases = phrases
        example.tokens = tokens
        for phrase in phrases:
            addPhrase(phrase, example.rating)
        for token in tokens:
            addToken(token, example.rating, posWords, negWords)
        fileToExample[fName] = example
    print("Examples preprocessed")
    filterPhrasesAndTokens()
    calculateScore()
    

    
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
        #stringFeature = ''.join(features)    
        #example.features = [ctypes.c_size_t(hash(stringFeature)).value]
        example.features = features
        fileToExample[fName] = example
    print("Examples preprocessed")
        
def preprocess(parentDir):
    subdirs = ["/pos", "/neg", "/neu"]
    for subdir in subdirs:
        for fileName in listdir(parentDir + subdir):
            fname = parentDir + subdir + fileName
            example = Example()
            example.tokens = readFileContent(fname)
            example.klass = subdir[1:]
            example.rating = int(fileName.spit("_")[2])
            example.name = fileName
            fileToExample[fname] = example
    #filterFeatures()
    negWords = Processing.getNegativeWords(parentDir)
    posWords = Processing.getPositiveWords(parentDir)
    preProcessExamples(posWords, negWords)
    preProcessExamplesWithHash()

        
def main():
    if (len(sys.argv) != 2):
        print ('usage:\tstart.py <data path>')
        sys.exit(0)
    else:
        preprocess(sys.argv[1])
        test10Fold()

if __name__ == "__main__":
    main()
