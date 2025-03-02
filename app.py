import os
from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from PIL import Image
from collections import Counter
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def get_dominant_colors(image_path, num_colors=5):
    # Read image with OpenCV
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Reshape the image to be a list of pixels
    pixels = image.reshape(-1, 3)
    
    # Reduce colors by clustering
    pixels = np.float32(pixels)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, palette = cv2.kmeans(pixels, num_colors, None, criteria, 10, flags)
    
    # Convert to integers
    palette = np.uint8(palette)
    
    # Calculate percentage of each color
    total_pixels = len(labels)
    color_counts = Counter(labels.flatten())
    
    # Sort colors by frequency
    color_info = []
    for i in range(num_colors):
        count = color_counts[i]
        percentage = (count / total_pixels) * 100
        color = palette[i].tolist()
        hex_color = rgb_to_hex(color)
        color_info.append({
            'hex': hex_color,
            'rgb': color,
            'percentage': round(percentage, 2)
        })
    
    return sorted(color_info, key=lambda x: x['percentage'], reverse=True)

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
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            colors = get_dominant_colors(filepath)
            # Clean up the uploaded file
            os.remove(filepath)
            return jsonify({'colors': colors})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True) 