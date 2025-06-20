from bottle import route, run, template
from TextConverter import *

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  # for Apple Silicon

@route('/')
def ImageToText():
    image = cv2.imread(getImageFile())
    processedImage = preprocessImage(image)
    text = pytesseract.image_to_string(processedImage)
    return text

run(host='localhost', port=8080, debug=True, reloader=True)