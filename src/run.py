'''
Created on Nov 19, 2016

@author: Rahul
'''
import os
import sys


ignoreFiles = ['city_tourist_attractions.txt', 'tourist_attractions.txt', 'hotel_info.txt', '.DS_Store']
foderDict = {1:0, 2:0, 3:0, 4:0, 5:0}
folderDict = {'pos':0, 'neu':0, 'neg':0}
#base = '/Users/Rahul/Documents/coursework/NLP/project/'
base = ''
moveFolder = {1: "neg", 2:"neg", 3:"neu", 4:"pos", 5:"pos"}
fileFromFolder = {1:0, 2:0, 3:0, 4:0, 5:0}
folders = { 1:6550,2:8300, 3:14850, 4: 7400, 5:7450}
folderNums = [1,2,3,4,5]

def readFile(fName):
    ratingStr = 'Rating:'
    contentStr = 'Content:'
    metaStr = "Meta Info:"
    content = ''
    rating = ''
    contentStarted = False;
    f = open(fName, encoding="utf8")
    for line in f:
        
        if line.startswith(ratingStr):
            rating  = ((line.split(ratingStr,1)[1]).split(' ', 1)[0]).strip()
        elif line.startswith(contentStr):
            content = (line.split(contentStr,1)[1]).strip()
        elif (contentStarted == True) and (line.startswith(metaStr) == False):
            content = content + ' ' + line.strip()
        elif line.startswith(metaStr):
            break;
    f.close()
    return content, rating

def getFilePath(folderNum, fileNum):
    global base
    return base + str(folderNum) + '/doc_' + str(fileNum) +'.txt'
    
def addToFolder(content, folderNum):
    folderNum = int(folderNum)
    fileNum = foderDict[folderNum];
    foderDict[folderNum] = fileNum +1;
    
    fpath = getFilePath(folderNum, fileNum)
    f = open(fpath, 'w')
    f.write(content)
    f.close()


def createFolders():
    global base
    dirs = ["1", "2", "3", "4", "5", "neg", "neu", "pos"]
    for folderName in dirs:
        folderPath = base + folderName
        os.makedirs(folderPath)

def parseReviews(dirPath, outPath):
    global base
    n = len(outPath)
    if n == 0:
        return
    if outPath[n-1] != "/":
        base = outPath + "/"
    else:
        base = outPath
    createFolders()
    for root, dirs, files in os.walk(dirPath):
        for file in files:
            if file not in ignoreFiles:
                fName = os.path.join(root, file)
                content, rating = readFile(fName)
                if (len(rating) == 0) or (len(content) == 0):
                    continue
                content=content.encode("ascii","ignore").decode("ascii")
                addToFolder(content, rating)
    

def findFold(folderNum):
    fileNum = fileFromFolder[folderNum]
    div = int(folders[folderNum]/10)
    return str(int(fileNum/div))

def moveFile(fName, folderNum):
    global base
    outputFolder = moveFolder[folderNum]
    folder = base + outputFolder
    
    fold = findFold(folderNum)
    path = folder + "/doc_" +fold +"_" + str(folderNum) + "_" + str(folderDict[outputFolder]) + ".txt"
    f  = open(fName)
    content =  ''
    for line in f:
        content = content + ' ' + line
    content.strip()
    f.close()
    f = open(path, "w")
    f.write(content)
    f.close()
    #print("file:", path)
    #print('Content:', content)
    folderDict[outputFolder] = folderDict[outputFolder] + 1

def divideReviews():
    global base
    for i in folderNums:
        folderName = base + str(i)
        count  = 0;
        folderCompleted = False;
        for root, dirs, files in os.walk(folderName):
            for file in files:
                if (count >= folders[i]):
                    folderCompleted = True;
                    break
                if file not in ignoreFiles:
                    fName = os.path.join(root, file)
                    #print("FileNumber:", fileFromFolder[i])
                    moveFile(fName, i)
                    count = count+1
                    fileFromFolder[i] = fileFromFolder[i]+1


def main():
    if (len(sys.argv) != 3):
        print ('usage:\t run.py <data path> <output folder path>')
        sys.exit(0)
    else:
        parseReviews(sys.argv[1], sys.argv[2])
        divideReviews()

if __name__ == "__main__":
    main()


            
