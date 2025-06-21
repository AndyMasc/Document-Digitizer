from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_dropzone import Dropzone
import pytesseract, cv2, os
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    if request.method == 'POST':
        file = request.files.get('file')
        filename = secure_filename(file.filename)
        global target
        target = os.path.join('UPLOAD_FOLDER', filename)
        app.config['UPLOAD_FOLDER'] = target
        file.save(target)
    return render_template('index.html', text=output)

@app.route('/ViewOutputText')  # By default, dropzone consumes POST response from server to know if upload succeeded.
                               # To actually see the rendered template, there has to be another flask endpoint or URL and a way to navigate to that.
def showOutputText():
    outputText = convertImageToText()
    return render_template('index.html', text=outputText)

def convertImageToText():
    global target
    image = cv2.imread(target)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(image)
    os.remove(target)
    return text

dropzone = Dropzone(app)
if __name__ == '__main__':
    target = ''
    app.run(debug=True)