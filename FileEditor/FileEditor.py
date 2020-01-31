from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
# 'Tkinter' had to be imported so we can use its modules to create
# the graphical window for the file editor. We import two other modules
# to give the program the function to 'open files' and 'save file as'.

class FileEditor:
    def __init__(self):
        window = Tk()
        window.title("Simple File Editor")

        # Create a menu bar
        menubar = Menu(window)
        window.config(menu = menubar) # Display the menu bar

        # Create a pull-down menu and add it to the menu bar
        operationMenu = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "File", menu = operationMenu)
        operationMenu.add_command(label = "Open", command = self.openFile)
        operationMenu.add_command(label = "Save", command = self.saveFile)

        # Add tool bar frame
        frame0 = Frame(window) # Create and add a frame to window
        frame0.grid(row = 1, column = 1, sticky = W)

        # Create Images
        openImage = PhotoImage(file = "image/open.gif")
        saveImage = PhotoImage(file = "image/save.gif")

        Button(frame0, image = openImage, command =
               self.openFile).grid(row = 1, column = 1, sticky = W)
        Button(frame0, image = saveImage,
               command = self.saveFile).grid(row = 1, column = 2)

        frame1 = Frame(window) # Hold editor pane
        frame1.grid(row = 2, column = 1)

        scrollbar = Scrollbar(frame1)
        scrollbar.pack(side = RIGHT, fill = Y)
        self.text = Text(frame1, width = 50, height = 20,
                         wrap = WORD, yscrollcommand = scrollbar.set)
        self.text.pack()
        scrollbar.config(command = self.text.yview)
        window.mainloop() # Create an event loop

    def openFile(self):
        filenameforReading = askopenfilename()
        infile = open(filenameforReading, "r")
        self.text.insert(END, infile.read()) # Read all from the file
        infile.close() # Close the input file

    def saveFile(self):
        filenameforWriting = asksaveasfilename()
        outfile = open(filenameforWriting, "w")
        # Write to the file
        outfile.write(self.text.get(1.0, END))
        outfile.close() # Close the output file

FileEditor()
