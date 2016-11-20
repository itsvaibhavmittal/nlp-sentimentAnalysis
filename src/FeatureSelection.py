'''
Created on Nov 20, 2016

@author: vaibhav
'''
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.feature_selection import VarianceThreshold

def chi2(k, trainingFeatures, trainingClasses, testFeatures):
    ch2 = SelectKBest(chi2, k=k)
    trainingFeaturesNew = ch2.fit_transform(trainingFeatures, trainingClasses)
    testFeaturesNew = ch2.transform(testFeatures)
    return (trainingFeaturesNew, testFeaturesNew)

def varianceThreshold(p, trainingFeatures, trainingClasses, testFeatures):
    sel = VarianceThreshold(threshold=(p * (1 - p)))
    trainingFeaturesNew = sel.fit_transform(trainingFeatures, trainingClasses)
    testFeaturesNew = sel.transform(testFeatures)
    return (trainingFeaturesNew, testFeaturesNew)
