from music21 import *
from pathlib import Path

musicdir = "C:\\Users\\Lobst\\Documents\\AIMusicInterpreter\\maestro-v3.0.0\\2018"  #change this later! Will not work off Jonah's Computer!

files = Path(musicdir)
STEP = 4 #This number is our "step". 1 = round to nearest quarter note. 2 = eighth note. etc. Higher number = better preserved music, but more data and hence more training time

pitchList = []
durationList = []
listIndex = 0

for file in files.iterdir(): #iterate through all the files
    currentSongStream = converter.parse(file).flatten() #convert the file to a useable music21 Stream
    #print(file)
    lastOffset = listIndex
    for noteOrChord in currentSongStream.iter().notes: #iterate through all the notes and chords
        if isinstance(noteOrChord, note.Note): #Check if its a note or a chord. Currently just ignoring chords until i setup the chord to pitch ID system
            noteOffset = int(round(noteOrChord.offset * STEP))
            noteDuration = int(round(noteOrChord.duration.quarterLength * STEP)) #Once I have the chord system working, when two notes evaluate to the same offset, i will treat them as a chord
            notePitch = noteOrChord.pitch.midi - 11

            while (noteOffset - lastOffset == 1 or noteOffset - lastOffset == 0) != True:
                #print("noteOffset off of lastOffset by " + str(noteOffset - lastOffset))
                pitchList.append(0)
                durationList.append(0)
                lastOffset += 1

            #print("Appending note")
            #print("Offset: " + str(noteOffset) + ", Duration: " + str(noteDuration) + ", Pitch: " + str(notePitch))
            #print("Standard format: " + str(noteOrChord.nameWithOctave))

            if noteOffset - lastOffset == 0:
                #print("Double offset detected at " + str(noteOffset))
                pitchList[noteOffset - 1] = notePitch
                durationList[noteOffset - 1] = noteDuration
            else:
                pitchList.append(notePitch)
                durationList.append(noteDuration)
            
            lastOffset = noteOffset
    listIndex += lastOffset
    break #This to to make it only parse one song. The first one is ten minutes long, more than enough for initial testing.
allNotes = list(zip(pitchList, durationList))
print(allNotes)
