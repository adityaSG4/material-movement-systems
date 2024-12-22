import cv2
import numpy as np
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import base64

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def solve_maze(image_path, max_size=3000):
    """Solves a maze image by finding start/end on edges."""
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None, "Error: Could not load image."

        _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

        def find_start_end(image):
            """Finds start and end points on the image edges."""
            start = None
            end = None
            h, w = image.shape
            border = 5  # How many pixels from border to check

            for x in range(border, w - border):
                if image[border, x] == 255:
                    if start is None:
                        start = (x, border)
                    else:
                        end = (x, border)
                if image[h - 1 - border, x] == 255:
                    if start is None:
                        start = (x, h - 1 - border)
                    else:
                        end = (x, h - 1 - border)

            for y in range(border, h - border):
                if image[y, border] == 255:
                    if start is None:
                        start = (border, y)
                    else:
                        end = (border, y)
                if image[y, w - 1 - border] == 255:
                    if start is None:
                        start = (w - 1 - border, y)
                    else:
                        end = (w - 1 - border, y)

            return start, end
        
        start, end = find_start_end(thresh)

        if start is None or end is None:
            return None, "Error: Could not find start or end points on the edges."

        # Pathfinding (flood fill)
        path = np.zeros_like(thresh, dtype=np.uint8)
        queue = [start]
        path[start[1], start[0]] = 1

        while queue:
            x, y = queue.pop(0)

            if (x, y) == end:
                break

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < thresh.shape[1] and 0 <= ny < thresh.shape[0] and thresh[ny, nx] == 255 and path[ny, nx] == 0:
                    queue.append((nx, ny))
                    path[ny, nx] = 1

        # Draw path
        color_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        path_coords = np.argwhere(path == 1)
        for y, x in path_coords:
            cv2.circle(color_img, (x, y), 1, (0, 255, 0), 4)

        cv2.circle(color_img, start, 3, (0, 255, 0), -1)  # Green start
        cv2.circle(color_img, end, 3, (255, 0, 0), -1)    # Blue end
            
        return color_img, "Maze solved successfully."

    except Exception as e:
        return None, f"An error occurred: {e}"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@app.route('/solve_maze', methods=['POST'])
def solve_maze_endpoint():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        solved_image, message = solve_maze(filepath)
        if solved_image is None:
            return jsonify({'error': message}), 400
        
        # Convert the solved image to base64
        _, buffer = cv2.imencode('.png', solved_image)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Clean up the uploaded file
        os.remove(filepath)
        
        return jsonify({
            'image': image_base64,
            'message': message
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='127.0.0.1')