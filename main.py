import cv2
import pytesseract

def preprocessImage(image):
    monochromeImage = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)  # Converting image to gray-scale enhances text differentiation
    normalizedImage = cv2.normalize(monochromeImage, None, 0, 255, cv2.NORM_MINMAX)
    return normalizedImage

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  # for Apple Silicon

image = cv2.imread("/Users/andymascarenhas/Downloads/test.png")

processedImage = preprocessImage(image)
text = pytesseract.image_to_string(processedImage)
print(text)