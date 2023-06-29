# Clark Otte
# Lab02 File Carving
# CSC 5347
# February 25, 2022
# Adapted some code from tutorial found at https://www.thehexninja.com/2018/01/practical-exercise-image-carving-ii.html to use regular expression library to search the file for fiel header and footer matches and write the file data between them.
# This program assumes the target file is in the same directory as the program file. It also assumes that the images are to be saved in the same directory the program is in.
import subprocess
import os
import shutil
import argparse
import sys
import re

if __name__ == "__main__":
    # parse the arguments from the command line
    parser = argparse.ArgumentParser(description="File Carving")
    
    parser.add_argument('-t', '--type', type=str, metavar='', required=True, help="Enter the type file type (jpg or pdf)")
    parser.add_argument('-f', '--filename', type=str, metavar='', required=True, help="Enter the name of the file to read")
    
    # check if there are any arguments provided, if not print help and exit
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    
    # store arguments in variables
    fileType = args.type
    fileName = args.filename
    
    # determine which start of file and end of file markers to use
    sof = ''
    eof = ''
    if fileType == 'jpg':
        sof = b"\xff\xd8\xff"
        eof = b"\xff\xd9"
    elif fileType == 'pdf':
        sof = b"\x25\x50\x44\x46"
        eof = b"\x45\x4f\x46\x0a"
    else:
        print("Not a vild file type")
        sys.exit(1)
    
    # open the file and get the data
    with open(fileName, 'rb') as binaryFile:
        data=binaryFile.read()
    
    # find the matches to the sof and eof markers and make a list of the bit positions
    sofList = [match.start() for match in re.finditer(re.escape(sof), data)]
    eofList = [match.start() for match in re.finditer(re.escape(eof), data)]
    
    # iterate through the list of sof markers and carve the data from each instance
    i=0
    for sof in sofList:
        carvedFileData=data[sof:eofList[i]+2]
        carvedFileName = "carvedFile_{}.{}".format((i+1), fileType)
        with open(carvedFileName, 'wb') as carvedFile:
            carvedFile.write(carvedFileData)
        i=i+1
        print("Found file, carved to "+carvedFileName)
