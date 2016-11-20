'''
Created on Nov 20, 2016

@author: vaibhav
'''
from sets import Set
import nltkUtil

adjTags = Set(['JJ', 'JJR', 'JJS'])
verbTags = Set(['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'])

def negationPhrases(taggedWordsTuples, negativePrefixes):
    '''
    taggedWordsTuples is a list of tuples(word, tag) for a sentence
    '''
    NOA = []
    NOV = []
    for i in range(0, len(taggedWordsTuples)):
        tupl = taggedWordsTuples[i]
        if tupl[0] in negativePrefixes:
            tuple1 = taggedWordsTuples[i + 1]
            if(tuple1[1] in adjTags or tuple1[1] in verbTags):
                NOA.append(tupl[0] + " " + tuple1[0])
                NOV.append(tupl[0] + " " + tuple1[0]) 
            else:
                tuple2 = taggedWordsTuples[i + 2]
                if(tuple2[1] in adjTags or tuple2[1] in verbTags):
                    NOA.append(tupl[0] + " " + tuple1[0] + " " + tuple2[0])
                    NOV.append(tupl[0] + " " + tuple1[0] + " " + tuple2[0])
                    
    return (NOA, NOV)

def getPositiveWords(directory):
    posWords = []
    file = open(directory + "/positive-words.txt")
    for line in file.readlines():
        if(line[0] != ";"):
            posWords.append(line.strip())
            
    return posWords

def getNegativeWords(directory):
    negWords = []
    file = open(directory + "/negative-words.txt")
    for line in file.readlines():
        if(line[0] != ";"):
            negWords.append(line.strip())
            
    return negWords

def sentenceTokens(sentence, positiveWords, negativeWords):
    tokens = nltkUtil.tokenization(sentence)
    posTokens = set(tokens) & set(positiveWords)
    negTokens = set(tokens) & set(negativeWords)
    if(posTokens is None and negTokens is None):
        return None
    return(posTokens, negTokens)
        
        
