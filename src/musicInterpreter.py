from music21 import *
from pathlib import Path

#KNOWN PROBLEMS:
#If two notes occur in the same time slot,
#such as two 32nd notes when we are rounding to the nearest sixteenth
#Then it will count them as two sixteenth notes in a row
#I am going to make it count them as a sixteenth note chord of both of them.

#Because it currently uses lists, which are ordered, to keep track of the pitches in a chord,
#it will sometimes store a chord in the chord list multiple times, such as
#{55, 75}, {75, 55}

#Both of these problems should be fixed in the next version of this

musicdir = "C:\\Users\\Lobst\\Documents\\AIMusicInterpreter\\maestro-v3.0.0\\2018"  #change this later! Will not work off Jonah's Computer!

files = Path(musicdir)
STEP = 4 #This number is our "step". 1 = round to nearest quarter note. 2 = eighth note. etc. Higher number = better preserved music, but more data and hence more training time

pitchList = []
durationList = []
listIndex = 0
chordList = [] 

for file in files.iterdir(): #iterate through all the files
    currentSongStream = converter.parse(file).flatten() #convert the file to a useable music21 Stream
    #print(file)
    lastOffset = listIndex
    for noteOrChord in currentSongStream.iter().notes: #iterate through all the notes and chords
        noteOffset = int(round(noteOrChord.offset * STEP))
        noteDuration = int(round(noteOrChord.duration.quarterLength * STEP))
        notePitch = 0
        if isinstance(noteOrChord, note.Note): 
            notePitch = noteOrChord.pitch.midi - 11
            #TODO: treat this chord and the note already there as a chord
        else: #What to do if it's a chord
            notePitches = []
            for chordNote in noteOrChord.notes:
                notePitches.append(chordNote.pitch.midi - 11)
            #Now we have the list of pitches in the chord
            if (notePitches in chordList) == False: #if we don't already have an ID for this set of pitches
                chordList.append(notePitches)       #Then add it
            notePitch = chordList.index(notePitches) + 128
            
        while noteOffset - lastOffset > 1: #fill in the gaps
            #print("noteOffset off of lastOffset by " + str(noteOffset - lastOffset))
            pitchList.append(0)
            durationList.append(0)
            lastOffset += 1
            
        #print("Appending note")
        #print("Offset: " + str(noteOffset) + ", Duration: " + str(noteDuration) + ", Pitch: " + str(notePitch))
        #print("Standard format: " + str(noteOrChord.nameWithOctave))
        
        pitchList.append(notePitch)
        durationList.append(noteDuration)
            
        lastOffset = noteOffset
    listIndex += lastOffset
    break #This to to make it only parse one song. The first one is ten minutes long, more than enough for initial testing.
allNotes = list(zip(pitchList, durationList))
print(chordList)
print("\n")
print(allNotes)

