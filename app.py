from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_dropzone import Dropzone
import pytesseract
import cv2
import os
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    if request.method == 'POST':
        file = request.files.get('file')
        filename = secure_filename(file.filename)
        global target
        target = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(target)
    return render_template('index.html', text=output)

@app.route('/ViewOutputText')  # By default, dropzone consumes POST response from server to know if upload succeeded. To actually see the rendered template, there has to be another flask endpoint or URL and a way to navigate to that.
def showOutputText():
    if not os.path.isfile(target):
        return redirect('/')
    outputText = convertImageToText()
    createPDF(outputText)
    return render_template('ExtractedTextView.html')

def convertImageToText():
    global target
    image = cv2.imread(target)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(image)
    os.remove(target)
    return text

def createPDF(content):
    with open('ExtractedText.txt', 'w') as text:
        text.write(content)

dropzone = Dropzone(app)
if __name__ == '__main__':
    target = ''
    app.run(debug=True)