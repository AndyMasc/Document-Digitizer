from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_dropzone import Dropzone
from fpdf import FPDF
import pytesseract
import cv2
import re
import os

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True

@app.route('/')
def Homepage():
    return render_template('HomePage.html')

@app.route('/upload', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        filename = secure_filename(file.filename)
        global target
        target = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(target)
    return render_template('index.html')

@app.route('/ViewOutputText')  # By default, dropzone consumes POST response from server to know if upload succeeded. To actually see the rendered template, there has to be another flask endpoint or URL and a way to navigate to that.
def showOutputText():
    if not os.path.isfile(target):
        return redirect('/upload')
    outputText = convertImageToText()
    createPDF(outputText)
    return render_template('ExtractedTextView.html')

def convertImageToText():
    global target
    image = cv2.imread(target)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(image)
    try:
        os.remove(target)
    except FileNotFoundError:
        pass
    print(repr(text))
    return text

def createPDF(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', '/Users/andymascarenhas/Library/Fonts/DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)
    if not content:
        pdf.cell(0, 10, "No text could be extracted.")

    content = content.replace('\r\n', '\n').replace('\r', '\n') # Normalize all line endings to just \n
    content = re.sub(r'\n{2,}', '<<<P>>>', content)  # Mark real paragraphs with temporary marker <<<P>>>
    content = content.replace('\n', ' ')  # Remove all single newlines
    content = content.replace('<<<P>>>', '\n\n') # Restore paragraph breaks
    for paragraph in content.split('\n\n'): # Pass the cleanly formatted paragraphs to be added to the PDF.
        paragraph = paragraph.strip()
        if paragraph:
            pdf.multi_cell(0, 10, paragraph)

    filePath = os.path.join(app.static_folder, 'ExtractedText.pdf')
    pdf.output(filePath)

dropzone = Dropzone(app)
if __name__ == '__main__':
    target = ''
    app.run(host='0.0.0.0', debug=True)