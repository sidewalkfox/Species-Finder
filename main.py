from parselmouth.praat import run_file
import numpy as np
import csv
import os
from collections import defaultdict
import webbrowser
from playsound import playsound
from tkinter import *
import tkinter
import cv2
import species as sp
#import this

##Variables
#Takes all files from directory and removes non-audio files
cliplist = os.listdir("audio")
cliplist.remove("analyser.praat")
for file in cliplist:
    if not file.endswith(".wav"):
        cliplist.remove(file)

#Converts the relative path of the audio folder into the absolute path
c = os.path.abspath("audio")

##Functions
#Clears the console
def clearConsole():
    os.system('cls' if os.name=='nt' else 'clear')
    print("Console cleared")
    cv2.destroyAllWindows()
    textBox.config(text="Info will go here")
    clicked.set(cliplist[0])

#Opens the GitHub page
def info():
    webbrowser.open_new("https://github.com/sidewalkchalka/species-finder")

#Gets all relevent information and creates an array of data
def mysptotal(m,p,x,species):

    #Changes local variables
    sound=p+"/"+m
    sourcerun=p+"/analyser.praat"
    path=p+"/"

    try:
        #Gets total Data
        objects = run_file(sourcerun, -20, 2, 0.3, "yes",sound,path, 80, 400, 0.01, capture_output=True)
        t1 = str(objects[1])
        t2 = t1.strip().split()
        t3 = np.array(t2)
        t4 = np.array(t3)[np.newaxis]
        t5 = t4.T

        #Subtracts max by min to get range
        maxTemp = float(t5[11])
        minTemp = float(t5[10])

        #Saves information into array
        rows = [
            x,
            species,
            float(t5[7]),
            float(t5[8]),
            float(t5[9]),
            float(maxTemp-minTemp),
            float(t5[12]),
            float(t5[13]),
        ]
        return rows

    #If fails to work, then print this
    except:
        print("Failed analysis of \"" + m + "\"")

#Defines the headers of data types
fields = [
        "clip",
        "species",
        "frequency mean",
        "frequency standard deviation",
        "frequency median",
        "frequency range",
        "frequency quantile 25th",
        "frequency quantile 75th",
        ]

#Plays sound when play button is clicked
def playDef():
    playsound("audio/" + clicked.get())

#Writes CSV data
def writecsv(rows,fields):
    with open('data.csv', 'a') as f:
        write = csv.writer(f)
        write.writerow(rows)

#Analyzes only the selected audio file
def targanalyze():
    #Defines data for analyzing, "x" and "species" are never used but they have to be defined or it will crash
    clipname = clicked.get()
    p=clipname
    x = clicked.get()
    species = "unknown"
    target = mysptotal(p,c,x,species)
    return target

