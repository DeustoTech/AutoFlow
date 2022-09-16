#!/usr/bin/env python
# encoding: utf-8
import zipfile
import os
import io
from datetime import datetime

from flask import Flask, request, jsonify, render_template, send_file
from flask_mongoengine import MongoEngine

import AudioProcesing.audio_processing as process

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'urosound_database',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class Clinic(db.Document):
    _id = db.StringField()
    name = db.StringField()
    def to_json(self):
        return {"_id": str(self._id),
                "name": self.name}

class Patient(db.Document):
    _id = db.StringField()
    audio_number = db.IntField()
    comments = db.StringField()
    clinic = db.ReferenceField(Clinic)
    def to_json(self):
        return {"_id": str(self._id),
                "audio_number": self.audio_number,
                "comments": self.comments,
                "clinic": self.clinic}

class Audio(db.Document):
    _id = db.StringField()
    audio = db.StringField()
    date = db.DateField()
    len = db.IntField()
    patient = db.ReferenceField(Patient)
    trust = db.IntField()
    def to_json(self):
        return {"_id": self._id,
                "audio": self.audio,
                "date": self.date,
                "len": self.len,
                "patient": self.patient,
                "trust": self.trust
                }

@app.route('/downloadAudio', methods=['POST'])
def download_audio():
    audio_id = request.form.get('audio_id')
    path_to_file = Audio.objects(_id=audio_id).first().audio

    return send_file(
         path_to_file, 
         mimetype="audio/wav", 
         as_attachment=True)

@app.route('/downloadAllAudio', methods=['POST'])
def download_all_audio():
    patient_id = request.form.get('patient_id')
    patient = Patient.objects(_id=patient_id).first()
    audios = Audio.objects(patient=patient).all()
    cwd = os.getcwd()
    print(cwd)
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for audio in audios:
            path = "Server"+audio.audio[1:]
            zf.write(path, str(path).split("/")[-1])
    
    memory_file.seek(0)
    return send_file(memory_file, attachment_filename='capsule.zip', as_attachment=True)
    
@app.route('/patientList', methods=['GET'])
def list_patients():
    patient_list = Patient.objects().all()
    return render_template("listPatients.html", patient_list=patient_list)

@app.route('/audioList', methods=['POST'])
def list_audios():
    patient_id = request.form.get('patient_id')
    patient = Patient.objects(_id=patient_id).first()
    audio_list = Audio.objects(patient=patient).all()
    valid_audio_list = [audio for audio in audio_list if audio.trust != 0]
    return render_template("listAudios.html", patient = patient, audio_list=valid_audio_list)

@app.route('/micturitionData', methods=['POST'])
def micturition_data():
    audio_id = request.form.get('audio_id')
    return render_template("micturitionData.html", id=audio_id)

@app.route('/micturitionDataChart', methods=['POST'])
def micturition_data_for_chart():
    audio_id = request.form.get('audio_id')
    #Replace hardcoded value with audio_id
    audio = Audio.objects(_id="6273a401352379d58941c446").first()
    path = "Server"+audio.audio[1:]
    trust, micturition_envelope, micturition_time, p_qmax = process.process_audio(filename= path)
    return jsonify([micturition_envelope, micturition_time, p_qmax])


@app.route('/uploadAudio', methods=['GET', 'POST'])
def upload_audio():
    if request.method == 'POST':

        id = request.form.get('patient')
        patient = Patient.objects(_id=id).first()
        patient.save()

        path = './patientAudio/'+str(id)
        exists = os.path.exists(path)
        if not exists: os.makedirs(path)

        f = request.files['file']
        file_path = path+'/audio_'+str(patient.audio_number+1)+'.wav'
        with open(file_path, 'wb') as audio:
                f.save(audio)

        length = os.stat(file_path).st_size
        trust = process.process_audio(filename=file_path)[0]

        Audio(audio = file_path,
            date = datetime.now(),
            len = length,
            patient = patient.to_dbref(),
            trust = trust).save()
        
        patient.audio_number = patient.audio_number+1
        patient.save()

        return "OK"

    return render_template('index.html')

@app.route('/uploadLog', methods=['POST'])
def upload_log():
    
    patient_id = request.form.get('patient')
    f = request.files['file']
    contents = str(f.read())[2:-1]

    file_path = 'logs/'+str(patient_id)+'.txt'
    
    x = contents.split("\\n")
    x.pop()
    for content in x:
        log = open(file_path, "a+")
        log.write(""+content+"\n")
        log.close()

    return "OK"


#TO DO inicializar pacientes desde formulario
@app.route('/patientInitialization', methods=['GET'])
def patient_initialization():
    clinic = Clinic.objects(name="test").first()
    clinic._id = str(clinic._id)
    clinic.save()
    patient = Patient(_id='a', audio_number = 0,
    comments = "")
    patient.clinic = clinic.to_dbref()
    patient.save()
    return jsonify(patient)

@app.route('/testConnectivity', methods=['GET'])
def test_connectivity():
    return jsonify({"connectivity":"yes"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)