#!/usr/bin/env python3

# Rob Walker - rob@ladle.net
# (c) 2020, GPL v3
#
# An export from MultiCharts gives us a single xml file.
# This script will parse that file, and break out some of the
# files that are inside of the archive.
#

import xml.etree.ElementTree as ET
import base64
import binascii
import os
import sys
from pathlib import Path as path

DEBUG = 0

def decodeLongName(longName):
    fileType = "a"
    shortName = ""
    if (longName[0] == 'f'):
        fileType = "function"
    elif (longName[0] == 's'):
        fileType = "strategy"
    elif (longName[0] == 'i'):
        fileType = "indicator"
    else:
        fileType = "other"
    if (longName[1] != '_'):
        shortNameDelimiter = longName[1]
        i = 3
        while (i < len(longName)):
            if (DEBUG == 1):
                print ("longName " + str(i) + " : " + longName[i])
            if (longName[i] == shortNameDelimiter):
                shortNameSpecial = longName[i + 1] + longName [i + 2]
                if (DEBUG == 1):
                    print ("Special character : " + shortNameSpecial)
                i = i + 2
                if (shortNameSpecial == "20"):
                    shortName = shortName + " "
                elif (shortNameSpecial == "21"):
                    shortName = shortName + "!"
                elif (shortNameSpecial == "23"):
                    shortName = shortName + "#"
                elif (shortNameSpecial == "24"):
                    shortName = shortName + "$"
                elif (shortNameSpecial == "25"):
                    shortName = shortName + "%"
                elif (shortNameSpecial == "26"):
                    shortName = shortName + "&"
                elif (shortNameSpecial == "28"):
                    shortName = shortName + "("
                elif (shortNameSpecial == "29"):
                    shortName = shortName + ")"
                elif (shortNameSpecial == "2c"):
                    shortName = shortName + ","
                elif (shortNameSpecial == "2d"):
                    shortName = shortName + "-"
                elif (shortNameSpecial == "2e"):
                    shortName = shortName + "."
                elif (shortNameSpecial == "2f"):
                    # '/' could be a directory delimiter, so we will
                    # substitute an '_'
                    # shortName = shortName + "/"
                    shortName = shortName + "_"
                elif (shortNameSpecial == "3c"):
                    # '<' isn't working in the filename, so we will
                    # substitute an 'lt'
                    # shortName = shortName + "<"
                    shortName = shortName + "lt"
                elif (shortNameSpecial == "3e"):
                    # '<' isn't working in the filename, so we will
                    # substitute an 'gt'
                    # shortName = shortName + ">"
                    shortName = shortName + "gt"
                else:
                    print("Unknown special character, please report")
                    print("this at https://github.com/biffhero/mcExport/issues")
                    print("Include the special character in the report")
                    print("report : " + shortNameSpecial)
                    exit()
            else:
                shortName = shortName + longName[i]
            if (DEBUG == 1):
                print ("Short name : " + shortName)
            i = i + 1
    else:
        shortName = longName[2:]  
    if (DEBUG == 1):
        print("")
        print("Long Name: ", longName)
        print(" fileType : ", fileType)
        print(" Short Name: ", shortName)
    return fileType, shortName

def main():
    file = sys.argv[1]    
    tree = ET.parse(file)
    root = tree.getroot()
    for gn in root:
        if (DEBUG == 1):
            print("gn : ", gn.tag, gn.attrib)
        for gnd in gn:
            if (gnd.tag == "data"):
                if (DEBUG == 1):
                    print("gnd data: ", gnd.tag, gnd.attrib)
                    print(" tag: ", gnd.tag)
                    print(" attrib : ", gnd.attrib)
                    print(" first : ", gnd.attrib['first'])
                longName = gnd.attrib['first']
                fileType, shortName = decodeLongName(longName)
            elif (gnd.tag == "NodeText"):
                if (DEBUG == 1):
                    print("encoded: ", gnd.tag, gnd.attrib)
                    print(" tag: ", gnd.tag)
                    print(" attrib : ", gnd.attrib)
                    print(" text : ", gnd.text)
                text = gnd.text
                textProgram = base64.urlsafe_b64decode(text)
                if (DEBUG == 1):
                    print(" program : ", textProgram)
                if not os.path.exists("mc"):
                    os.mkdir("mc")
                if (fileType == "function"):
                    if not os.path.exists("mc/functions"):
                        os.mkdir("mc/functions")
                    fileDirectory = path("mc/functions")
                if (fileType == "strategy"):
                    if not os.path.exists("mc/strategies"):
                        os.mkdir("mc/strategies")
                    fileDirectory = path("mc/strategies")
                if (fileType == "indicator"):
                    if not os.path.exists("mc/indicators"):
                        os.mkdir("mc/indicators")
                    fileDirectory = path("mc/indicators") 
                if (fileType == "other"):
                    if not os.path.exists("mc/other"):
                        os.mkdir("mc/other")
                    fileDirectory = path("mc/other") 
                shortName = shortName + '.eld'
                outputFile = fileDirectory / shortName
                fo = open(outputFile, 'wb')
                fo.write(textProgram)
                fo.close()
            elif (gnd.tag != "data"):
                1
                if (DEBUG == 1):
                    print("gnd other: ", gnd.tag, gnd.attrib)
                    print(" tag: ", gnd.tag)
                    print(" attrib : ", gnd.attrib)

if __name__ == "__main__":
    main()
