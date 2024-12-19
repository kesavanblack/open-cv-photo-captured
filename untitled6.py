import cv2
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime

# Initialize global list to store image paths
image_paths = []

# Function to capture an image and save it to a new folder
def capture_and_save_image():
    # Initialize webcam (camera index 0 by default)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Press 'c' to capture the image or 'q' to quit.")

    # Capture image from webcam
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

# Tkinter GUI setup
def setup_gui():
    global label, status_label

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

    # Label to display the image
    label = tk.Label(root)
    label.pack(padx=10, pady=10)

    # Label for status showing the current photo filename
    status_label = tk.Label(root, text="No photos to display.")
    status_label.pack(pady=10)

    # Start the Tkinter main loop
    root.mainloop()

# Main function to run the program
def main():
    setup_gui()

if __name__ == "__main__":
    main()
