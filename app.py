# app.py

from flask import Flask, request, render_template, send_from_directory
import os
from reducer import reduce_pdf
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
REDUCED_FOLDER = 'reduced'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REDUCED_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['pdf']
        quality_option = request.form['quality']

        quality_map = {
            'best_compress': 5,
            'default': 10,
            'best_quality': 30
        }
        quality = quality_map.get(quality_option, 10)

        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            output_filename = 'reduced_' + filename
            output_path = os.path.join(REDUCED_FOLDER, output_filename)

            file.save(input_path)
            reduce_pdf(input_path, output_path, quality=quality)

            return send_from_directory(REDUCED_FOLDER, output_filename, as_attachment=True)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
