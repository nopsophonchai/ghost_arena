import tkinter as tk
import pyautogui

def get_relative_coordinates(event=None):
    # Get the absolute screen width and height
    screen_width, screen_height = pyautogui.size()
    
    # Get the current mouse position
    x, y = pyautogui.position()
    
    # Calculate the relative coordinates
    relative_x = x / screen_width
    relative_y = y / screen_height

    # Print relative coordinates
    print(f"Relative Coordinates: ({relative_x:.3f}, {relative_y:.3f})")
    
    # Display absolute coordinates for reference
    print(f"Absolute Coordinates: ({x}, {y})")

# Initialize a simple Tkinter window to capture mouse movements
root = tk.Tk()
root.geometry("1280x720")
root.bind("<Motion>", get_relative_coordinates)

root.mainloop()
