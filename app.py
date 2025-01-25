from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
from process_image import process_image


app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    edge_detection = request.form.get('edgeDetection')
    gaussian_blur = request.form.get('gaussianBlur') == 'true'
    dilate_erode = request.form.get('dilateErode') == 'true' 
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(filepath)

        config_params = {}
        config_params["gaussianBlur"] = gaussian_blur
        config_params["edgeDetection"] = edge_detection
        config_params["dilateAndErrode"] = dilate_erode

        filename1, filename2 = process_image(filepath, config_params)

        file_url1 = url_for('static', filename=f'processed/{filename1}', _external=True)
        file_url2 = url_for('static', filename=f'processed/{filename2}', _external=True)

        return jsonify({'file_url1': file_url1, 'file_url2': file_url2}), 200

    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename=os.path.join('uploads', filename)))

@app.route('/processed/<filename>')
def processed_file_file(filename):
    return redirect(url_for('static', filename=os.path.join('processed', filename)))

if __name__ == '__main__':
    app.run(debug=True)
