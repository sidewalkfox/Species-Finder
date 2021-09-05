# species-finder
### Features
- Analyzes and reads audio files to attempt to find species.
- Audio playback.

**To install**
1. Install Python (This was made in 3.9.2).
2. Install all dependencies from the `requirements.txt` file.

**To add more audio files**
1. Close the program.
2. Add a `.wav` file that is longer than 7 seconds (no spaces and capitalized) to the "audio" folder.\
*Make sure your audio files don't get longer than 15 seconds or the analysis process will soft lock the program.*
3. In `species.py`, add the name of the audio clip (without the .wav) and set it equal to the species.
4. Analyze

**To add another species *(advanced)***
1. Close the program.
2. Add a `.png` image with your species name (no spaces, capitalized, and 400x300 resolution) to the "images" folder.
3. At line 178 in `main.py`, add the species to the dictionary and give it a value of "0".
4. Analyze

**To run**
1. Open with your preferred IDE or run with the python console.
2. Press any button (you can hover over every button to find out what it does).

**To analyze**
1. Press the analyze button (brain image).\
*Every change to the data will require a new analysis.*\
*If an audio file cannot be analyzed, a message will appear in the console.*\
*The program may become unresponsive, this is normal, the program will become responsive after analysis if finished.*

**To read**
1. Select the audio file you want to read from the drop down box.
2. Press the read button (magnifying glass).\
*The resulting image will open in a new window (if multiple show up, both species were found).*

**Info button**\
This button will open the GitHub page.

**Trash button**\
This button will clear the console, reset the drop down box, and close all image windows.

**Play button**\
This button will play the selected audio file.\
*The program may become unresponsive, this is normal, it will become responsive once the audio file is over.*

**Troubleshooting**\
Is everything spelled right? Are your sounds `.wav`? Are your images in `.png`? Do your sounds have non-vocal background noise? In an error doesn't show up, check the console. It gives a good idea on what happened.