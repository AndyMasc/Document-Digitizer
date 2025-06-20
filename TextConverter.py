import cv2
import pytesseract
from tkinter.filedialog import askopenfilename

def getImageFile():
    imageFile = askopenfilename()
    return imageFile

def preprocessImage(image):
    GreyScaleImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Converting image to gray-scale enhances text differentiation
    normalizedImage = cv2.normalize(GreyScaleImage, None, 0, 255, cv2.NORM_MINMAX)
    return normalizedImage

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  # for Apple Silicon

image = cv2.imread(getImageFile())
processedImage = preprocessImage(image)

text = pytesseract.image_to_string(processedImage)
print(text)