from tkinter import *
import os
from PIL import Image, ImageGrab
import pytesseract
from tkinter import filedialog



class txtextapp(Frame):
    def __init__(self, master=None):
        self.tes_path = r"C:/Program Files/Tesseract-OCR/tesseract"
        Frame.__init__(self,master)
        self.grid()
        self.widgets()

    def widgets(self):
        self.display_label = Label(self, text="Choose a method to insert image")
        self.display_label.grid(row=0, column=0)

        self.calculation_button = Button(self, text="Clipboard!", command=self.clipbrd)
        self.calculation_button.grid(row=3,column=2)

        self.calculation_button = Button(self, text="Browse local", command=self.local)
        self.calculation_button.grid(row=4,column=2)

        self.quit_button = Button(self, text="Quit", command=self.master.destroy)
        self.quit_button.grid(row=7,column=0)	

    def clipbrd(self):

        temp_path = "D:\python\sample.png" # Whatever temp path you want here
        im = ImageGrab.grabclipboard() # Get image from clipboard

        if im is None:
            # displays a static content 
            self.display_label = Label(self, text="Please take a screenshot to proceed")
            self.display_label.grid(row=5, column=0)

        else:
            #saves the sceernshot as an image in a temporary path
            im.save(temp_path,format="PNG") 

            pytesseract.pytesseract.tesseract_cmd = self.tes_path

            # opens the saved image from the temporary path
            imgshot = Image.open(temp_path)

            # extracts the text in screenshot using image_to_string function in pytessearact
            self.txtnshot = pytesseract.image_to_string(imgshot)

            # adds the extracted text to the displayed screen
            self.display_label = Label(self, text=self.txtnshot)
            self.display_label.grid(row=5, column=0)

            self.calculation_button = Button(self, text="Write in txt file", command=self.write_to_txt)
            self.calculation_button.grid(row=6,column=0)

            os.remove(temp_path)

    def browse_file(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Images", "*.png*"),("all files", "*.*")))
        return filename

    def local(self):
        saved_img = self.browse_file()
        # print(saved_img.type())
        # Image.open(saved_img)
        pytesseract.pytesseract.tesseract_cmd = self.tes_path

        # opens the saved image from the temporary path
        imgshot = Image.open(saved_img)

        # extracts the text in screenshot using image_to_string function in pytessearact
        self.txtnshot = pytesseract.image_to_string(imgshot)

        # adds the extracted text to the displayed screen
        self.display_label = Label(self, text=self.txtnshot)
        self.display_label.grid(row=5, column=0)

        self.calculation_button = Button(self, text="Write in txt file", command=self.write_to_txt)
        self.calculation_button.grid(row=6,column=0)

    def write_to_txt(self):
        # rewritting the newly extracted texts for future purposes
        temp_str = open("D:\python\sshotapp\extracted_text.txt","w+")

        temp_str.write(self.txtnshot)
        temp_str.close()

if __name__ == "__main__":
    app = txtextapp()
    app.mainloop()

