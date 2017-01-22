#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom
import glob, os
import json
from lxml import etree

pwd = "/Users/shashank/Personal Projects/Skeledroid/"
pcwd = pwd + "main/res-profile/layout/"
styleDoc = etree.parse ( pwd + "testing/masterStyleSheet.xml" )
dimenDoc = etree.parse ( pwd + "testing/masterDimenSheet.xml" )
colorDoc = etree.parse ( pwd + "testing/masterColorSheet.xml" )
stringDoc = etree.parse ( pwd + "testing/masterStringSheet.xml" )

def iterate_children(parent):
    child = parent.firstChild
    while child != None:
        yield child
        child = child.nextSibling

def openTag(data,space,customUIClass):
  if customUIClass in data:
    if data[customUIClass]['extends'] in data:
      print '  '*space + '<' + data[data[customUIClass]['extends']]['extends']
    else :
      print '  '*space + '<' + data[customUIClass]['extends']
  else :
    print '  '*space + '<' + customUIClass

def attachAttributes(child,space):
  style = None
  for item in child.attributes.items():
    if not ("tools" in str(item[0]) or "bind" in str(item[0])) :
      if ("style" in str(item[0])) or ("them" in str(item[0])):
        try:
          style = styleDoc.xpath("//style[@name=\""+str(item[1]).replace("@style/","")+"\"]")[0] 
        except IndexError as e:
          pass
      elif "@dimen" in str(item[1]):
        try:
          dimension = dimenDoc.xpath("//dimen[@name=\""+str(item[1]).replace("@dimen/","")+"\"]")[0]
          print '   '*space + item[0] +"="+ "\"" + dimension.text + "\""    
        except IndexError as e:
          print '   '*space + item[0] +"="+ "\"" + "0dp" + "\""    
          pass
      elif "@color" in str(item[1]):
        try:
          color = colorDoc.xpath("//color[@name=\""+str(item[1]).replace("@color/","")+"\"]")[0]
          print '   '*space + item[0] +"="+ "\"" + color.text + "\""    
        except IndexError as e:
          pass
      elif "@string" in str(item[1]):
        try:
          string = stringDoc.xpath("//string[@name=\""+str(item[1]).replace("@string/","")+"\"]")[0]
          print '   '*space + item[0] +"="+ "\"" + string.text + "\""
        except IndexError as e:
          pass
      else:
        print '   '*space + item[0] +"="+ "\"" + item[1] + "\""
  if style:
    for styleItem in style.getchildren():
      styleNotInItemChild = True
      for item in child.attributes.items():
          if styleItem.attrib["name"] in item[0]:
              styleNotInItemChild = False
      if styleNotInItemChild:
        print '   '*space + styleItem.attrib['name'] +"="+ "\"" + styleItem.text + "\""   
  print "  "*space + ">"

def closeTag(data,space,customUIClass):
  if not (customUIClass == "include" or customUIClass == "layout" or customUIClass == "import" \
    or customUIClass == "data" or customUIClass == "variable" or customUIClass == "merge" ):
        if customUIClass in data:
          if data[customUIClass]['extends'] in data:
            print '  '*space + "</" + data[data[customUIClass]['extends']]['extends'] +">" 
          else:
            print '  '*space + "</" + data[customUIClass]['extends'] +">"
        else :
          print '  '*space + "</" + customUIClass + ">"

def findFileAndParse(filename,space):
  for root, dirs, files in os.walk(pwd+"/main"):
    for file in files:
      if file.endswith(filename):
        fileFullPath = os.path.join(root, file)
        parseAndroidXmlDom(fileFullPath,space)
        return

def parseChild(parent,space):
  for child in iterate_children(parent):
    if child.nodeType != child.TEXT_NODE and child.nodeType != child.COMMENT_NODE:
      custom = child.tagName.split(".")
      customUIClass = custom[len(custom) - 1]
      if customUIClass == "include":
        layout = child.getAttribute("layout").replace("@layout/","") + ".xml"
        findFileAndParse(layout,space)
      else :
        if not (customUIClass == "include" or customUIClass == "layout" or customUIClass == "import" or customUIClass == "data" or customUIClass == "variable"):
          openTag(data,space,customUIClass)
          attachAttributes(child,space)
      parseChild(child,space+1)
      closeTag(data,space,customUIClass)

def parseAndroidXmlDom(file,space):
  DOMTree = xml.dom.minidom.parse(file)
  collection = DOMTree.documentElement
  custom = collection.tagName.split(".")
  customUIClass = custom[len(custom) - 1]
  if not (customUIClass== "merge" or customUIClass == "layout"):
    openTag(data,space,customUIClass)
    attachAttributes(collection,space)
  parseChild(collection,space)
  closeTag(data,space,customUIClass)


json_data = open(pwd + "testing/data.json")
data = json.load(json_data)

layoutFile = str(data['EditPracticeActivity']['setContentView'][0]).replace("R.layout.","") + ".xml"
findFileAndParse(layoutFile,1)