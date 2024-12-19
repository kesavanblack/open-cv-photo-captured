import cv2
import os
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk

# Function to capture image and save it to a new folder
def capture_and_save_image():
    # Initialize the webcam (camera index 0 by default)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Press 'c' to capture the image or 'q' to quit.")
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame")
            break

        # Show the captured frame in a window
        cv2.imshow("Capture Image", frame)

        # Wait for user input
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):  # Press 'c' to capture the photo
            # Create a new folder with a timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            folder_path = f"Captured_Photos/{timestamp}"

            # Create the folder if it does not exist
            os.makedirs(folder_path, exist_ok=True)

            # Save the captured photo in the new folder
            photo_path = os.path.join(folder_path, f"photo_{timestamp}.jpg")
            cv2.imwrite(photo_path, frame)
            print(f"Photo saved as {photo_path}")
            break

        elif key == ord('q'):  # Press 'q' to quit without saving
            print("Quitting without saving.")
            break

    # Release the webcam and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

    return photo_path

# Function to display the image and ask for the person's name
def display_and_get_name(photo_path):
    # Read and display the saved photo
    image = cv2.imread(photo_path)
    cv2.imshow("Saved Photo", image)
    cv2.waitKey(0)  # Wait for any key press

    # Ask for the person's name
    name = input("Enter the person's name: ")

    # Display the name on the image
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, f"Name: {name}", (10, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    # Save the image with the name displayed
    name_image_path = photo_path.replace(".jpg", f"_{name}.jpg")
    cv2.imwrite(name_image_path, image)
    print(f"Image with name saved as {name_image_path}")

    # Show the image with the name in Tkinter window
    show_image_in_tkinter(name_image_path)

def show_image_in_tkinter(image_path):
    # Initialize the Tkinter window
    root = tk.Tk()
    root.title("Image with Name")

    # Open the image using Pillow
    img = Image.open(image_path)
    img = img.resize((400, 400))  # Resize image to fit in window
    img_tk = ImageTk.PhotoImage(img)

    # Create a Label to display the image
    label = tk.Label(root, image=img_tk)
    label.image = img_tk  # Keep a reference to avoid garbage collection
    label.pack()

    # Start the Tkinter GUI
    root.mainloop()

def main():
    # Capture and save the image
    photo_path = capture_and_save_image()

    if photo_path:
        # Display the photo and get the person's name
        display_and_get_name(photo_path)

if __name__ == "__main__":
    main()
