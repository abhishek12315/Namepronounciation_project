import tkinter as tk

def get_input(event):
    global value
    value = entry.get()
    entry.delete(0, tk.END)  # Clear the input field after getting the value
    print("User input:", value)

# Create the main window
root = tk.Tk()
root.title("Input Example")

# Create a Label widget
label = tk.Label(root, text="Enter a value:")
label.pack()

# Create an Entry widget
entry = tk.Entry(root)
entry.pack()

# Bind the Enter key press event to the get_input function
entry.bind("<Return>", get_input)

# Start the tkinter event loop
root.mainloop()
