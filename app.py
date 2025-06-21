from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
import cv2
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['upload']
        filename = secure_filename(file.filename)
        global target
        target = os.path.join('UPLOAD_FOLDER', filename)
        file.save(target)
        return redirect(url_for('convertImage'))
    return render_template('index.html')

@app.route('/ImageConversion')
def convertImage():
    global target
    image = cv2.imread(target)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    text = pytesseract.image_to_string(image)
    os.remove(target)
    return f"Extracted text:<br><pre>{text}</pre>"

if __name__ == '__main__':
    target = ''
    app.run(debug=True)