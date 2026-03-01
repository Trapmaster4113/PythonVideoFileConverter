import tkinter as tk
from tkinter import filedialog
from moviepy import VideoFileClip
import os
#Function used to change label text for Error Message on the bottom right and the Input/Output labels in the top right
#Takes in 2 parameters: 
#name: used to see which label to change
#text: this is the new text
def changeText(name, text):

    if name == "input":
        inputLabel.config(text=text)
    elif name == "output":
        outputLabel.config(text=text)
    elif name == "error":
        errorLabel.config(text=text)
#input(): function used to get location of file/folder to be changed
def input():
    #Makes sure the function uses global variables instead of local variables with the same name
    global inputFile
    global inputFolder
    #If User selects option 1, will ask for an input file rather than an input folder
    if w.get() == 1:
        #Creates a variable storing the file type and ensures correct file type
        inputFile = filedialog.askopenfilename(
        title = "Select a file",
        filetypes=[("Video Files", "*.mp4 *.mkv *.mov *.ogv *.webm *.avi")]
        )
        #Changes the input label to display the file name
        changeText("input", inputFile.title())
        #Ensures that the inputFolder is null just in case don't know if necessary
        inputFolder = None
    #If User selects option 2, will ask for an input folder rather than an input file
    elif w.get() == 2:
        #Creates a variable storing the folder location
        inputFolder = filedialog.askdirectory(title="Select a folder")
        #Changes the input label to display the folder name
        changeText("input", inputFolder.title())
        #Ensures that the inputFile is null just in case don't know if necessary
        inputFile = None
#enterOutputFolder(): function used to get location of folder to place the converted video
def enterOutputFolder():
    #Makes sure the function uses global variables instead of local variables with the same name
    global outputFolder
    global outputLabel
    #Creates a variable storing the folder location
    outputFolder = filedialog.askdirectory(title="Select a folder")
    #Changes the output label to display the folder name
    changeText("output", outputFolder.title())
#fileType(): function used to set variables used later in the conversion process
def fileType():
    #Makes sure the function uses global variables instead of local variables with the same name
    global code
    global file
    #Over complicated if statements
    if v.get() == 4:
        code = "libtheora"
        file = ".ogv"
    elif v.get() == 5:
        code = "libvpx"
        file = ".webm"
    elif v.get() == 6:
        code = ""
        file = ".avi"
    #For some reason these 3 file types use the same code
    else:
        code = "libx264"
        if v.get() == 1:
            file = ".mp4"
        elif v.get() == 2:
            file = ".mkv"
        elif v.get() == 3:
            file = ".mov"
#convert(): function used to covert the file or the entire folder of videos into the desired type while skipping files that were already converted
def convert():
    #Makes sure the function uses global variables instead of local variables with the same name
    global outputFolder
    global inputFile
    global inputFolder
    global clipDuration
    #If no outputFolder selected, throw error and stops function
    if outputFolder is None:
        changeText("error","No Output Selected")
        return
    #Checks if user wants to change a single file
    if not inputFile is None:
        #Removes the absolute location and gets only the file name
        name = inputFile.split("/")[-1]
        #Removes the file type from the end
        name = name[:name.find(".")]
        #Creates a VideoFileClip variable with the video file that can be manipulated
        clip = VideoFileClip(inputFile)
        #Shortens the video by a small percentage to remove any dead frames (For some reason, all clips have them at the end)
        clip = clip.subclipped(0, clip.duration * clipDuration)
        #Gets file path of output folder to check if going to make a duplicate
        contents2 = os.listdir(outputFolder)
        #Checks if duplicate exits
        if name+file in contents2:
            #Throws error due to duplicate file
            changeText("error", "Duplicate File Located")
            #Reset input text and file
            changeText("input", "")
            inputFile = None
            #Exits function
            return
        #Creates the new video YAY!
        clip.write_videofile(outputFolder+"/"+name+file, codec=code)
        #Reset input text and file
        inputFile = None
        changeText("input", "")
    #Checks if user wants to change all files in a folder
    elif not inputFolder is None:
        #Gets folder paths for both input and output folders
        contents = os.listdir(inputFolder)
        contents2 = os.listdir(outputFolder)
        #Iterates through all files in the inputfolder
        for i in contents:
            #Removes file type from all file names
            name = i[:i.find(".")]
            #Checks if duplicate exits in outputFolder
            if name+file in contents2:
                continue

            #Creates a VideoFileClip variable with the video file that can be manipulated
            clip = VideoFileClip(inputFile)
            #Shortens the video by a small percentage to remove any dead frames (For some reason, all clips have them at the end)
            clip = clip.subclipped(0, clip.duration * clipDuration)
            #Creates the new video YAY!
            clip.write_videofile(outputFolder+"/"+name+file, codec=code)
        #Reset input text and file
        inputFolder = None
        changeText("input", "")
    else:
        #If no input selected, throws error and stops function
        changeText("error","No Input Selected")
        return
    #Text to show that file was created
    changeText("error","Job Done")
    return
#Used for creating desktop application with Tkinter
root = tk.Tk()
#Creating global variables so functions can share (don't know if necessary)
inputFile = None
inputFolder = None
outputFolder = None
#Technically an arbitray number, but I think it works
clipDuration = 0.983
code = None
file = None
#creating the text labels for input,output, and error
#.grid is used to position them on the application
inputLabel = tk.Label(root, text="")
inputLabel.grid(row=0, column=4, sticky=tk.W)
outputLabel = tk.Label(root, text="")
outputLabel.grid(row=1, column=4, sticky=tk.W)
errorLabel = tk.Label(root, text="")
errorLabel.grid(row=5,column=2,columnspan=3, sticky=tk.W)
inputLabel2 = tk.Label(root, text="Input: ").grid(row=0,column=3, sticky=tk.W)
outputLabel2 = tk.Label(root, text="Output: ").grid(row=1,column=3, sticky=tk.W)
#Create variables to accept user input
w = tk.IntVar()
#Radiobutton is single select option
tk.Radiobutton(root, text="InputFile", variable=w, value=1, command=input).grid(row=0, column=1, sticky=tk.W)
tk.Radiobutton(root, text="InputFolder", variable=w, value=2, command=input).grid(row=1, column=1, sticky=tk.W)
v = tk.IntVar()
tk.Radiobutton(root, text="mp4", variable=v, command=fileType, value=1).grid(row=0, column=0, sticky=tk.W)
tk.Radiobutton(root, text="mkv", variable=v, command=fileType, value=2).grid(row=1, column=0, sticky=tk.W)
tk.Radiobutton(root, text="mov", variable=v, command=fileType, value=3).grid(row=2, column=0, sticky=tk.W)
tk.Radiobutton(root, text="ogv", variable=v, command=fileType, value=4).grid(row=3, column=0, sticky=tk.W)
tk.Radiobutton(root, text="webm", variable=v, command=fileType, value=5).grid(row=4, column=0, sticky=tk.W)
tk.Radiobutton(root, text="avi", variable=v, command=fileType, value=6).grid(row=5, column=0, sticky=tk.W)
#Button used to ask for output folder location
button = tk.Button(root, text="Enter Output Folder",command=enterOutputFolder).grid(row=3,column=3)
#button to convert
button2 = tk.Button(root, text="Convert", width=25, command=convert).grid(row=3,column=5)
#Loops the program to be ready to be used whenever user activates
root.mainloop()