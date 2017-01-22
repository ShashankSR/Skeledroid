#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom
import glob,os
import re
import sys
from lxml import etree

pwd = "/Users/shashank/Personal Projects/Skeledroid/"

pwcd = pwd + "/testing/"
fileCount = 0

def getDrawableFile(drawable):
    for root, dirs, files in os.walk(pwd+"/main"):
        for file in files:
            stringFile = drawable.replace("@drawable/","")
            if re.match(r'color.*\.xml',file) :
                fileFullPath = os.path.join(root, file)
                return fileFullPath
    return ""

def iterate_children(parent):
    child = parent.firstChild
    while child != None:
        yield child
        child = child.nextSibling

dataMain = etree.fromstring("<book></book>")
for root, dirs, files in os.walk(pwd+"/main"):
    for file in files:
        if re.match(r'style.*\.xml',file) :
            fileFullPath = os.path.join(root, file)
            data = etree.parse ( fileFullPath )
            for item in data.xpath("//style"):
                dataMain.append(item)
            fileCount += 1
with open(pwd + 'testing/'+ 'masterStyleSheet.xml', 'w') as outfile:
    try:
        outfile.write(etree.tostring(dataMain,pretty_print=True))
    except IndexError as e:
        print ("-----------No Classname Error------------")
print fileCount

fileCount = 0
dimenFileList = []
dataMain = etree.fromstring("<book></book>")
for root, dirs, files in os.walk(pwd+"/main"):
    for file in files:
        if re.match(r'dimen.*\.xml',file) :
            fileFullPath = os.path.join(root, file)
            data = etree.parse ( fileFullPath )
            for item in data.xpath("//dimen"):
                dataMain.append(item)
            fileCount += 1
with open(pwd + 'testing/'+ 'masterDimenSheet.xml', 'w') as outfile:
    try:
        outfile.write(etree.tostring(dataMain,pretty_print=True))
    except IndexError as e:
        print ("-----------No Classname Error------------")
print fileCount

fileCount = 0
colorFileList = []
dataMain = etree.fromstring("<book></book>")
for root, dirs, files in os.walk(pwd+"/main"):
    for file in files:
        if re.match(r'color.*\.xml',file) :
            fileFullPath = os.path.join(root, file)
            data = etree.parse ( fileFullPath )
            for item in data.xpath("//color"):
                dataMain.append(item)
            fileCount += 1
with open(pwd + 'testing/'+ 'masterColorSheet.xml', 'w') as outfile:
    try:
        outfile.write(etree.tostring(dataMain,pretty_print=True))
    except IndexError as e:
        print ("-----------No Classname Error------------")
print fileCount

dataMain = etree.fromstring("<book></book>")
for root, dirs, files in os.walk(pwd+"/main"):
    for file in files:
        if re.match(r'string.*\.xml',file) :
            fileFullPath = os.path.join(root, file)
            data = etree.parse ( fileFullPath )
            for item in data.xpath("//string"):
                dataMain.append(item)
            fileCount += 1
with open(pwd + 'testing/'+ 'masterStringSheet.xml', 'w') as outfile:
    try:
        outfile.write(etree.tostring(dataMain,pretty_print=True))
    except IndexError as e:
        print ("-----------No Classname Error------------")
print fileCount

dimenDoc = etree.parse ( pwd + "testing/masterDimenSheet.xml" )
dimensions = dimenDoc.xpath("//dimen")
for item in dimensions:
    if ("@dimen" in item.text):
        try:
            strXpath = '//dimen[@name=\"'+item.text.replace("@dimen/","")+'\"]'
            dimen = dimenDoc.xpath(strXpath)[0].text
            while "@dimen" in dimen:
                dimen = doc.xpath('//dimen[@name=\"'+item.text.replace("@dimen/","")+'\""]')[0].text
            item.text = dimen
        except IndexError as e:
            print "error"
with open(pwd + 'testing/'+ 'masterDimenSheet.xml', 'w') as outfile:
    dimenDoc.write(outfile, pretty_print=True)

colorDoc = etree.parse ( pwd + "testing/masterColorSheet.xml" )
colors = colorDoc.xpath("//color")
for item in colors:
    if ("@color" in item.text):
        try:
            strXpath = '//color[@name=\"'+item.text.replace("@color/","")+'\"]'
            dimen = colorDoc.xpath(strXpath)[0].text
            while "@dimen" in dimen:
                dimen = colorDoc.xpath('//color[@name=\"'+item.text.replace("@color/","")+'\"]')[0].text
            item.text = dimen
        except IndexError as e:
            print "error"
with open(pwd + 'testing/'+ 'masterColorSheet.xml', 'w') as outfile:
    colorDoc.write(outfile, pretty_print=True)


styleDoc = etree.parse ( pwd + "testing/masterStyleSheet.xml" )
items = styleDoc.xpath("//item")
for item in items:
    try:
        if "@dimen" in item.text:
            item.text = dimenDoc.xpath('//dimen[@name=\"'+' '.join(item.text.replace("@dimen/","").split())+'\"]')[0].text
        if "@color" in item.text:
            item.text = colorDoc.xpath('//color[@name=\"'+' '.join(item.text.replace("@color/","").split())+'\"]')[0].text
    except IndexError as e:
        print "error"
with open(pwd + 'testing/'+ 'masterStyleSheet.xml', 'w') as outfile:
    styleDoc.write(outfile, pretty_print=True)

items = styleDoc.xpath("//style")
for item in items:
    try:
        if "parent" in item.attrib :
            parent = styleDoc.xpath("//style[@name=\""+item.attrib["parent"]+"\"]")[0]
            while parent:
                for child in parent.getchildren():
                    notInItemChild = True
                    for itemChild in item.getchildren():
                        if child.attrib["name"] in itemChild.attrib["name"]:
                            notInItemChild = False
                            break
                    if notInItemChild:
                        item.append(child)
                parent = styleDoc.xpath("//style[@name=\""+parent.attrib["parent"]+"\"]")[0]
    except IndexError as e:
        pass
    except KeyError as e:
        pass

with open(pwd + 'testing/'+ 'masterStyleSheet.xml', 'w') as outfile:
    styleDoc.write(outfile, pretty_print=True)


