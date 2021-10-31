import tensorflow as tf 
import music21 as m
import pathlib

from tensorflow import keras

def main():
    make_generator_model() 



def make_generator_model():
    model = tf.keras.Sequential() # makes a sequential model using keras