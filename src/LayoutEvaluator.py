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

def parseChild(parent,space):
  for child in iterate_children(parent):
    if child.nodeType != child.TEXT_NODE and child.nodeType != child.COMMENT_NODE:
      customUIClass = ""
      custom = ""
      if child.tagName == "include":
        layout = child.getAttribute("layout").replace("@layout/","")
        for root, dirs, files in os.walk(pwd+"/main"):
          for file in files:
            if file.endswith(layout+".xml"):
              fileFullPath = os.path.join(root, file)
              parseAndroidXmlDom(fileFullPath,space+1)
              break
      else :
        if not (child.tagName == "include" or child.tagName == "layout" or child.tagName == "import" or child.tagName == "data" or child.tagName == "variable"):
          custom = child.tagName.split(".")
          if len(custom) !=0 :
            customUIClass = custom[len(custom) - 1]
            if customUIClass in data:
              print '  '*space + '<' + data[customUIClass]['extends']
            else :
              print '  '*space + '<' + customUIClass
          else :
            print '  '*space + '<' +child.tagName 
          for item in child.attributes.items():
            print '   '*space + item[0] +"="+ "\"" + item[1] + "\""
      if not (child.tagName == "include" or child.tagName == "layout" or child.tagName == "import" or child.tagName == "data" or child.tagName == "variable"):
        print "  "*space + ">"
      parseChild(child,space+1)
      if not (child.tagName == "include" or child.tagName == "layout" or child.tagName == "import" or child.tagName == "data" or child.tagName == "variable"):
        if customUIClass in data:
          print '  '*space + "</" + data[customUIClass]['extends'] +">"
        else :
          print '  '*space + "</" + customUIClass + ">"
        #print child.attributes.items()


def parseAndroidXmlDom(file,space):
  DOMTree = xml.dom.minidom.parse(file)
  collection = DOMTree.documentElement
  if not (collection.tagName == "merge" or collection.tagName == "layout"):
    print '<'*space + collection.tagName 
  parseChild(collection,space)

json_data = open(pwd + "testing/data.json")
data = json.load(json_data)

layoutFile = str(data['SignInActivity']['setContentView'][0]).replace("R.layout.","") + ".xml"
for root, dirs, files in os.walk(pwd+"/main"):
    for file in files:
        if file.endswith(layoutFile):
             fileFullPath = os.path.join(root, file)
             parseAndroidXmlDom(fileFullPath,1)

# ignore layout import variable data


#parseAndroidXmlDom(pcwd+"activity_profile_edit_practice.xml",1)