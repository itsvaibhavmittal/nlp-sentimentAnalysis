'''
Created on Nov 19, 2016

'''
from os import listdir
import sys
import nltkUtil
from naiveBayes import naiveBayes
from nltk.corpus import stopwords
import ctypes
from neuralNetwork import neuralNetwork
from svm import svm
from RandomForest import RandomForest
import Processing

idx = 0
allWordsMap = {}
fileToExample = {}
wordToDoc = {}
allWords = []
stop = set(stopwords.words('english'))
phrasesScore = {}
phraseToIndex = {}
phraseIndex = 0
tokensScore = {}
tokenToIndex = {}
tokenIndex = 0
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
rating = [0, 0, 0, 0, 0, 0]


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
        self.groundTruth = 0
        self.label = 0
      

def segmentWords(s):
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
    for token in tokens:
        if token == "n't":
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
    for fold in range(0, 10):
        split = TrainSplit()
        for fName, example in fileToExample.items():
            fileName = example.name
            if(fileName.startswith('doc_' + str(fold) + '_')):
                split.test.append(example)
            else:
                split.train.append(example)
        splits.append(split)
    return splits


def test10Fold():
    global allWords
    splits = tenFoldCrossValidation()
    
    count = 0
    total = 0
    print("Naive Bayes")
    for split in splits:
        nb = naiveBayes()
        trainFeatures = []
        trainClasses = []
        testFeatures = []
        testClasses = []
        for example in split.train:
            trainFeatures.append(example.features)
            trainClasses.append(example.klass)
        for example in split.test:
            testFeatures.append(example.features)
            testClasses.append(example.klass)
        
        nb.train(trainFeatures, trainClasses)
        nb.test(testFeatures, testClasses)
        accuracy = nb.getCorrectCount() / len(testClasses)
        total = total + accuracy
        print("[INFO]\tFold ", str(count), " Accuracy:", str(accuracy))
        count =  count +1
    
    print("[INFO]\tAccuracy:", str(total / 10))

    count = 0
    total = 0
    print("Random Forest")
    for split in splits:
        nb = RandomForest(100)
        trainFeatures = []
        trainClasses = []
        testFeatures = []
        testClasses = []
        for example in split.train:
            trainFeatures.append(example.features)
            trainClasses.append(example.klass)
        for example in split.test:
            testFeatures.append(example.features)
            testClasses.append(example.klass)
        
        nb.train(trainFeatures, trainClasses)
        nb.test(testFeatures, testClasses)
        accuracy = nb.getCorrectCount() / len(testClasses)
        total = total + accuracy
        print("[INFO]\tFold ", str(count), " Accuracy:", str(accuracy))
        count =  count +1
    
    print("[INFO]\tAccuracy:", str(total / 10))
    
    count = 0
    total = 0
    print("Neural 5")
    for split in splits:
        nb = neuralNetwork((5,),1000)
        trainFeatures = []
        trainClasses = []
        testFeatures = []
        testClasses = []
        for example in split.train:
            trainFeatures.append(example.features)
            trainClasses.append(example.klass)
        for example in split.test:
            testFeatures.append(example.features)
            testClasses.append(example.klass)
        
        nb.train(trainFeatures, trainClasses)
        nb.test(testFeatures, testClasses)
        accuracy = nb.getCorrectCount() / len(testClasses)
        total = total + accuracy
        print("[INFO]\tFold ", str(count), " Accuracy:", str(accuracy))
        count =  count +1
    
    print("[INFO]\tAccuracy:", str(total / 10))
    
    count = 0
    total = 0
    print("Neural 3")
    for split in splits:
        nb = neuralNetwork((3,),1000)
        trainFeatures = []
        trainClasses = []
        testFeatures = []
        testClasses = []
        for example in split.train:
            trainFeatures.append(example.features)
            trainClasses.append(example.klass)
        for example in split.test:
            testFeatures.append(example.features)
            testClasses.append(example.klass)
        
        nb.train(trainFeatures, trainClasses)
        nb.test(testFeatures, testClasses)
        accuracy = nb.getCorrectCount() / len(testClasses)
        total = total + accuracy
        print("[INFO]\tFold ", str(count), " Accuracy:", str(accuracy))
        count =  count +1
    
    print("[INFO]\tAccuracy:", str(total / 10))
    
    count = 0
    total = 0
    print("SVM")
    for split in splits:
        nb = svm()
        trainFeatures = []
        trainClasses = []
        testFeatures = []
        testClasses = []
        for example in split.train:
            trainFeatures.append(example.features)
            trainClasses.append(example.klass)
        for example in split.test:
            testFeatures.append(example.features)
            testClasses.append(example.klass)
        
        nb.train(trainFeatures, trainClasses)
        nb.test(testFeatures, testClasses)
        accuracy = nb.getCorrectCount() / len(testClasses)
        total = total + accuracy
        print("[INFO]\tFold ", str(count), " Accuracy:", str(accuracy))
        count =  count +1
    
    print("[INFO]\tAccuracy:", str(total / 10))
   


