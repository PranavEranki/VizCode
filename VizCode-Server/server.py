import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from ocr import process_image, process_image_local
from execute import execute
from werkzeug.utils import secure_filename
from errorCorrection import error_correction

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.config['UPLOAD_FOLDER'] = 'img/'
CORS(app)

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/process')
def process():
  image_url = request.args.get('image')
  res = process_image(image_url)
  return jsonify(list(res))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'file' in request.files:
      file = request.files['file']
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      code = process_image_local('img/' + filename)
      code = error_correction(code)
      res = execute(code)
      return jsonify(code=format_code(code), res=res)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
  code = request.data
  res = execute(code)
  return jsonify(code=code, res=res)

@app.route('/test')
def test():
  return request.args.get('test')

def format_code(code):
  fcode = ''
  for line in code:
    fcode += line + '\n'
  return fcode

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int('80'))
