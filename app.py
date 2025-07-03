from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_dropzone import Dropzone
from fpdf import FPDF
import os
from google.cloud import vision

app = Flask(__name__)

creds_json = os.environ["CloudVisionAPI"]
tmp_path = "/tmp/google_creds.json"
with open(tmp_path, "w") as f:
    f.write(creds_json)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = tmp_path
client = vision.ImageAnnotatorClient()

os.makedirs(app.static_folder, exist_ok=True)

if not os.path.exists(os.path.join(os.getcwd(), 'uploads')):
    os.makedirs(os.path.join(os.getcwd(), 'uploads'))

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def uploadPage():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        global imageFilePath
        imageFilePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(imageFilePath)
    return render_template('uploadPage.html')

def convertImageToText():
    global imageFilePath
    with open(imageFilePath, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)  # Use document_text_detection for handwriting
    texts = response.text_annotations
    result = ''
    for text in texts:
        result = result + ("{}".format(text.description))
    result = texts[0].description
    return result

@app.route('/ViewOutputText')  # By default, dropzone consumes POST response from server to know if upload succeeded. To actually see the rendered template, there has to be another flask endpoint or URL and a way to navigate to that.
def showOutputText():
    outputText = convertImageToText()
    createPDF(outputText)
    os.remove(imageFilePath)
    return render_template('outputPage.html')

def createPDF(extractedText):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', os.path.join('fonts', 'DejaVuSansCondensed.ttf'), uni=True)
    pdf.set_font('DejaVu', '', 12)
    if not extractedText:
        pdf.cell(0, 10, "No text could be extracted.")
    else:
        pdf.multi_cell(0, 10, extractedText)
    pdfFilePath = os.path.join(app.static_folder, 'ExtractedText.pdf')
    pdf.output(pdfFilePath)

dropzone = Dropzone(app)
if __name__ == '__main__':
    imageFilePath = ''
    app.run()