import sys, random, argparse
import numpy as np
import math

from PIL import Image, ImageDraw

#Gray scale level values from:  
#http://paulbourke.net/dataformats/asciiart/ 

#70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
#10 levels of gray
gscale2 = "@%#*+=-:. "

def getAverage(image):
    #Get image as numpy array
    im = np.array(image)

    #Get shape
    w, h = im.shape

    #Get average
    return np.average(im.reshape(w*h))

def convertImageToASCII(fileName, cols, scale, moreLevels):
    #Declare global
    global gscale1, gscale2

    #Open image and convert to grayscale
    image = Image.open(fileName).convert('L')

    #Store dimension
    W, H = image.size[0], image.size[1]

    #Compute width of tile
    w = W/cols

    #Compute tile height base on aspect ratio and scale
    h = w/scale

    #Compute number of rows
    rows = int(H/h)

    print("cols: %d, rows %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))

    #Check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    #ASCII image is a list of character strings
    aimg = []
    #Generate list of dimension
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)

        #Correct last tile
        if j == rows-1:
            y2 = H

        #append an empty string
        aimg.append("")

        for i in range(cols):
            #Crop image to tile
            x1 = int(i*w)
            x2 = int((i+1)*w)

            #Correct last tile
            if (i == cols-1):
                x2 = W

            #Crop image to extract tile
            img = image.crop((x1, y1, x2, y2))

            #Get average luminance
            avg = int(getAverage(img))

            #Look up ASCII char
            if moreLevels:
                gsval = gscale1[int((avg*69)/255)]
            else:
                gsval = gscale2[int((avg*9)/255)]

            #Apeend ASCII char to string
            aimg[j] += gsval

    #return txt image
    return aimg

#main() function
def main():
    #Create parser
    descStr = "This program converts an image into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)
    #Add expected arguments
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--morelevels', dest='moreLevels', action='store_true')

    #Parse args
    args = parser.parse_args()

    imgFile = args.imgFile

    #Set ouput file
    outFile = 'out'
    if args.outFile:
        outFile = args.outFile

    #Set scale default as 0.43 (fit courier font)
    scale = 0.43
    if args.scale:
        scale = float(args.scale)

    #Set cols
    cols = 80
    if args.cols:
        cols = int(args.cols)

    print('generating ASCII art...')
    #Convert image to ASCII txt
    aimg = convertImageToASCII(imgFile, cols, scale, args.moreLevels)
    #Draw simple image
    img = Image.new('RGB', (cols * 6, len(aimg[0]) * 8), color = 'white')
    img.save(outFile + ".jpg")
    d = ImageDraw.Draw(img)

    #Open file
    f = open(outFile, 'w')

    #Write to file
    for rowIndex, row in enumerate(aimg):
        f.write(row + '\n')
        for colIndex, col in enumerate(row):
            d.text((colIndex * 6, rowIndex * 8), col, fill= 'black')
            img.save(outFile + ".jpg")
        

    #Cleanup
    f.close()
    print("ASCII art written to %s" % outFile)
    img.save(outFile + ".jpg")


# call main 
if __name__ == '__main__': 
    main() 