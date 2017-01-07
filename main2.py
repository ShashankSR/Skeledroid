import re
import json
import pprint

replaceFragmentPattern= ""
functionCallPattern = re.compile("^\s*(\w+)\(.*\);")
startActivityPattern = re.compile("(\w+)(.start\(|.startActivity.*\()(\s*\w+\))")
functionPattern = re.compile("(public|protected|private|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\(([^\)]*)\) *(\{?|[^;])")
contentviewPat = re.compile("(setContentView)*(^;)")
classPat = re.compile("class (\w+)");
extendsPat = re.compile("class (\w+) .* extends (\w+)");
implementsPat = re.compile("class (\w+).+implements (.+){")
listenersPat = re.compile("^(\w+)\.(\w+).*Listener\((\w+)")
layoutFilePat = re.compile("(R.layout.\w+)")
ovverridenFunction = re.compile("@[Oo]verride")
isOverRidden = False
mjson = {};
mjson['functions'] = {}
mjson['functions']['own'] = {}
mjson['functions']['overridden']={}
mjson['implements'] = []
mCurrentFunction = ""
mIsOverridden = ""

with open('test.java', 'r') as myfile:
    data=myfile.read()

match = re.search(r'(public|protected|private|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *(?:\{?|[^;])',data,re.DOTALL)
match = re.search(r'class (\w+).+implements (.+){', data, re.DOTALL)


for match in re.finditer(classPat,line):
        mjson['classname'] = match.groups()
    for match in re.finditer(ovverridenFunction,line):
        isOverRidden = True
    for match in re.finditer(extendsPat, line):
        mjson['extends'] = match.groups()[1]
    for match in re.finditer(functionPattern, line.strip()):
        if(isOverRidden):
            mjson['functions']['overridden'][''+match.groups()[1]] = []
            isOverRidden = False
            mIsOverridden = 'overridden'
            mCurrentFunction = match.groups()[1]
        else:
            mIsOverridden = 'own'
            mCurrentFunction = match.groups()[1]
            mjson['functions']['own'][''+match.groups()[1]] = []
    for match in re.finditer(functionCallPattern, line.strip()):
        mjson['functions'][mIsOverridden][mCurrentFunction].append(match.groups()[0])
    for match in re.finditer(listenersPat, line.strip()):
        mjson['functions'][mIsOverridden][mCurrentFunction].append(match.groups()[0])
    for match in re.finditer(startActivityPattern, line):
        mjson['functions'][mIsOverridden][mCurrentFunction].append(match.groups())
    for match in re.finditer(contentviewPat, line):
        print 'Found on line %s: %s' % (i+1, match.groups())


print mjson
with open('data.txt', 'w') as outfile:
    json.dump(mjson, outfile)
#with open('data.txt','w') as outfile:
#    json.dump(data,outfile)
    	
