import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from subprocess import run
from pathlib import Path
import re

class YOLOv7GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("WASTE CLASSIFICATION")

        # Set window size to fill the screen
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))

        # Set the background color of the main frame to light green
        self.master.configure(bg="#679356")  # You can adjust the hexadecimal color code

        self.image_path = ""
        self.output_image_path = ""

        # Create GUI components
        self.frame = tk.Frame(master, bg="#679356")  # Set the background color of the frame to light green
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Define a bold font for the labels and buttons
        bold_font = ("Georgia", 24, "bold")

        self.label = tk.Label(self.frame, text="Input Image:", font=bold_font, bg="#679356")
        self.label.place(x=270, y=30)

        self.output_label = tk.Label(self.frame, text="Output Image:", font=bold_font, bg="#679356")
        self.output_label.place(x=975, y=30)

        self.input_image_label = tk.Label(self.frame, bg="#679356")
        self.input_image_label.place(x=10, y = 70)

        self.output_image_label = tk.Label(self.frame, bg="#679356")
        self.output_image_label.place(x=725, y = 70)

        # Add a label for detection information
        self.info_label = tk.Label(self.frame, text="", font=bold_font, bg="#679356")
        self.info_label.place(x=600, y= 600)  # Adjust the pixel coordinates as needed

        # Buttons at the bottom
        self.run_button = tk.Button(self.master, text="Run Detection", command=self.run_detection, font=bold_font, bg="#679356")
        self.run_button.place(x= 800, y= 700 )

        self.browse_button = tk.Button(self.master, text="Browse Image", command=self.browse_image, font=bold_font, bg="#679356")
        self.browse_button.place(x=500, y = 700)

        

    def browse_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", ("*.jpg", "*.jpeg", "*.png")), ("All files", "*.*")])
        if self.image_path:
            self.display_image(self.image_path, self.input_image_label)

    def run_detection(self):
        if not self.image_path:
            return

        # Determine the output directory dynamically based on previous runs
        output_dir = "runs/detect/exp"
        i = 1
        while Path(f"{output_dir}{i}").exists():
            i += 1

        # Run YOLOv7 detection command
        command = [
            "python3",
            "detect.py",
            "--weights", "best.pt",
            "--source", self.image_path,
            "--project", "runs/detect",
            "--name", f"exp{i}",
        ]
        
        result = run(command, capture_output=True, text=True)

        # Extract detection information
        pattern = re.compile(r'model is traced!(.*?)Done', re.DOTALL)
        match = re.search(pattern, result.stdout)
        extracted_text = match.group(1).strip() if match else "Detection information not available."
        extracted_text = extracted_text[:-1]
        extracted_text = "Results: " + extracted_text
        # Display detection information
        self.info_label.config(text=extracted_text)

        # Display output image after a 5-second delay
        output_image_name = Path(self.image_path).stem + ".jpeg"
        self.output_image_path = f"{output_dir}{i}/{output_image_name}"
        print(f"Output Image Path: {self.output_image_path}")  # Add this line for debugging
        self.master.after(500, lambda: self.display_image(self.output_image_path, self.output_image_label))

    def display_image(self, path, label):
        image = Image.open(path)
        image.thumbnail((700, 700))
        tk_image = ImageTk.PhotoImage(image)

        label.config(image=tk_image)
        label.photo = tk_image


if __name__ == "__main__":
    root = tk.Tk()
    gui = YOLOv7GUI(root)
    root.mainloop()
