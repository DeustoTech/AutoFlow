import tensorflow_hub as hub
import tensorflow as tf
import csv
import numpy as np

# Load the model from TensorFlow Hub.
model = hub.load('https://tfhub.dev/google/yamnet/1')

# Find the name of the class with the top score when mean-aggregated across frames.
def class_names_from_csv(class_map_csv_text):
  """Returns list of class names corresponding to score vector."""
  class_names = []
  with tf.io.gfile.GFile(class_map_csv_text) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      class_names.append(row['display_name'])

  return class_names

class_map_path = model.class_map_path().numpy()
class_names = class_names_from_csv(class_map_path)

# Executing the Model
def yamnet_run_inference(wav_data):
  waveform = wav_data / tf.int16.max #wav_data` needs to be normalized to values in `[-1.0, 1.0]
  
  #Run the model, check the output.
  scores, embeddings, spectrogram = model(waveform)
  mean_scores = np.mean(scores, axis=0)
  top_n = 3
  top_class_indices = np.argsort(mean_scores)[::-1][:top_n]
  return [class_names[top_class_indices[x]] for x in range(0, top_n, 1)]
