'''
Created on Nov 19, 2016

@author: vaibhav
'''

import nltk

def posTag(tokens):
    return nltk.pos_tag(tokens)

def tokenization(sentence):
    return nltk.word_tokenize(sentence)