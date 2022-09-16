import tensorflow as tf

interpreter = tf.lite.Interpreter('tflite_model/void_model.tflite')

input_details = interpreter.get_input_details()
waveform_input_index = input_details[0]['index']
output_details = interpreter.get_output_details()
scores_output_index = output_details[0]['index']

my_classes = ['no_void', 
              'void']

def detect_micturition(wav_data):
    waveform = tf.convert_to_tensor(wav_data)

    interpreter.resize_tensor_input(waveform_input_index, [len(waveform)], strict=True)
    interpreter.allocate_tensors()
    interpreter.set_tensor(waveform_input_index, waveform)
    interpreter.invoke()

    scores = interpreter.get_tensor(scores_output_index)# (N, 521) (N, 1024) (M, 64)

    your_top_class = tf.math.argmax(scores)
    your_inferred_class = my_classes[your_top_class]
    class_probabilities = tf.nn.softmax(scores, axis=-1)
    your_top_score = class_probabilities[your_top_class]
    
    return  your_inferred_class=="void" and your_top_score.numpy()>=0.8