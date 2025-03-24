# app.py
from flask import Flask, request, render_template, send_from_directory, jsonify
import os
from reducer import reduce_pdf, estimate_compressed_size
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
REDUCED_FOLDER = 'reduced'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REDUCED_FOLDER, exist_ok=True)

from flask import send_file

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(REDUCED_FOLDER, filename, as_attachment=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    file = request.files['pdf']
    dpi = int(request.form.get('dpi', 72))
    quality = int(request.form.get('quality', 20))
    grayscale = 'grayscale' in request.form

    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_filename = 'reduced_' + filename
        output_path = os.path.join(REDUCED_FOLDER, output_filename)

        file.save(input_path)
        original_size = os.path.getsize(input_path) / 1024 / 1024  # in MB
        est_size = estimate_compressed_size(input_path, dpi, quality, grayscale)

        reduce_pdf(input_path, output_path, dpi, quality, grayscale)

        return jsonify({
            'original_size': round(original_size, 2),
            'estimated': est_size,
            'download_url': f'/download/{output_filename}',
            'filename': output_filename
        })

    return jsonify({'error': 'Invalid file format'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
