from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_dropzone import Dropzone
from fpdf import FPDF
import pytesseract
import cv2
import re
import os
import platform

if platform.system() == "Darwin":
    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
app = Flask(__name__)

os.makedirs(app.static_folder, exist_ok=True)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def uploadPage():
    if request.method == 'POST':
        file = request.files.get('file')
        filename = secure_filename(file.filename)
        global target
        target = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(target)
    return render_template('uploadPage.html')

@app.route('/ViewOutputText')  # By default, dropzone consumes POST response from server to know if upload succeeded. To actually see the rendered template, there has to be another flask endpoint or URL and a way to navigate to that.
def showOutputText():
    global target
    if not os.path.isfile(target):
        return redirect('/upload')
    outputText = convertImageToText()
    createPDF(outputText)
    return render_template('outputPage.html')

def convertImageToText():
    global target
    image = cv2.imread(target)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(image)
    try:
        os.remove(target)
    except FileNotFoundError:
        pass
    return text

def createPDF(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', os.path.join('fonts', 'DejaVuSansCondensed.ttf'), uni=True)
    pdf.set_font('DejaVu', '', 12)
    if not content:
        pdf.cell(0, 10, "No text could be extracted.")

    content = content.replace('\r\n', '\n').replace('\r', '\n')
    content = re.sub(r'\n{2,}', '<<<P>>>', content)
    content = content.replace('\n', ' ')
    content = content.replace('<<<P>>>', '\n\n')
    for paragraph in content.split('\n\n'):
        paragraph = paragraph.strip()
        if paragraph:
            pdf.multi_cell(0, 10, paragraph)

    filePath = os.path.join(app.static_folder, 'ExtractedText.pdf')
    pdf.output(filePath)

dropzone = Dropzone(app)
if __name__ == '__main__':
    target = ''
    app.run()