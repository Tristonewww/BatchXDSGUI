import tkinter as tk
from tkinter import ttk  # Import ttk module for themed widgets
from ttkthemes import ThemedStyle

root = tk.Tk()

# Initialize the themed style
style = ThemedStyle(root)
style.set_theme('equilux')  # Set the theme

# Use ttk.Button to apply the themed style
ttk.Button(root, text="Test Button").pack()
# Customizing the button appearance
style.configure('TButton', font=('Helvetica', 1, 'bold'), foreground='blue')


root.mainloop()
