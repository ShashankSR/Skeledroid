#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom


pwd = "/Users/shashank/Personal Projects/Skeledroid/"
# Open XML document using minidom parser
DOMTree = xml.dom.minidom.parse(pwd + "main/AndroidManifest.xml")
collection = DOMTree.documentElement
if collection.hasAttribute("shelf"):
   print "Root element : %s" % collection.getAttribute("shelf")

# Get all the movies in the collection
permissions = collection.getElementsByTagName("uses-permission")
activities = collection.getElementsByTagName("activity")
services = collection.getElementsByTagName("service")
launcherActivity = ""
# Print detail of each movie.
count = 0
for permission in permissions:
   if permission.hasAttribute("android:name"):
      #print "%s" % permission.getAttribute("android:name").replace("android.permission.","")
      count += 1
print "Permission count %d " % count

count = 0
for service in services:
   if service.hasAttribute("android:name"):
      #print "%s" % permission.getAttribute("android:name").replace("android.permission.","")
      count += 1
print "Service count %d " % count

count = 0
count2 = 0
for activity in activities:
    if activity.hasAttribute("android:name"):
        #print "%s" % activity.getAttribute("android:name")
        count += 1
    for intent in activity.getElementsByTagName("intent-filter"):
        count2 += 1
        for category in intent.getElementsByTagName("category"):
            if (category.getAttribute("android:name") == "android.intent.category.LAUNCHER"):
                launcherActivity = activity.getAttribute("android:name")

print "Activity count %d" % count
print "Activites with other entry point %d" % count2
print "Laucnher Activity %s" % launcherActivity
