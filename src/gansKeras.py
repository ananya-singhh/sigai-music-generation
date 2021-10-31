import tensorflow as tf 
import music21 as m
import pathlib
import pretty_midi
import glob

from tensorflow import keras
from keras.model import Sequential

def main():
    root = tf.keras.utils.get_file(
    'midi_files',
    '../data',
    untar=True) # sets the root variable to the files in ../data
    root = pathlib.Path(root) # the root points to the head of the directory
    list_ds = tf.data.Dataset.list_files(str(root/'*/*')) #the variable list_ds is a Dataset type of all the files
    
    filenames = glob.glob(str(data_dir/'**/*.mid*')) #filenames[] array 
    print('Number of files:', len(filenames)) #seeing how many files are in the array, aka how many files there are
    
    make_generator_model() #call to make_generator_model which makes the GANS



def make_generator_model():
    model = tf.keras.Sequential() # makes a sequential model using keras