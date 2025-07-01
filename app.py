from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_dropzone import Dropzone
from fpdf import FPDF
import os
from google.cloud import vision

app = Flask(__name__)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.environ.get('CloudVisionAPI')

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
    client = vision.ImageAnnotatorClient()

    with open(target, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)  # Use document_text_detection for handwriting
    texts = response.text_annotations
    result = ''
    for text in texts:
        result = result + ("{}".format(text.description))
    result = texts[0].description
    os.remove(target)
    return result

def createPDF(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', os.path.join('fonts', 'DejaVuSansCondensed.ttf'), uni=True)
    pdf.set_font('DejaVu', '', 12)
    if not content:
        pdf.cell(0, 10, "No text could be extracted.")
    else:
        pdf.multi_cell(0, 10, content)

    filePath = os.path.join(app.static_folder, 'ExtractedText.pdf')
    pdf.output(filePath)

dropzone = Dropzone(app)
if __name__ == '__main__':
    target = ''
    app.run()