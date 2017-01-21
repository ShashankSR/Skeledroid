#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom
import glob, os
import json

pwd = "/Users/shashank/Personal Projects/Skeledroid/"
pcwd = pwd + "main/res-profile/layout/"

def iterate_children(parent):
    child = parent.firstChild
    while child != None:
        yield child
        child = child.nextSibling

def attachAttributes(child,space):
  for item in child.attributes.items():
    if not ("tools" in str(item[0]) or "bind" in str(item[0])) :
      print '   '*space + item[0] +"="+ "\"" + item[1] + "\""
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

def parseChild(parent,space):
  for child in iterate_children(parent):
    if child.nodeType != child.TEXT_NODE and child.nodeType != child.COMMENT_NODE:
      custom = child.tagName.split(".")
      customUIClass = custom[len(custom) - 1]
      if customUIClass == "include":
        layout = child.getAttribute("layout").replace("@layout/","")
        for root, dirs, files in os.walk(pwd+"/main"):
          for file in files:
            if file.endswith(layout+".xml"):
              fileFullPath = os.path.join(root, file)
              parseAndroidXmlDom(fileFullPath,space+1)
              break
      else :
        if not (customUIClass == "include" or customUIClass == "layout" or customUIClass == "import" or customUIClass == "data" or customUIClass == "variable"):
          if customUIClass in data:
            if data[customUIClass]['extends'] in data:
              print '  '*space + '<' + data[data[customUIClass]['extends']]['extends']
            else :
              print '  '*space + '<' + data[customUIClass]['extends']
          else :
            print '  '*space + '<' + customUIClass
          attachAttributes(child,space)
      parseChild(child,space+1)
      closeTag(data,space,customUIClass)

def parseAndroidXmlDom(file,space):
  DOMTree = xml.dom.minidom.parse(file)
  collection = DOMTree.documentElement
  custom = collection.tagName.split(".")
  customUIClass = custom[len(custom) - 1]
  if not (customUIClass== "merge" or customUIClass == "layout"):
    if customUIClass in data:
      if data[customUIClass]['extends'] in data:
        print '  '*space + '<' + data[data[customUIClass]['extends']]['extends']
      else :
        print '  '*space + '<' + data[customUIClass]['extends']
    else :
      print '  '*space + '<' + customUIClass
    attachAttributes(collection,space)
  parseChild(collection,space)
  closeTag(data,space,customUIClass)





json_data = open(pwd + "testing/data.json")
data = json.load(json_data)

layoutFile = str(data['EditPracticeActivity']['setContentView'][0]).replace("R.layout.","") + ".xml"
for root, dirs, files in os.walk(pwd+"/main"):
    for file in files:
        if file.endswith(layoutFile):
             fileFullPath = os.path.join(root, file)
             parseAndroidXmlDom(fileFullPath,1)
