import cv2
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime

# Initialize global list to store image paths
image_paths = []
label = None  # Declare label for image display globally
status_label = None  # Declare status_label for status globally
canvas = None  # Declare canvas for webcam feed globally

# Function to capture an image and save it to a new folder
def capture_and_save_image():
    # Initialize webcam (camera index 0 by default)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Capture one frame from the webcam feed
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        return

    # Create a new folder with a timestamp for saving the photo
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_path = f"Captured_Photos/{timestamp}"

    # Create folder if it does not exist
    os.makedirs(folder_path, exist_ok=True)

    # Save the captured photo
    photo_path = os.path.join(folder_path, f"photo_{timestamp}.jpg")
    cv2.imwrite(photo_path, frame)
    print(f"Photo saved as {photo_path}")

    # Add the new photo to the list of saved images
    image_paths.append(photo_path)

    # Release webcam and close OpenCV window
    cap.release()

    # Update image in the Tkinter canvas
    show_image()

# Function to show the most recent photo in the Tkinter window
def show_image():
    if not image_paths:
        messagebox.showerror("Error", "No photos captured yet!")
        return

    # Load the most recent image
    img_path = image_paths[-1]
    img = Image.open(img_path)
    img = img.resize((400, 400))  # Resize to fit in window
    img_tk = ImageTk.PhotoImage(img)

    # Update the label with the new image
    label.config(image=img_tk)
    label.image = img_tk  # Keep reference to avoid garbage collection

    # Update the status label with the filename of the most recent photo
    status_label.config(text=f"Displaying: {os.path.basename(img_path)}")

# Function to show the previous photo in the Tkinter window
def show_previous_image():
    if len(image_paths) < 2:
        messagebox.showinfo("Info", "No previous images to show!")
        return

    # Get the previous photo path
    prev_img_path = image_paths[-2]
    img = Image.open(prev_img_path)
    img = img.resize((400, 400))  # Resize to fit in window
    img_tk = ImageTk.PhotoImage(img)

    # Update the label with the new image
    label.config(image=img_tk)
    label.image = img_tk  # Keep reference to avoid garbage collection

    # Update the status label with the filename of the previous photo
    status_label.config(text=f"Displaying: {os.path.basename(prev_img_path)}")

# Function to display the webcam feed in a Tkinter canvas
def display_webcam_feed():
    # Open the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    def update_frame():
        ret, frame = cap.read()
        if ret:
            # Convert the image to RGB (OpenCV uses BGR by default)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img = img.resize((400, 400))  # Resize to fit in window
            img_tk = ImageTk.PhotoImage(img)

            # Update the canvas with the new frame
            canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            canvas.image = img_tk  # Keep reference to avoid garbage collection

        # Continue updating the frame
        canvas.after(10, update_frame)

    # Start updating frames
    update_frame()

# Tkinter GUI setup
def setup_gui():
    global label, status_label, canvas  # Declare them as global variables

    # Initialize the Tkinter window
    root = tk.Tk()
    root.title("Photo Capture and Viewer")

    # Create buttons for capture and navigation
    capture_button = tk.Button(root, text="Capture Photo", command=capture_and_save_image)
    capture_button.pack(pady=10)

    # Button to show the most recent photo
    show_button = tk.Button(root, text="Show Recent Photo", command=show_image)
    show_button.pack(pady=10)

    # Button to show the previous photo
    prev_button = tk.Button(root, text="Show Previous Photo", command=show_previous_image)
    prev_button.pack(pady=10)

    # Canvas to display the webcam feed
    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack()

    # Label to display the captured image
    label = tk.Label(root)
    label.pack(padx=10, pady=10)

    # Status label to show which photo is being displayed
    status_label = tk.Label(root, text="No photos to display.")
    status_label.pack(pady=10)

    # Start displaying webcam feed
    display_webcam_feed()

    # Start the Tkinter main loop
    root.mainloop()

# Main function to run the program
def main():
    setup_gui()

if __name__ == "__main__":
    main()
