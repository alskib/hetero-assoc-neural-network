#franklin leung
import Image
import re
from sys import exit

imageName = "a.png"

def WhiteLoop(direction, imageName):
    im = Image.open(imageName)
    pixels = im.load()
    width, height = im.size
    if (direction is "top"):
        for y in range(height):
            for x in range(width):
                #print pixels[x, y], "on pixel[" + str(x) + ",", str(y) + "]"
                match = re.match(r'\((\d+), (\d+), (\d+)\)', str(pixels[x, y]))
                v1 = int(match.group(1))
                v2 = int(match.group(2))
                v3 = int(match.group(3))
                if (v1 != 255 or v2 != 255 or v3 != 255):
                    box = (0, y, width, height)
                    newimage = im.crop(box)
                    newimage.save(imageName)
                    print "Top has been cropped."
                    return 0
    elif (direction is "left"):
        for x in range(width):
            for y in range(height):
                match = re.match(r'\((\d+), (\d+), (\d+)\)', str(pixels[x, y]))
                v1 = int(match.group(1))
                v2 = int(match.group(2))
                v3 = int(match.group(3))
                if (v1 != 255 or v2 != 255 or v3 != 255):
                    box = (x, 0, width, height)
                    newimage = im.crop(box)
                    newimage.save(imageName)
                    print "Left has been cropped."
                    return 0
    elif (direction is "right"):
        for x in reversed(range(width)):
            for y in range(height):
                match = re.match(r'\((\d+), (\d+), (\d+)\)', str(pixels[x, y]))
                v1 = int(match.group(1))
                v2 = int(match.group(2))
                v3 = int(match.group(3))
                if (v1 != 255 or v2 != 255 or v3 != 255):
                    box = (0, 0, x + 1, height)
                    newimage = im.crop(box)
                    newimage.save(imageName)
                    print "Right has been cropped."
                    return 0
    elif (direction is "bottom"):
        for y in reversed(range(height)):
            for x in range(width):
                match = re.match(r'\((\d+), (\d+), (\d+)\)', str(pixels[x, y]))
                v1 = int(match.group(1))
                v2 = int(match.group(2))
                v3 = int(match.group(3))
                if (v1 != 255 or v2 != 255 or v3 != 255):
                    box = (0, 0, width, y + 1)
                    newimage = im.crop(box)
                    newimage.save(imageName)
                    print "Bottom has been cropped."
                    return 0
    else:
        print "Incorrect direction specified. Exiting."
        exit(0)

WhiteLoop("top", imageName)
WhiteLoop("left", imageName)
WhiteLoop("right", imageName)
WhiteLoop("bottom", imageName)