def addPhrase(phrase, rating):
    if phrase not in phrasesOccurence:
        phrasesOccurence[phrase] = 0
    phrasesOccurence[phrase] = phrasesOccurence[phrase] + 1
    if rating == 1:
        if phrase not in phraseOccurence1:
            phraseOccurence1[phrase] = 0
        phraseOccurence1[phrase] = phraseOccurence1[phrase] + 1
    elif rating == 2:
        if phrase not in phraseOccurence2:
            phraseOccurence2[phrase] = 0
        phraseOccurence2[phrase] = phraseOccurence2[phrase] + 1
    elif rating == 3:
        if phrase not in phraseOccurence3:
            phraseOccurence3[phrase] = 0
        phraseOccurence3[phrase] = phraseOccurence3[phrase] + 1
    elif rating == 4:
        if phrase not in phraseOccurence4:
            phraseOccurence4[phrase] = 0
        phraseOccurence4[phrase] = phraseOccurence4[phrase] + 1
    else:
        if phrase not in phraseOccurence5:
            phraseOccurence5[phrase] = 0
        phraseOccurence5[phrase] = phraseOccurence5[phrase] + 1

def addToken(token, rating, posWords, negWords):
    label = 0
    if token[0] in posWords:
        label = 1
    elif token[0] in negWords:
        label = -1
    else:
        return 0
    
    if token not in tokensOccurence:
        tokensOccurence[token] = 0
    tokensOccurence[token] = tokensOccurence[token] + 1
    
    if rating == 1:
        if token not in tokenOccurence1:
            tokenOccurence1[token] = 0
        tokenOccurence1[token] = tokenOccurence1[token] + 1
    elif rating == 2:
        if token not in tokenOccurence2:
            tokenOccurence2[token] = 0
        tokenOccurence2[token] = tokenOccurence2[token] + 1
    elif rating == 3:
        if token not in tokenOccurence3:
            tokenOccurence3[token] = 0
        tokenOccurence3[token] = tokenOccurence3[token] + 1
    elif rating == 4:
        if token not in tokenOccurence4:
            tokenOccurence4[token] = 0
        tokenOccurence4[token] = tokenOccurence4[token] + 1
    else:
        if token not in tokenOccurence5:
            tokenOccurence5[token] = 0
        tokenOccurence5[token] = tokenOccurence5[token] + 1
    
    return label

def filterPhrasesAndTokens():
    global phraseIndex
    global tokenIndex
    for phrase, occurence in phrasesOccurence.items():
        if occurence >= 10:
            phrasesScore[phrase] = 0
            phraseToIndex[phrase] = phraseIndex
            phraseIndex += 1
    
    for token, occurence in tokensOccurence.items():
        if occurence >= 10:
            tokensScore[token] = 0
            tokenToIndex[token] = tokenIndex
            tokenIndex += 1

def getPhraseOccurence(phrase, rating):
    if rating ==1 and phrase in phraseOccurence1:
        return phraseOccurence1[phrase]
    elif rating ==2 and phrase in phraseOccurence2:
        return phraseOccurence2[phrase]
    elif rating ==3 and phrase in phraseOccurence3:
        return phraseOccurence3[phrase]
    elif rating ==4 and phrase in phraseOccurence4:
        return phraseOccurence4[phrase]
    elif phrase in phraseOccurence5:
        return phraseOccurence5[phrase]
    else:
        return 0
    
