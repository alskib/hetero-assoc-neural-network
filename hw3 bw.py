#franklin leung
import Image # Python Imaging Library
import os
import sys
import shutil
import numpy as np
import random

# Prints the entire matrix to console, rather than shortening it and omitting some data from view
np.set_printoptions(threshold='nan') 

# Print image as 1s and 0s as imported by PIL 
def printImage(imageName):
    im = Image.open(imageName)
    pixels = im.getdata()
    width, height = im.size
    print width, height

    for i, x in enumerate(pixels):
        print x,
        if (i % width == (width - 1)):
            print
    print

# Crop image, removing excess whitespace
def Crop(direction, imageName): 
    im = Image.open(imageName)
    pixels = im.load()
    width, height = im.size
    if (direction is "top"):    # Start processing from top row (0,0)
        for y in range(height):
            for x in range(width):
                if (pixels[x, y] == 0):
                    box = (0, y, width, height)
                    newimage = im.crop(box)
                    newimage.save(imageName)
                    return 0
    elif (direction is "left"):
        for x in range(width):
            for y in range(height):
                if (pixels[x, y] == 0):
                    box = (x, 0, width, height)
                    newimage = im.crop(box)
                    newimage.save(imageName)
                    return 0
    elif (direction is "right"):
        for x in reversed(range(width)):
            for y in range(height):
                if (pixels[x, y] == 0):
                    box = (0, 0, x + 1, height)
                    newimage = im.crop(box)
                    newimage.save(imageName)
                    return 0
    elif (direction is "bottom"):
        for y in reversed(range(height)):
            for x in range(width):
                if (pixels[x, y] == 0):
                    box = (0, 0, width, y + 1)
                    newimage = im.crop(box)
                    newimage.save(imageName)
                    return 0
    else:
        print "Incorrect direction specified. Exiting."
        exit(0)

# Collection of crops for all directions
def CropAll(imageName): 
    Crop("top", imageName)
    Crop("left", imageName)
    Crop("right", imageName)
    Crop("bottom", imageName)

# Resize image from original to size (specified in function)
def resize(imageName):  
    size = 10, 10   # Output size
    im = Image.open(imageName)
##    im.thumbnail(size, Image.ANTIALIAS)   # Keeps aspect ratio, will only resize until one dimension (either x or y) matches specified size
    im = im.resize(size, Image.ANTIALIAS)   # Ignores aspect ratio, forces both x and y to match
    im.save(imageName)

# Convert list from PIL representation of black/white (where 0 is black) to NN method (1 is black)
def swapBinary(listItem):
    newList = []
    for x in listItem:
        if (x == 1):
            newList.extend([0])
        if (x == 0):
            newList.extend([1])
    return newList

# Print input list (10x10) into a pretty image
def imagePrintInputList(listItem, noise=0):  
    targetWidth = 10
    for i, x in enumerate(listItem):
        if noise is 1:
            if x is 0:
                print '?',
            else:
                print x,
        else:
            print x,
        if (i % targetWidth == (targetWidth - 1)):
            print

# Print output list (3x5) into a pretty image
def imagePrintOutputList(listItem): 
    width = 3
    print
    for i, x in enumerate(listItem):
        if x is 1:
            print '#',
        if x is -1:
            print '-',
        if (i+1) % width is 0:
            print
    print

# Convert image data to a list structure
def convertImageToList(imageName):   
    im = Image.open(imageName)
    pixels = im.getdata()
    width, height = im.size
    imageList = []
    targetWidth = 10    # Intended to match 'size = ' in resize() function

    # insert image's pixel values into new list
    for x in pixels:
        imageList.extend([x])

    imageList = swapBinary(imageList)

    # Print newly resized image
    imagePrintInputList(imageList)
    print
    
    im.save(imageName)

    return imageList

# Collection of functions from initial image to final list (to be fed into NN)
def ImageToList(image): 
    CropAll(image)
    printImage(image)
    resize(image)
    return convertImageToList(image)

# Yin function for bipolar matrices
def yIn_Bipolar(matrix):    
    newTemp = []
    for x in np.nditer(matrix.copy(order='C')):
        if x > 0:
            newTemp.extend([1])
        if x is 0:
            newTemp.extend([0])
        if x < 0:
            newTemp.extend([-1])
    return newTemp

# Introduce random noise into matrix
def randomNoise(matrix):    
    newTemp = []
    for x in np.nditer(matrix):
        if random.randint(1, 2) is 1:
            newTemp.extend([0])
        else:
            newTemp.extend([x])
    imagePrintInputList(newTemp, 1)
    return np.mat(newTemp)

# Hetero-associative neural network
def heteroAssoc(aList, tList, xList):
    # Create matrix from list of values
    a = np.mat(aList)
    t = np.mat(tList)
    x = np.mat(xList)

    # Create matrices of output pairs
    aTarget = np.mat([-1, 1, -1, 1, -1, 1, 1, 1, 1, 1, -1, 1, 1, -1, 1])
    tTarget = np.mat([1, 1, 1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1])
    xTarget = np.mat([1, -1, 1, 1, -1, 1, -1, 1, -1, 1, -1, 1, 1, -1, 1])

    # Calculate weights matrix
    weights = (a.T * aTarget
             + t.T * tTarget
             + x.T * xTarget
               )
    
    print weights

    # Recall
    imagePrintOutputList(yIn_Bipolar(a * weights))
    imagePrintOutputList(yIn_Bipolar(t * weights))
    imagePrintOutputList(yIn_Bipolar(x * weights))

    # Noisy recall
    imagePrintOutputList(yIn_Bipolar(randomNoise(a) * weights))
    imagePrintOutputList(yIn_Bipolar(randomNoise(t) * weights))
    imagePrintOutputList(yIn_Bipolar(randomNoise(x) * weights))
      
def main():
    imageAorig = "a orig.png"
    imageA = "a result2.png"
    shutil.copyfile(imageAorig, imageA)

    imageTorig = "t orig.png"
    imageT = "t result2.png"
    shutil.copyfile(imageTorig, imageT)

    imageXorig = "x orig.png"
    imageX = "x result2.png"
    shutil.copyfile(imageXorig, imageX)
    
    heteroAssoc(ImageToList(imageA), ImageToList(imageT), ImageToList(imageX))

main()

    
