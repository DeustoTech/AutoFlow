import pyaudio
import threading
import wave
import sendAudio
import runInference_ml
import numpy as np

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 16000 # 16kHz sampling rate
chunk = 128 # 2^12 samples for buffer
dev_index = 1 # recording device

search_secs = 90 # seconds to search for
recording_secs = 60 # recording length
sample_length = 5 # audio sample length to infer
inference_frequency = 2 

micturition = False
current_sec = sample_length
micturition_start = 0

def detect_micturition(frames):
        global micturition
        global current_sec
        global micturition_start
    
        # take the last sample_length seconds
        ff = np.array(frames[-int(samp_rate/chunk)*sample_length:])
        data0 = np.frombuffer(ff, dtype='int16')

        #we pass it to float32, the format of the audios used to generate the models
        wav_data = data0.astype(np.float32, order='C') / 32768.0 
        sounds = runInference_ml.run_inference(wav_data)
        print(sounds)

        # get inference result
        if sounds == 1.0:
            micturition_start = current_sec
            print(micturition_start)
                

def record():
    
    audio = pyaudio.PyAudio() # create pyaudio instantiation

    # create pyaudio stream
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)

    frames = []
    second_length = int(samp_rate/chunk)

    global micturition
    global current_sec
    
    # loop through stream and append audio chunks to frame array
    for i in range(0,int((samp_rate/chunk)*(search_secs+recording_secs))):
        data = stream.read(chunk, exception_on_overflow = False)
        frames.append(data)
        
        # in the first sample_length seconds and every inference_frequency seconds thereafter if no micturition has been detected
        if i >= second_length*sample_length and i%(second_length)==0 and ((i/second_length)-sample_length)%inference_frequency == 0 and not micturition:
            threading.Thread(target=detect_micturition,args=(frames,)).start()
            print(current_sec)
            current_sec+=inference_frequency
            

        if i >= second_length*search_secs and not micturition: 
            break

        if i >= second_length*(recording_secs+micturition_start) and micturition: 
            break

    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # save and send succesfull micturition record
    if micturition:
        micturition = False

        # create a wav file from the audio and frames
        wavefile = wave.open('micturition.wav','wb')
        wavefile.setnchannels(chans)
        wavefile.setsampwidth(audio.get_sample_size(form_1))
        wavefile.setframerate(samp_rate)
        wavefile.writeframes(b''.join(frames[second_length*micturition_start:]))
        wavefile.close()
        print(len(frames))
        
        sendAudio.send_audio()

record()