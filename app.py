from flask import Flask, request, render_template, redirect, url_for, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(filename)
        file.save(filepath)
        file_url = url_for('static', filename=f'uploads/{filename}', _external=True)
        return jsonify({'file_url': file_url}), 200

    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename=os.path.join('uploads', filename)))

if __name__ == '__main__':
    app.run(debug=True)
