from flask import Flask, render_template, request, jsonify
from pydub import AudioSegment
from pydub.playback import play
import os
import wave
import io

app = Flask(__name__)

# Path to store uploaded audio files
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for the main page
@app.route('/')
def index():
    # Placeholder word in English (to be translated into French for pronunciation)
    word = 'apple'  
    return render_template('index.html', word=word)

# Route to handle audio upload
@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio_data' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    
    audio_file = request.files['audio_data']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], 'user_audio.wav')
    
    # Save the audio file
    audio_file.save(filename)
    
    # Convert audio to string (optional placeholder functionality)
    audio_data = convert_audio_to_wav(filename)

    return jsonify({"message": "Audio uploaded successfully", "transcription": audio_data})

def convert_audio_to_wav(audio_path):
    # This function converts audio to a .wav file format and returns the file path
    sound = AudioSegment.from_file(audio_path)
    wav_io = io.BytesIO()
    sound.export(wav_io, format="wav")
    
    # You can further process the .wav file for model input here
    return "Audio saved for further processing."

if __name__ == '__main__':
    app.run(debug=True)
