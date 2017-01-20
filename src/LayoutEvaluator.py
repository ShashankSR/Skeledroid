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
    parseChild(child,space+1)
    if child.nodeType != child.TEXT_NODE and child.nodeType != child.COMMENT_NODE:
      if child.tagName == "include":
        layout = child.getAttribute("layout").replace("@layout/","")
        for root, dirs, files in os.walk(pwd+"/main"):
          for file in files:
            if file.endswith(layout+".xml"):
              fileFullPath = os.path.join(root, file)
              parseAndroidXmlDom(fileFullPath,space+1)
              break
      else :
        print ''*space + child.tagName 


def parseAndroidXmlDom(file,space):
  DOMTree = xml.dom.minidom.parse(file)
  collection = DOMTree.documentElement
  print ''*space + collection.tagName 
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