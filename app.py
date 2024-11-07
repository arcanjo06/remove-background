from flask import Flask, redirect, render_template, request, send_file, url_for
from rembg import remove
from PIL import Image
import os
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER']='/uploads'


# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('index'))
        file = request.files['file']

        if file.filename == '':
            return redirect(url_for('index'))

        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_path)

        with open(input_path, 'rb') as i:
            input_data = i.read()
            output_data = remove(input_data)

        output_image = Image.open(io.BytesIO(output_data))
        output_image = output_image.convert('RGBA')

        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'no_background'+file.filename)
        output_image.save(output_path,'PNG')

        return send_file(output_path, mimetype='image/png')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)