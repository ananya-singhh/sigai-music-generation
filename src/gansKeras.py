import tensorflow as tf
import music21 as m
import pathlib
import pretty_midi
import glob
import fluidsynth

from tensorflow import keras
from IPython import display
#from keras.model import Sequential
def main():
    data_dir = pathlib.Path('data/maestro-v2.0.0')
    root = tf.keras.utils.get_file(
    'maestro-v2.0.0-midi.zip',
      origin='https://storage.googleapis.com/magentadata/datasets/maestro/v2.0.0/maestro-v2.0.0-midi.zip',
      extract=True,
      cache_dir='.', cache_subdir='data',) # sets the root variable to the files in ../data
    filenames = glob.glob(str(data_dir/'**/*.mid*')) #filenames[] array 
    print('Number of files:', len(filenames)) #seeing how many files are in the array, aka how many files there are
    
    sample_file = filenames[1]
    print(sample_file)
    
    pm = pretty_midi.PrettyMIDI(sample_file)
    make_generator_model() #call to make_generator_model which makes the GANS
    
def define_discriminator(in_shape = (106,106,1)):
    #got this from a tutorial - we can change the parameters/what functions to add once we know more
    model = Sequential()
    model.add(Conv2D(64, (3,3), strides=(2, 2), padding='same', input_shape=in_shape))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.5))
    model.add(Conv2D(64, (3,3), strides=(2, 2), padding='same'))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(BatchNormalization())
    model.add(Dense(1, activation='sigmoid'))
    opt = Adam(lr=0.0002, beta_1=0.5)
    model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
    return model

def make_generator_model():
    model = tf.keras.Sequential() # makes a sequential model using keras


if __name__ == "__main__":
    main()
    
