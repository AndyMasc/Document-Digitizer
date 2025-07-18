from flask import Flask, render_template, request, redirect, url_for
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

# Create static folder for CSS and images if not already existing.
os.makedirs(app.static_folder, exist_ok=True)

absPath = os.path.abspath(os.path.dirname(__file__))
# Create uploads folder for uploaded file if not already existing
if not os.path.exists(os.path.join(absPath, 'uploads')):
    os.makedirs(os.path.join(os.getcwd(), 'uploads'))

app.config.update(
    UPLOADED_PATH = os.path.join(absPath, 'uploads'),
    DROPZONE_MAX_FILES = 1,
    DROPZONE_MAX_FILE_SIZE = 20,
    DROPZONE_ALLOWED_FILE_CUSTOM = True,
    DROPZONE_ALLOWED_FILE_TYPE = '.jpg, .jpeg, .png',
    DROPZONE_DEFAULT_MESSAGE = 'Drop your <b> image file </b> onto the scanner or click here to upload. You will automatically be redirected',
    DROPZONE_REDIRECT_VIEW = 'showOutputText',
)

dropzone = Dropzone(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def uploadPage():
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        global imageFilePath
        imageFilePath = os.path.join(app.config['UPLOADED_PATH'], filename)
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
    if not texts:
        return "No text found in this image. Please try another image with text."
    return texts[0].description

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

if __name__ == '__main__':
    imageFilePath = ''
    app.run()