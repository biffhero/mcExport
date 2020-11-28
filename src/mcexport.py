#!/usr/bin/env python3

# Rob Walker - rob@ladle.net
# (c) 2020, GPL v3
#
# An export from MultiCharts gives us a single xml file.
# This script will parse that file, and break out some of the
# files that are inside of the archive.
#
# TODO is at the bottom of the file

import xml.etree.ElementTree as ET
import base64
import binascii
import os
import sys
from pathlib import Path as path

DEBUG = 0

def main():
    file = sys.argv[1]    
    tree = ET.parse(file)
    root = tree.getroot()
    for gn in root:
        if DEBUG:
            print("gn : ", gn.tag, gn.attrib)
        for gnd in gn:
            if (gnd.tag == "data"):
                if DEBUG:
                    print("gnd data: ", gnd.tag, gnd.attrib)
                    print(" tag: ", gnd.tag)
                    print(" attrib : ", gnd.attrib)
                    print(" first : ", gnd.attrib['first'])
                longName = gnd.attrib['first']
                if (longName[0] == 'f'):
                    fileType = "function"
                elif (longName[0] == 's'):
                    fileType = "strategy"
                elif (longName[0] == 'i'):
                    fileType = "indicator"
                else:
                    fileType = "other"
                shortName = longName[2:]    
                if DEBUG:
                    print(" name : ", shortName)
                    print(" type : ", fileType)
            elif (gnd.tag == "NodeText"):
                if DEBUG:
                    print("encoded: ", gnd.tag, gnd.attrib)
                    print(" tag: ", gnd.tag)
                    print(" attrib : ", gnd.attrib)
                    print(" text : ", gnd.text)
                text = gnd.text
                textProgram = base64.urlsafe_b64decode(text)
                if DEBUG:
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
                outputFile = fileDirectory / shortName
                fo = open(outputFile, 'wb')
                fo.write(textProgram)
                fo.close()
            elif (gnd.tag != "data"):
                1
                if DEBUG:
                    print("gnd other: ", gnd.tag, gnd.attrib)
                    print(" tag: ", gnd.tag)
                    print(" attrib : ", gnd.attrib)

if __name__ == "__main__":
    main()
