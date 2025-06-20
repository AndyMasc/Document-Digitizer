from bottle import route, run, template, view, static_file
from TextConverter import *

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  # for Apple Silicon

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')

@route('/')
def index():
    return template('Homepage')

run(host='localhost', port=8080, debug=True, reloader=True)