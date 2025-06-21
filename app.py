from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
import cv2
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = ''
    if request.method == 'POST':
        file = request.files['upload']
        filename = secure_filename(file.filename)
        global target
        target = os.path.join('UPLOAD_FOLDER', filename)
        file.save(target)
        convertImage()
        with open('textFile.txt', 'r') as output:
            extracted_text = output.read()
        os.remove('textFile.txt')
    return render_template('index.html', text=extracted_text)

def convertImage():
    global target
    image = cv2.imread(target)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    text = pytesseract.image_to_string(image)
    os.remove(target)

    with open('textFile.txt', 'w') as textFile:
        textFile.write(text)

if __name__ == '__main__':
    target = ''
    app.run(debug=True)