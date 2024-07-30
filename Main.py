import cv2
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import os
from ultralytics import YOLO
import threading
from plateReader import readLiscencePlate

# Load your YOLO model and set up necessary configurations
model_path = os.path.join('.', 'train', 'weights', 'last.pt')
model = YOLO(model_path)

# Initialize Tkinter
root = tk.Tk()
root.title("License Plate Detection")

# Set the path to the icon file (replace 'icon.ico' with your icon file)
icon_path = '../camera.ico'
root.iconbitmap(icon_path)

# Set the desired width and height for the canvas (smaller dimensions)
canvas_width = 800
canvas_height = 400

# Create a canvas to display the video feed
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Entry widget for user to input the video link
link_entry = tk.Entry(root)
link_entry.pack(pady=10, ipadx=10, ipady=5)

# Frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack()

# Function to process video feed
def process_video_feed():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (canvas_width, canvas_height))  # Resize the frame to fit the smaller canvas
        results = model(frame)[0]  # Perform object detection on the frame
        for detection in results:
            bbox = detection.boxes.xyxy[0]  # Extract the bounding box coordinates
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw rectangle around detected object
        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.img = img_tk
        canvas.after(1, process_video_feed)

# Function to start video capture based on user input
def start_video_capture():
    global cap
    link = link_entry.get()
    cap = cv2.VideoCapture("http://" + link + ":8080/video")
    if not cap.isOpened():
        error_label.config(text="Error: Invalid link or unable to open video stream.")
    else:
        process_video_feed()
        error_label.config(text="")  # Clear any previous error message
        link_entry.config(state="disabled")  # Disable the text field once the live feed starts
        check_button.config(state="normal")

# Function to stop the live video feed
def stop_video_capture():
    if cap is not None:
        cap.release()
        link_entry.config(state="normal")  # Enable the text field
        check_button.config(state="disabled")
        error_label.config(text="Live video feed stopped.")  # Display message
        canvas.delete("all")  # Clear the canvas

def capture_screen():
    if cap is not None:
        ret, frame = cap.read()
        if ret:
            results = model(frame)[0]  # Perform object detection on the frame
            for detection in results:
                bbox = detection.boxes.xyxy[0]  # Extract the bounding box coordinates
                x1, y1, x2, y2 = map(int, bbox)
                screenshot = frame[y1:y2, x1:x2]  # Crop the screenshot around the bounding box
                cv2.imwrite("Captures/screen.jpg", screenshot)  # Save the screenshot
                if readLiscencePlate():
                    result_label.config(text="Allowed to go in", fg="green")
                else:
                    result_label.config(text="Not allowed to go in", fg="red")

# Label to display the result message
result_label = tk.Label(root, font=("Arial", 24, "bold"))
result_label.pack()

# Buttons to start and stop the live video feed
start_button = tk.Button(button_frame, text="Start Live Video", command=start_video_capture, bg='#861896', padx=20, pady=10, border=0)
start_button.pack(side=tk.LEFT, padx=5)
stop_button = tk.Button(button_frame, text="Stop Live Video", command=stop_video_capture, bg='#861896', padx=20, pady=10, border=0)
stop_button.pack(side=tk.LEFT, padx=5)
check_button = tk.Button(button_frame, text="Check", command=capture_screen, bg='#861896', padx=20, pady=10, border=0)
check_button.pack(side=tk.LEFT, padx=5)
check_button.config(state="disabled")

# Label to display error messages
error_label = tk.Label(root, fg="red", font=("Arial", 24, "bold"))
error_label.pack()

# Run the Tkinter main loop
root.mainloop()