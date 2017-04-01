from PIL import Image
import sys

def resize(img, height=8, width=8):
	img = img.resize((height, width))
	return img

def convertRGB(img):
	return img.convert("RGB")

#Attempt to resize any given image to be crudely displayed on the senseHAT screen
img = Image.open(sys.argv[1])
print(img.format, img.size, img.mode)
img = resize(img)
img = convertRGB(img)
print(img.getpixel((0,0)))
print(img.getpixel((5,5)))
img.save("iso.png","PNG")