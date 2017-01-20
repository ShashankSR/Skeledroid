import re
import json
import pprint
import sys
import time
import glob, os

pwd = "/Users/shashank/Personal Projects/Skeledroid/"

replaceFragmentPattern = ""
functionCallPattern = re.compile("^\s*(\w+)\(.*\);")
startActivityPattern = re.compile("(\w+)\.(?:start.*)\((.*)\)")
functionPattern = re.compile("(public|protected|private|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *(?:\{?|[^;])")
contentviewPat = re.compile("(?:setContentView).*(R.layout.*)\)")
classPat = re.compile("class (\w+)");
extendsPat = re.compile("class (\w+) * extends (\w+)");
implementsPat = re.compile("class (\w+) .* implements (\w+(, \w+)*)")
listenersPat = re.compile("^(\w+)\.(\w+).*Listener\((\w+)")
ovverridenFunction = re.compile("@[Oo]verride")
finishDeclaration = re.compile("{")

def writeToFile(path,jsonobject):
    with open(pwd + 'testing/'+ path, 'a') as outfile:
        try:
            outfile.write("\""+str(jsonobject['classname'][0])+"\":")
            json.dump(jsonobject, outfile)# with open('data.txt', 'w') as outfile: #json.dump(data, outfile)
            outfile.write(",")
        except IndexError as e:
            print ("-----------No Classname Error---------------")
        

def getFilePath(droidFilePath):
    droidFilePath = droidFilePath.replace(" ","")
    droidFilePath = droidFilePath.replace(".","/")
    droidFilePath = pwd + "main/java/" + droidFilePath + ".java"
    return droidFilePath

def fileAnalyser(filename):

    isOverRidden = False
    isInnerClass = False
    classJsonRep = {}
    classJsonRep['functions'] = {}
    classJsonRep['functions']['own'] = {}
    classJsonRep['functions']['overridden'] = {}
    classJsonRep['implements'] = []
    mCurrentFunction = ""
    mIsOverridden = ""
    classJsonRep['classname'] = ""
    classJsonRep['extends'] = ""
    classJsonRep['innerClass'] = []
    classJsonRep['setContentView'] = []
    classJsonRep['startingActivity'] = []
    classJsonRep['startActivityName'] = []
    try:
        with open(filename, 'r') as myfile:
            data=myfile.read()
        myfile.close()
        isOverRidden = False
        for i, line in enumerate(open(filename)):
            for match in re.finditer(classPat, line):
                if classJsonRep['classname'] == "":
                    classJsonRep['classname'] = match.groups()
                else :
                    classJsonRep['innerClass'].append(match.groups())
            for match in re.finditer(ovverridenFunction, line):
                isOverRidden = True
            for match in re.finditer(extendsPat, line):
                if classJsonRep['extends'] == "":
                    classJsonRep['extends'] = match.groups()[1]
            for match in re.finditer(implementsPat, line):
                if classJsonRep['implements']:
                    for x in xrange(1, len(match.groups())):
                        classJsonRep['implements'].append(match.groups()[x])
            for match in re.finditer(functionPattern, line.strip()):
                if (isOverRidden):
                    classJsonRep['functions']['overridden']['' + match.groups()[1]] = []
                    isOverRidden = False
                    mIsOverridden = 'overridden'
                    mCurrentFunction = match.groups()[1]
                else :
                    mIsOverridden = 'own'
                    mCurrentFunction = match.groups()[1]
                    classJsonRep['functions']['own']['' + match.groups()[1]] = []
            for match in re.finditer(functionCallPattern, line.strip()):
                classJsonRep['functions'][mIsOverridden][mCurrentFunction].append(match.groups()[0])
            for match in re.finditer(listenersPat, line.strip()):
                classJsonRep['functions'][mIsOverridden][mCurrentFunction].append(match.groups()[0])
            for match in re.finditer(startActivityPattern, line):
                filematch = re.search(r'import(.*'+match.groups()[0]+').*;',data)
                if filematch:
                    classJsonRep['startingActivity'].append(getFilePath(filematch.group(1)))
                    classJsonRep['startActivityName'].append(match.groups()[0])
            for match in re.finditer(contentviewPat, line):
                classJsonRep['setContentView'].append(match.groups()[0])
        myfile.close()
        return classJsonRep
    except IOError as e:
        print "error"
    finally:
        return classJsonRep


fileList = []
fileCount = 0;
for root, dirs, files in os.walk(pwd+"/main"):
    for file in files:
        if file.endswith(".java"):
             fileFullPath = os.path.join(root, file)
             fileList.append(fileFullPath)
             writeToFile('data.json',fileAnalyser(fileFullPath))
             fileCount += 1
print fileCount



with open(pwd + 'testing/fileList.txt', 'w') as outfile:
    for item in fileList:
        outfile.write(item +"\n")
outfile.close()

os.chdir(pwd+"/main")
for file in glob.glob("*.java"):
    print(file)