#Processes data
def analyze():
    #Writes fields on the top of the datasheet
    with open('data.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(fields)

    #Runs everything for the number of audio files
    for x in cliplist:
        #Stores the first name of the array into the used clip (I know I messed this up but I'm scared about what will happen if I change it)
        clipname = x
        p=clipname
        #Creates a second variable without the .wav
        clipshort = x[:-4]
        #Asks species.py for the species assigned to the name of audio file. If there isn't one, it won't analyze the file.
        try:
            species = getattr(sp, clipshort)
        except:
            continue

        #Tries to get the data out of the funcations and then tells the functions to save them into the datasheet
        try:
            #Reads and saves the total function
            rows = mysptotal(p,c,x,species)
            #Reads and writes functions
            writecsv(rows,fields)
        except:
            print("Couldn't display data from \"" + x + "\"")

        #This prints what file was just analyzed
        print("The file analyzed was \"" + x + "\"")
        
    print("Done analying")

##Reads csv file
def read():
    #Gets target data and stores it then removes the first two items
    target = targanalyze()
    target = target[2:]

    #Reads column data from the data file and creates a dictionary
    columns = defaultdict(list)
    with open('data.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            for (k,v) in row.items():
                columns[k].append(v)

    #Converts dictionary into array and converts string numbers into floats
    speciesData = columns['species']
    fmeanData = list(map(float, columns['frequency mean']))
    fsdData = list(map(float, columns['frequency standard deviation']))
    fmedianData = list(map(float, columns['frequency median']))
    frData = list(map(float, columns['frequency range']))
    fq25th = list(map(float, columns['frequency quantile 25th']))
    fq75th = list(map(float, columns['frequency quantile 75th']))

    #Finds closest value in arrays
    fmeanDataClose = min(fmeanData, key=lambda listValue : abs(listValue-target[0]))
    fsdDataClose = min(fsdData, key=lambda listValue : abs(listValue-target[1]))
    fmedianDataClose = min(fmedianData, key=lambda listValue : abs(listValue-target[2]))
    frDataClose = min(frData, key=lambda listValue : abs(listValue-target[3]))
    fq25thClose = min(fq25th, key=lambda listValue : abs(listValue-target[4]))
    fq75thClose = min(fq75th, key=lambda listValue : abs(listValue-target[5]))

    #Saves data into their own array to be used with for loops
    data = [fmeanData, fsdData, fmedianData, frData, fq25th, fq75th]
    close = [fmeanDataClose, fsdDataClose, fmedianDataClose, frDataClose, fq25thClose, fq75thClose]

    #Dictionary of all species
    species = {
        "Wolf": 0,
        "Fox": 0,
        "Dog": 0,
        "BigCat": 0,
        "Dragon": 0,
        "Rabbit": 0,
        "Raccoon": 0,
        "Reptile": 0,
        "Otter": 0,
        "Horse": 0,
        "Hyena": 0,
        "Deer": 0,
        "Squirrel": 0,
        "Cat": 0,
        "Coyote": 0
    }

    ##Scans every item and adds a point to the matching species (this was so much fun coding and I definitely liked spending two weeks trying to figure out why it wasn't working)
    #For every array in data
    c=-1
    for g in data:
        i=-1
        c=c+1
        #For every value in the array that the above for loop got
        for d in g:
            i = i+1
            #If one of those values equals the equivalent close value, add a point to the correct species
            if d == close[c]:
                #If species has multiple values, split and convert into array
                if ", " in speciesData[i]:
                    speciesArray = speciesData[i].split(", ", -1)
                    #Adds point to each of the split values
                    for a in speciesArray:
                        species[a] = species[a] + 1
                else:
                    species[speciesData[i]] = species[speciesData[i]] + 1

    #Gets the max value of the dictionary and stores it as an array
    global result
    result = []
    result.append(max(species, key=species.get))

    #Checks if there are multiple results with the same value and and adds them to an array
    global resultMatched
    resultMatched = 0
    resultValue = species[result[0]]
    result = []
    for s in species:
        if species[s] == resultValue:
            resultMatched = resultMatched + 1
            result.append(s)

    #Shows the image or images and prints the output
    showImage()
    for r in result:
        print("Found: " + r)
    print("Done reading")

#Displays the resulting image or images
def showImage():
    cv2.destroyAllWindows()
    #If there is only one result
    if resultMatched<2:
        try:
            image = "images/" + result[0] + ".png"
            image = cv2.imread(image)
            cv2.imshow(clicked.get()[:-4] + "'s result", image)
        except:
            image = cv2.imread("images/missing.png")
            cv2.imshow(str(result[0]), image)
    #If there is more than one result, opens multiple windows
    else:
        i=0
        for r in result:
            i=i+1
            try:
                image = "images/" + r + ".png"
                image = cv2.imread(image)
                cv2.imshow(clicked.get()[:-4] + "'s result " + str(i), image)
            except:
                image = cv2.imread("images/missing.png")
                cv2.imshow(str(r), image)

##TKinter
root = tkinter.Tk()

##Hover functions
#When not hovering
def hoverLeave(event): textBox.config(text="Hover over a button")
#When hovering
def trashButtonHover(event): textBox.config(text="Resets the window")
def analyzeButtonHover(event): textBox.config(text="Analyzes all data")
def readButtonHover(event): textBox.config(text="Reads selected file")
def dropButtonHover(event): textBox.config(text="Selected file to be read")
def playButtonHover(event): textBox.config(text="Plays selected file")
def infoButtonHover(event): textBox.config(text="Opens the GitHub page")

#Stuff
root.title("Species Finder")
icon = PhotoImage(file="images/paw.png")
root.iconphoto(False, icon)
root.resizable(False, False)

#Frames
playFrame = Frame(root)

#Analyze button
analyzeImage = PhotoImage(file="images/analyze.png")
analyzeButton = Button(root, image=analyzeImage, command=lambda:analyze())
analyzeButton.bind("<Enter>", analyzeButtonHover)
analyzeButton.bind("<Leave>", hoverLeave)
analyzeButton.grid(row=0,column=0)

#Read button
readImage = PhotoImage(file="images/read.png")
readButton = Button(root, image=readImage, command=lambda:read())
readButton.bind("<Enter>", readButtonHover)
readButton.bind("<Leave>", hoverLeave)
readButton.grid(row=0,column=1)

#Trash button
trashImage = PhotoImage(file="images/trash.png")
trashButton = Button(root, image=trashImage, command=lambda:clearConsole())
trashButton.bind("<Enter>", trashButtonHover)
trashButton.bind("<Leave>", hoverLeave)
trashButton.grid(row=0,column=2)

#Drop down
clicked = StringVar(root)
clicked.set(cliplist[0])
dropDown = OptionMenu(playFrame, clicked, *cliplist)
dropDown.config(width=14,height=1)
dropDown.bind("<Enter>", dropButtonHover)
dropDown.bind("<Leave>", hoverLeave)
dropDown.grid(row=0,column=0)

#Play button
playImage = PhotoImage(file="images/play.png")
playButton = Button(playFrame, image=playImage, command=lambda:playDef())
playButton.bind("<Enter>", playButtonHover)
playButton.bind("<Leave>", hoverLeave)
playButton.grid(row=0,column=1)

#Frames up the drop down box and the play button
playFrame.grid(row=1,column=0)

#Info button
infoImage = PhotoImage(file="images/info.png")
infoButton = Button(root, image=infoImage, command=lambda:info())
infoButton.bind("<Enter>", infoButtonHover)
infoButton.bind("<Leave>", hoverLeave)
infoButton.grid(row=1,column=2)

#Message box
global textBox
textBox = Label(root, text='Info will go here', fg="black", font=("Monaco", 9))
textBox.grid(row=1,column=1)

#Finishies Tkinter code
root.mainloop()