def getTokenOccurence(token, rating):
    if rating ==1 and token in tokenOccurence1:
        return tokenOccurence1[token]
    elif rating ==2 and token in tokenOccurence2:
        return tokenOccurence2[token]
    elif rating ==3 and token in tokenOccurence3:
        return tokenOccurence3[token]
    elif rating ==4 and token in tokenOccurence4:
        return tokenOccurence4[token]
    elif token in tokenOccurence5:
        return tokenOccurence5[token]
    else:
        return 0

def calculateScore():
    for phrase, score in phrasesScore.items():
        num = 0
        den = 0
        for i in range(1,6):
            num = num+ (i*rating[i]*getPhraseOccurence(phrase, i))
            den = den + (rating[i]*getPhraseOccurence(phrase, i))
        
        phrasesScore[phrase] = float(num/den)
    
    for token, score in tokensScore.items():
        num = 0
        den = 0
        for i in range(1,6):
            num = num+ (i*rating[i]*getTokenOccurence(token, i))
            den = den + (rating[i]*getTokenOccurence(token, i))
        tokensScore[token] = float(num/den)

def getAverageScore(example):
    score = 0
    count  = 0
    for phrase in example.phrases:
        if phrase in phrasesScore:
            score += phrasesScore[phrase]
            count +=1
    
    for token in example.tokens:
        if token in tokensScore:
            score += tokensScore[token]
            count +=1
    
    if (count ==0):
        return 0
    return float(score/count)
       
def preProcessExamples(posWords, negWords):
    count  = 0
    for fName, example in fileToExample.items():
        phrases, tokens, example.label = Processing.getPhrasesAndTokens(example.content, posWords, negWords)
        example.phrases = phrases
        example.tokens = tokens
        if example.label > 0:
            example.label = 2
        elif example.label < 0:
            example.label = 1
        label = 1
        for phrase in phrases:
            addPhrase(phrase, example.rating)
        for token in tokens:
            label += addToken(token, example.rating, posWords, negWords)
        if label >0:
            example.groundTruth = 2
        elif label < 0:
            example.groundTruth = 1
        
        fileToExample[fName] = example
        count +=1
    filterPhrasesAndTokens()
    calculateScore()

    
def preProcessExamplesWithHash():
    numPhrases = len(phraseToIndex)
    numTokens = len(tokenToIndex)
    for fName, example in fileToExample.items():
        phrases = example.phrases
        phraseArray = [0] * numPhrases
        tokens = example.tokens
        tokenArray = [0] * numTokens
        for phrase in phrases:
            if phrase in phraseToIndex:
                phraseArray[phraseToIndex[phrase]] = 1
        for token in tokens:
            if token in tokenToIndex:
                tokenArray[tokenToIndex[token]] = 1
        features = []
        features = features + phraseArray
        features = features + tokenArray
        features.append(getAverageScore(example))
        features.append(example.groundTruth)
        features.append(example.label)
        example.features = features
        fileToExample[fName] = example

def processRatings():
    global rating
    for i in range(1,6):
        if i != 3:
            rating[i] = rating[5]/rating[i]
        
def preprocess(parentDir):
    global rating
    subdirs = ["/pos", "/neg"]
    for subdir in subdirs:
        for fileName in listdir(parentDir + subdir):
            fname = parentDir + subdir + "/"+fileName
            example = Example()
            example.content = readFileContent(fname)
            example.klass = subdir[1:]
            example.rating = int(fileName.split("_")[2])
            rating[int(fileName.split("_")[2])]  = rating[int(fileName.split("_")[2])] +1
            example.name = fileName
            fileToExample[fname] = example
    negWords = Processing.getNegativeWords(parentDir)
    posWords = Processing.getPositiveWords(parentDir)
    processRatings()
    preProcessExamples(posWords, negWords)
    preProcessExamplesWithHash()

        
def main():
    if (len(sys.argv) != 2):
        print ('usage:\t algoStart.py <data path>')
        sys.exit(0)
    else:
        preprocess(sys.argv[1])
        test10Fold()

if __name__ == "__main__":
    main()
