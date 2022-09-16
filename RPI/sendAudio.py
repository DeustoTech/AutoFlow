from datetime import datetime
import requests
import socket
import os


patient = str(socket.gethostname())
serverIP = os.environ["SERVER_IP"]
upload_audio_adress = 'http://'+serverIP+':5000/uploadAudio'
upload_log_adress = 'http://'+serverIP+':5000/uploadLog'

def send_audio():

    if not os.path.exists('audios'):
        os.makedirs('audios', exist_ok=False)

    try:
        req = post_data(upload_audio_adress)
    except requests.exceptions.ConnectTimeout:
        retry()
        return False
        
    if req.status_code == 200:
        reupload_and_send_logs()

    else:
        retry()

def retry():
    try:
        req = post_data(upload_audio_adress)
    except requests.exceptions.ConnectTimeout:
        error_log("timeout")
        return False
        
    if req.status_code == 200:
        reupload_and_send_logs()

    else:
        error_log(str(req.status_code))

def error_log(error_type):
    f=open(patient+".txt", "a+")
    time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    f.write(time+";"+error_type+";"+patient+"\n")
    f.close()
    os.rename("micturition.wav","audios/"+time+".wav")

def reupload_and_send_logs():
    for audio in os.listdir("audios"):
        try:
            req = post_data(upload_audio_adress)
        except requests.exceptions.ConnectTimeout:
            print("Timeout")
        if req.status_code == 200:
            os.remove("audios/"+audio)
    
    if os.path.exists(""+patient+".txt"):
        req = None
        try:
            post_data(upload_log_adress)
        except requests.exceptions.ConnectTimeout:
            print("Timeout")
        if req.status_code == 200:
            os.remove(""+patient+".txt")

def post_data(url):
    with open("micturition.wav", 'rb') as wavFile:
            req = requests.post(url, data={'patient': patient}, files={'file': wavFile}, timeout=2)
            return req