import re
import json
import pprint
import sys
import time


replaceFragmentPattern = ""
functionCallPattern = re.compile("^\s*(\w+)\(.*\);")
startActivityPattern = re.compile("(\w+)\.(?:start.*)\((.*)\)")
functionPattern = re.compile("(public|protected|private|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *(?:\{?|[^;])")
contentviewPat = re.compile("(?:setContentView).*,(.*)\)")
classPat = re.compile("class (\w+)");
extendsPat = re.compile("class (\w+) * extends (\w+)");
implementsPat = re.compile("class (\w+) .* implements (\w+(, \w+)*)")
listenersPat = re.compile("^(\w+)\.(\w+).*Listener\((\w+)")
ovverridenFunction = re.compile("@[Oo]verride")
finishDeclaration = re.compile("{")

def getFilePath(droidFilePath):
    droidFilePath = droidFilePath.replace(" ","")
    droidFilePath = droidFilePath.replace(".","/")
    droidFilePath = "/Users/shashank/Personal Projects/Skeledroid/main/java/" + droidFilePath + ".java"
    return droidFilePath

def fileAnalyser(filename):

    isOverRidden = False
    isInnerClass = False
    mjson = {}
    mjson['functions'] = {}
    mjson['functions']['own'] = {}
    mjson['functions']['overridden'] = {}
    mjson['implements'] = []
    mCurrentFunction = ""
    mIsOverridden = ""
    mjson['classname'] = ""
    mjson['extends'] = ""
    mjson['innerClass'] = []
    mjson['setContentView'] = []
    mjson['startingActivity'] = []
    mjson['startActivityName'] = []
    try:
        with open(filename, 'r') as myfile:
            data=myfile.read()
        myfile.close()
        isOverRidden = False
        for i, line in enumerate(open(filename)):
            for match in re.finditer(classPat, line):
                if mjson['classname'] == "":
                    mjson['classname'] = match.groups()
                else :
                    mjson['innerClass'].append(match.groups())
            for match in re.finditer(ovverridenFunction, line):
                isOverRidden = True
            for match in re.finditer(extendsPat, line):
                if mjson['extends'] == "":
                    mjson['extends'] = match.groups()[1]
            for match in re.finditer(implementsPat, line):
                if mjson['implements']:
                    for x in xrange(1, len(match.groups())):
                        mjson['implements'].append(match.groups()[x])
            for match in re.finditer(functionPattern, line.strip()):
                if (isOverRidden):
                    mjson['functions']['overridden']['' + match.groups()[1]] = []
                    isOverRidden = False
                    mIsOverridden = 'overridden'
                    mCurrentFunction = match.groups()[1]
                else :
                    mIsOverridden = 'own'
                    mCurrentFunction = match.groups()[1]
                    mjson['functions']['own']['' + match.groups()[1]] = []
            for match in re.finditer(functionCallPattern, line.strip()):
                mjson['functions'][mIsOverridden][mCurrentFunction].append(match.groups()[0])
            for match in re.finditer(listenersPat, line.strip()):
                mjson['functions'][mIsOverridden][mCurrentFunction].append(match.groups()[0])
            for match in re.finditer(startActivityPattern, line):
                filematch = re.search(r'import(.*'+match.groups()[0]+').*;',data)
                if filematch:
                    mjson['startingActivity'].append(getFilePath(filematch.group(1)))
                    mjson['startActivityName'].append(match.groups()[0])
            for match in re.finditer(contentviewPat, line):
                mjson['setContentView'].append(match.groups()[0])
        myfile.close()
        return mjson
    except IOError as e:
        print "error"
    finally:
        return mjson

addedFiles = []
addedStartClasses = []
filename = sys.argv[1]
analysed = fileAnalyser(filename)
print analysed['classname']
with open('data.txt', 'w') as outfile:
    json.dump(analysed, outfile)# with open('data.txt', 'w') as outfile: #json.dump(data, outfile)
if analysed['startingActivity']:
    addedFiles = list(set(analysed['startingActivity']))
    addedStartClasses = list(set(analysed['startActivityName']))
print addedStartClasses


i =0
while i < len(addedFiles):
    analysed = fileAnalyser(addedFiles[i])
    with open('data.txt', 'a') as outfile:
        outfile.write("\n")
        json.dump(analysed, outfile)# with open('data.txt', 'w') as outfile: #json.dump(data, outfile)
    if analysed['startingActivity']:
        addedFiles = addedFiles + list(set(sorted(analysed['startingActivity'])) - set(sorted(addedFiles)))
        addedStartClasses = addedStartClasses + list(set(sorted(analysed['startActivityName'])) - set(sorted(addedStartClasses)))
    print i
    print len(addedFiles)
    i += 1
    if (i == len(addedFiles)):
        print addedStartClasses




