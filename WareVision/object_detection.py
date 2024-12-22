import glob
import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json
import mimetypes
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load environment variables
load_dotenv()

def analyze_image_with_gemini(image_path):
    """
    Analyzes an image using the Gemini AI API and draws bounding boxes.

    Args:
        image_path (str): The path to the image file.

    Returns:
        tuple: A tuple containing the modified image and the AI-generated text response.
               Returns (None, None) if the request fails.
    """
    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
        return None, None

    try:
        # 1. File Upload
        upload_url = f'https://generativelanguage.googleapis.com/upload/v1beta/files?key={api_key}'
        mime_type = mimetypes.guess_type(image_path)[0] or 'application/octet-stream'

        with open(image_path, 'rb') as image_file:
            files = {'file': (os.path.basename(image_path), image_file, mime_type)}
            upload_response = requests.post(upload_url, files=files)
            upload_response.raise_for_status()  # Raise exception for non-200 status

        file_uri = upload_response.json().get('file', {}).get('uri')
        if not file_uri:
            print("Error: File upload failed, no file URI returned.")
            return None, None

        # 2. Content Generation Request
        content_generation_url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}'
        headers = {'Content-Type': 'application/json'}
        prompt = ("count the boxes and tell the approx degree of angle the front face of each box visible is inclining with respect to the camera screen of image. provide the output in this format only"
        "Total Boxes: <Number>\n"
        "The top box (Box 1): approx <angle description> to the camera plane.\n"
        "The two boxes to the left and right of the top box (Box 2 & Box 3): approx <angle description> away from the camera.\n"
        "The two smaller boxes in front (Box 4 & Box 5): approx <angle description>.\n"
        "The bottom-right box (Box 6): approx <angle description>\n"
        "The bottom-left box (Box 7): approx <angle description>.\n I am aware of approximation so dont add note or any extra output instead of given example.")

        request_body = json.dumps({
            "contents": [
                {"role": "user", "parts": [{"fileData": {"fileUri": file_uri, "mimeType": mime_type}}]},
                {"role": "user", "parts": [{"text": prompt}]}
            ],
            "generationConfig": {
                "temperature": 1,
                "topK": 64,
                "topP": 0.95,
                "maxOutputTokens": 100000,
                "responseMimeType": "text/plain"
            },
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        })

        content_response = requests.post(content_generation_url, headers=headers, data=request_body)
        content_response.raise_for_status()  # Raise exception for non-200 status

        response_body = content_response.json()
        text_response = response_body.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text")

        if not text_response:
            print("Error: Invalid response from Gemini API.")
            return None, None

        
        return None, text_response # Return None for image as you don't want to display it

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None, None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None


@app.route('/analyze', methods=['POST'])
def analyze_endpoint():
    if 'file' not in request.files:
        print("No file part in request")
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    if file.filename == '':
        print("No selected file")
        return jsonify({'error': 'No selected file'}), 400
    
    # Create uploads directory if it doesn't exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    # Save file temporarily
    temp_path = os.path.join('uploads', 'temp_image.jpg')
    try:
        file.save(temp_path)
        print(f"File saved to {temp_path}")
        
        # Process the image
        _, text_response = analyze_image_with_gemini(temp_path)
        
        if text_response:
            print(f"Analysis response: {text_response}")
            return jsonify({'text_response': text_response})
        else:
            print("Failed to get response from Gemini")
            return jsonify({'error': 'Failed to get response from Gemini'}), 500
            
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return jsonify({'error': str(e)}), 500
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print(f"Cleaned up {temp_path}")

if __name__ == '__main__':
    app.run(debug=True, port=5000)