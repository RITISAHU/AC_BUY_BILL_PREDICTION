import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
#from model import build_model, predict
#from models.model import build_model, predict

import pytesseract

# Set up Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Load the model
model = build_model()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        prediction = predict(model, filepath)
        extracted_text = pytesseract.image_to_string(filepath)
        return render_template('result.html', prediction=prediction, extracted_text=extracted_text)
    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)

