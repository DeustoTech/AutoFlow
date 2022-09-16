import tensorflow as tf


saved_model_path = './keras_model' 
reloaded_model = tf.saved_model.load(saved_model_path)


my_classes = ['no_void', 
              'void']

@tf.function
def convert_wav_tf(wav):
    """ convert audio to a float tensor"""
    wav = tf.squeeze(wav, axis=-1)
    return wav

# Utility functions for loading audio files and making sure the sample rate is correct.
@tf.function
def load_wav_file(filename):
    """ Load a WAV file, convert it to a float tensor"""
    file_contents = tf.io.read_file(filename)
    wav, sample_rate = tf.audio.decode_wav(
          file_contents,
          desired_channels=1)
    return wav

def detect_micturition(wav):
    waveform = convert_wav_tf(wav)   

    scores = reloaded_model(waveform)

    your_top_class = tf.math.argmax(scores)
    your_inferred_class = my_classes[your_top_class]
    class_probabilities = tf.nn.softmax(scores, axis=-1)
    your_top_score = class_probabilities[your_top_class]

    
    return  your_inferred_class=="void" and your_top_score.numpy()>=0.8

r = detectMicturition(load_wav_file("void3.wav"))
print(r)
