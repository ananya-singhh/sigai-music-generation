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
    discriminator = define_discriminator() #call to define_discriminator which makes the discriminator
    generator = define_generator(network_input=sample_file, batch_data=filenames)
    
def define_discriminator(in_shape = (106,106,1)):
    #got this from a tutorial - we can change the parameters/what functions to add once we know more
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Conv2D(64, (3,3), strides=(2, 2), padding='same', input_shape=in_shape))
    model.add(tf.keras.layers.LeakyReLU(alpha=0.2))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Conv2D(64, (3,3), strides=(2, 2), padding='same'))
    model.add(tf.keras.layers.LeakyReLU(alpha=0.2))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
    #opt = tf.keras.optimizers.Adam(learning_rate=0.0002, beta_1=0.5)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()
    return model

def define_generator(network_input, batch_data):
    model = tf.keras.Sequential() # makes a sequential model using keras
    model.add(tf.compat.v1.keras.layers.CuDNNLSTM(512, return_sequences=True))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Bidirectional(tf.compat.v1.keras.layers.CuDNNLSTM(512)))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Bidirectional(tf.compat.v1.keras.layers.CuDNNLSTM(512)))
    model.add(tf.keras.layers.Dense(512))
    model.add(tf.keras.layers.Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    #model.build(input_shape=network_input.shape[1])
    model.summary()
    return model


if __name__ == "__main__":
    main()
    
