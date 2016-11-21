'''
Created on Nov 20, 2016

@author: vaibhav
'''
#from sets import Set
import nltkUtil
import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


def negationPhrases(taggedWordsTuples):
    adjTags = set(['JJ', 'JJR', 'JJS'])
    verbTags = set(['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'])
    negativePrefixes = set(['RB', 'RBR', 'RBS'])    
    '''
    taggedWordsTuples is a list of tuples(word, tag) for a sentence
    '''
    NOA = []
    NOV = []
    for i in range(0, len(taggedWordsTuples)):
        tupl = taggedWordsTuples[i]
        if (tupl[1] in negativePrefixes) and (i+1 < len(taggedWordsTuples)):
            tuple1 = taggedWordsTuples[i + 1]
            if(tuple1[1] in adjTags or tuple1[1] in verbTags):
                NOA.append(tupl[0] + " " + tuple1[0])
                #NOV.append(tupl[0] + " " + tuple1[0]) 
            elif i+2 < len(taggedWordsTuples) :
                tuple2 = taggedWordsTuples[i + 2]
                if(tuple2[1] in adjTags or tuple2[1] in verbTags):
                    NOA.append(tupl[0] + " " + tuple1[0] + " " + tuple2[0])
                    #NOV.append(tupl[0] + " " + tuple1[0] + " " + tuple2[0])
                    
    return (NOA, NOV)

def getPositiveWords(directory):
    posWords = set()
    file = open(directory + "/positive-words.txt")
    for line in file:
        posWords.add(line.strip())
            
    return posWords

def getNegativeWords(directory):
    negWords = set()
    file = open(directory + "/negative-words.txt")
    for line in file:
        negWords.add(line.strip())
            
    return negWords

def sentenceTokens(sentence, positiveWords, negativeWords):
    tokens = nltkUtil.tokenization(sentence)
    posTokens = set(tokens) & set(positiveWords)
    negTokens = set(tokens) & set(negativeWords)
    if(posTokens is None and negTokens is None):
        return None, 0
    label = 0
    if len(posTokens) > len(negTokens):
        label = -1
    elif len(negTokens) > len(posTokens):
        label = 1
    return tokens, label

def getSentencesFromContent(content):
    global tokenizer
    return tokenizer.tokenize(content)

def getPhrasesAndTokens(content, poswWords, negWords):
    phrases = []
    resultTokens = []
    resultLabel = 0
    #print(content)
    sentences = getSentencesFromContent(content)
    for sentence in sentences:
        tokens, label = sentenceTokens(sentence,poswWords, negWords )
        resultLabel += label
        if tokens is not None:
            taggedTokens = nltkUtil.posTag(tokens)
            NOA, NOV = negationPhrases(taggedTokens)
            if len(NOA) > 0:
                phrases = phrases + NOA
            resultTokens = resultTokens + taggedTokens
   # print("Phrases:", phrases)
    #print("tokens:", resultTokens)
    #print("Label:", resultLabel)
    return phrases, resultTokens, resultLabel
                


        
        
