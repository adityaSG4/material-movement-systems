# working code

import cv2
import requests
import numpy as np
import threading
from ultralytics import YOLO

# Define object-specific variables
focal = 450
width = 4
distances = {}
buffer_size = 5

def get_ip_camera_feed(url):
    """
    Captures video from an IP camera using its URL.

    Args:
        url (str): The URL of the IP camera feed.

    Returns:
        cv2.VideoCapture: A cv2.VideoCapture object for accessing the camera feed.
    """
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        raise Exception(f"Could not open IP camera at URL: {url}")
    return cap

def detect_aruco_markers(frame):
    """
    Detects Aruco markers in the frame and returns their IDs and corners.

    Args:
        frame (np.array): The input video frame.

    Returns:
        tuple: A tuple containing two lists: ids and corners.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    aruco_params = cv2.aruco.DetectorParameters()
    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)
    return ids, corners


def get_dist(rectangle_params):
      """
      Calculates the distance of an object.

      Args:
          rectangle_params: params of bounding box.

      Returns:
        float: Distance from the camera in centimeters.
      """
      # Find the number of pixels covered
      pixels = rectangle_params[1][0]
      # Calculate distance
      dist = (width * focal * 4.5) / pixels
      return dist


def display_frames(cap, model):
    """
    Processes the camera feed, displaying each frame.

    Args:
        cap (cv2.VideoCapture): The VideoCapture object.
        model: The YOLO model object
    """
    global distances

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break
        results = model(frame)  # Pass the frame to the YOLO model

        # Extract data from YOLO results
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for i, box in enumerate(boxes):
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                label = model.names[class_id]  # Access model.names to get the class name

                if label in ['refrigerator', 'suitcase', 'tv', 'box']:  # Checking if the label is one of those
                    label = f'Box{i + 1}'
                    # Calculate distance
                    rectangle_params = (None, ((x2 - x1), None), None)
                    dist = get_dist(rectangle_params)
                    
                    # Add to buffer
                    if label not in distances:
                         distances[label] = []
                    distances[label].append(dist)

                    # Only keep the latest buffer_size values
                    distances[label] = distances[label][-buffer_size:]

                    # Calculate the smoothed distance
                    smoothed_dist = np.mean(distances[label])
                    
                    label = f'{label} {smoothed_dist:.2f}cm'  # Append the distance
                else:
                    label = 'Obstacle'  # Default label for non-box objects
                
                print(f"Object: {label} , Confidence: {confidence:.2f}, Box: ({x1}, {y1}, {x2}, {y2})")
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


        # Aruco Marker detection and processing
        ids, corners = detect_aruco_markers(frame)
        if ids is not None:
             for i, marker_id in enumerate(ids):
                corner = corners[i][0].astype(int)
                print(f"Aruco Marker ID: {marker_id}, Corners: {corner}")
                cv2.polylines(frame, [corner], True, (0, 255, 0), 2)
                cv2.putText(frame, str(marker_id), (corner[0][0], corner[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('YOLOv8 Object Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # Replace with your actual IP camera URL
    ip_camera_url = "http://172.18.39.176:8080/video"  # REPLACE WITH YOUR LOCAL IP AND PORT
    try:
        cap = get_ip_camera_feed(ip_camera_url)

        # Load the YOLOv8 model
        model = YOLO("yolov8n.pt")  # Changed to yolov8l.pt

        display_thread = threading.Thread(target=display_frames, args=(cap, model))
        display_thread.start()
    except Exception as e:
        print(f"Error: {e}")





# import cv2
# import requests
# import numpy as np
# import threading
# from ultralytics import YOLO
# import asyncio
# import websockets
# import base64
# import time
# import logging
# logging.basicConfig(level=logging.DEBUG)

# # Define object-specific variables
# focal = 450
# width = 4
# distances = {}
# buffer_size = 5


# def get_ip_camera_feed(url):
#     """Captures video from an IP camera using its URL."""
#     cap = cv2.VideoCapture(url)
#     if not cap.isOpened():
#         raise Exception(f"Could not open IP camera at URL: {url}")
#     return cap


# def detect_aruco_markers(frame):
#     """Detects Aruco markers in the frame and returns their IDs and corners."""
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
#     aruco_params = cv2.aruco.DetectorParameters()
#     corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)
#     return ids, corners


# def get_dist(rectangle_params):
#       """Calculates the distance of an object."""
#       pixels = rectangle_params[1][0]
#       dist = (width * focal * 4.5) / pixels
#       return dist

# async def process_and_send_frames(cap, model, websocket):
#     """Processes frames and sends them via WebSocket."""
#     global distances

#     try:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 logging.error("Error: Can't receive frame (stream end?). Exiting ...")
#                 break
#              # Process using YOLO
#             results = model(frame)  # Pass the frame to the YOLO model
#             # Extract data from YOLO results
#             for result in results:
#                 boxes = result.boxes.cpu().numpy()
#                 for i, box in enumerate(boxes):
#                     x1, y1, x2, y2 = map(int, box.xyxy[0])
#                     class_id = int(box.cls[0])
#                     confidence = float(box.conf[0])
#                     label = model.names[class_id]  # Access model.names to get the class name

#                     if label in ['refrigerator', 'suitcase', 'tv', 'box']:  # Checking if the label is one of those
#                         label = f'Box{i + 1}'
#                         # Calculate distance
#                         rectangle_params = (None, ((x2 - x1), None), None)
#                         dist = get_dist(rectangle_params)
                        
#                         # Add to buffer
#                         if label not in distances:
#                             distances[label] = []
#                         distances[label].append(dist)

#                         # Only keep the latest buffer_size values
#                         distances[label] = distances[label][-buffer_size:]

#                         # Calculate the smoothed distance
#                         smoothed_dist = np.mean(distances[label])
                        
#                         label = f'{label} {smoothed_dist:.2f}cm'  # Append the distance
#                     else:
#                         label = 'Obstacle'  # Default label for non-box objects
                    
#                     logging.debug(f"Object: {label} , Confidence: {confidence:.2f}, Box: ({x1}, {y1}, {x2}, {y2})")
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                     cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#             # Aruco Marker detection and processing
#             ids, corners = detect_aruco_markers(frame)
#             if ids is not None:
#                 for i, marker_id in enumerate(ids):
#                     corner = corners[i][0].astype(int)
#                     logging.debug(f"Aruco Marker ID: {marker_id}, Corners: {corner}")
#                     cv2.polylines(frame, [corner], True, (0, 255, 0), 2)
#                     cv2.putText(frame, str(marker_id), (corner[0][0], corner[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#             # Encode the frame as base64
#             _, buffer = cv2.imencode('.jpg', frame)
#             encoded_frame = base64.b64encode(buffer).decode('utf-8')
             
#             # Send the encoded frame over WebSocket
#             await websocket.send(encoded_frame)
#             await asyncio.sleep(0.03)
#     except Exception as e:
#          logging.error(f"Error in process_and_send_frames: {e}")
#     finally:
#          logging.info("Closing connection and releasing resources")
#          cap.release()

# async def websocket_handler(websocket, path):
#     """Handles WebSocket connections."""
#     logging.info("Client connected over websocket")
#     # Load the YOLOv8 model
#     model = YOLO("yolov8n.pt") # Changed to yolov8n.pt for faster processing
#     # Replace with your actual IP camera URL
#     ip_camera_url = "http://172.18.39.176:8080/video"  # REPLACE WITH YOUR LOCAL IP AND PORT
#     try:
#         cap = get_ip_camera_feed(ip_camera_url)
#         await process_and_send_frames(cap, model, websocket)
#     except Exception as e:
#         logging.error(f"Error getting IP camera feed: {e}")
#     finally:
#         logging.info("Client disconnected")


# async def main():
#     """Main function to start the WebSocket server."""
#     logging.info("Starting the websocket server")
#     async with websockets.serve(websocket_handler, "0.0.0.0", 8765):
#         await asyncio.Future()

# if __name__ == '__main__':
#     try:
#         asyncio.run(main())
#     except Exception as e:
#           logging.error(f"Error in main method: {e}")