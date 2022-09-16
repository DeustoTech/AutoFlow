import numpy as np
from joblib import load
import librosa


model_name = './ml_model/forest.joblib'
modeln = load(model_name)
print('***********    MODEL LOADED   ***********')
#----------------------------------------------------------------------------------
#Feature extraction: MFCC
#----------------------------------------------------------------------------------


def features_extractor_mel(wav,fs,n_mfcc):
    # parameters: https://librosa.org/doc/main/generated/librosa.feature.mfcc.html
    mfccs_features = librosa.feature.mfcc(y=wav, sr=fs, n_mfcc=n_mfcc)
    print(mfccs_features.shape)
    
    mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
    print(mfccs_scaled_features.shape)    
    return mfccs_scaled_features

 
n_mfcc = 40
def run_inference(wav,fs):
    feats2=features_extractor_mel(wav,fs,n_mfcc)
    feats=np.array(feats2).reshape(1, -1)
    result = modeln.predict(feats)
    return result


