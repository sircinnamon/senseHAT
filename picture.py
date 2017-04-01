from PIL import Image
import sys
import imageResize
from sense_hat import SenseHat
sense = SenseHat()

#Attempt to display a given image on senseHAT
img = Image.open(sys.argv[1])
#print(img.format, img.size, img.mode)
#Resize the image to 8x8, mangling it horribly
img = imageResize.resize(img, 8, 8)
img = imageResize.convertRGB(img)
#convert the 64 pixels to a list
pixels = list(img.getdata())
sense.set_pixels(pixels)
#print(str(pixels))