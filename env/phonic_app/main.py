
bucketname = "audio_uploads1"
import nlp as nlp
import datetime
from pydub import AudioSegment
import io
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

import wave
from google.cloud import storage
import os
from flask import Flask, render_template, request, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav'}
# import speech_recognition as sr

app = Flask(__name__) 

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# GOOGLE_SPEECH_API_KEY = "72414513a2849e86d1129c10a6da834564184a6f"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/", methods=["GET", "POST"])
def index():
    extra_line = ''
    if request.method == "POST":
        # Check if the post request has the file part.
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If user does not select file, browser also
        # submit an empty part without filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Speech Recognition stuff.
            # recognizer = sr.Recognizer()
            # audio_file = sr.AudioFile(file)
            # with audio_file as source:
            #     audio_data = recognizer.record(source)
            # text = recognizer.recognize_google(
            #     audio_data, key=GOOGLE_SPEECH_API_KEY, language="ru-RU"
            # )
            # extra_line = f'Your text: "{text}"'

            # Saving the file.
            # TODO: upload file as blob (32MB limit)
            filename = secure_filename(file.filename)
            filepath = app.config['UPLOAD_FOLDER'] + "/"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            extra_line += f"<br>File saved to {filepath}"
            # return redirect(url_for('uploaded_file',filename=filename))
            # Run with Google Speech
            transcript = google_transcribe(filename, filepath)
            print(transcript)
            sent = nlp.google_nlp_sentiment(transcript)
            print('Sentiment: {}, {}'.format(sent.score, sent.magnitude))

    return f"""
    <!doctype html>
    <title>Upload new File</title>
    {extra_line}
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <p/>
      <input type=submit value=Upload>
    </form>
    """

def mp3_to_wav(audio_file_name):
    if audio_file_name.split('.')[1] == 'mp3':    
        sound = AudioSegment.from_mp3(audio_file_name)
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
        sound.export(audio_file_name, format="wav")
        
def stereo_to_mono(audio_file_name):
    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")

def frame_rate_channel(audio_file_name):
    """Return the audio frame rate for the file"""
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate,channels

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    
def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

def google_transcribe(audio_file_name, filepath):
    
    file_name = filepath + audio_file_name
    mp3_to_wav(file_name)

    # The name of the audio file to transcribe
    
    frame_rate, channels = frame_rate_channel(file_name)
    
    if channels > 1:
        stereo_to_mono(file_name)
    
    bucket_name = bucketname
    source_file_name = filepath + audio_file_name
    destination_blob_name = audio_file_name
    
    upload_blob(bucket_name, source_file_name, destination_blob_name)
    
    gcs_uri = 'gs://' + bucketname + '/' + audio_file_name
    transcript = ''
    
    client = speech.SpeechClient()
    audio = types.RecognitionAudio(uri=gcs_uri)

    config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=frame_rate,
    language_code='en-US')

    # Detects speech in the audio file
    operation = client.long_running_recognize(config, audio)
    response = operation.result(timeout=10000)

    for result in response.results:
        transcript += result.alternatives[0].transcript
    
    delete_blob(bucket_name, destination_blob_name)
    return transcript

# def write_transcripts(transcript_filename,transcript):
#     f= open(output_filepath + transcript_filename,"w+")
#     f.write(transcript)
#     f.close()

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
    


