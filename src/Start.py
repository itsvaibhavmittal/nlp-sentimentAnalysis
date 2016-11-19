'''
Created on Nov 19, 2016

@author: vaibhav
'''
from os import listdir
import nltkUtil

def readFile(fileName):
    file = open(fileName)
    content = file.read().replace('\n', ' ')
    file.close()
    tokens = nltkUtil.tokenization(content)
    return tokens

def 10FoldCrossValidation(parentDir):
    
    for fold in range(1, 11):
        trainingExamples = []
        testingExamples = []
        for fileName in listdir(parentDir + "/pos"):
            if(fileName.startswith('doc_'+str(fold)+'_')):
                testingExamples.append(readFile())
            else:
                trainingExamples.append()
                
        for file in listdir(parentDir + "/neu"):
            if(fileName.startswith('doc_'+str(fold)+'_')):
                testingExamples.append()
            else:
                trainingExamples.append()
                
        for file in listdir(parentDir + "/neg"):
            if(fileName.startswith('doc_'+str(fold)+'_')):
                testingExamples.append()
            else:
                trainingExamples.append()