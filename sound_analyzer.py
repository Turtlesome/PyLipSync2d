import librosa
import soundfile as sf
import speech_recognition as sr
from pydub import AudioSegment, silence


'''
y to jednowymiarowa tablica numpy reprezentująca szereg czasowy audio. 
sr to częstotliwość próbkowania pliku audio. 
'''


def speechtext(audio_file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:   
        print("Listening...")

        try:

            audio = recognizer.listen(source)

            text = recognizer.recognize_google(audio)
            
            print(f"You said: {text}")
            
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            print("Trying different recognizers.")
            
            text = recognizer.recognize_sphinx(audio)
            print ("Sphinx recognized: " + text)
            
        except sr.RequestError as e:
            print(f"Request error: {e}")

        return text


def load_audio_file(audio_file):
    # sr=None oznacza, że plik audio zostanie załadowany z natywną częstotliwością próbkowania
    y, sr = librosa.load(audio_file, sr=None)
    return y, sr



def get_audio_duration(audio_file):
    # sample_rate = 48kHz
    audio_data, sample_rate = sf.read(audio_file)
    duration = len(audio_data) / sample_rate
    return duration



def get_onset_frames(y, sr):
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=512, delta=0.005)
    return onset_frames



def get_onset_times(onset_frames, sr):
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    return onset_times



def detect_silence(audio_file):
    myaudio = AudioSegment.from_wav(audio_file)
    dBFS=myaudio.dBFS
    silenzio = silence.detect_silence(myaudio, min_silence_len=150, silence_thresh=dBFS-18)

    silenzio = [((start/1000),(stop/1000)) for start, stop in silenzio]
    return silenzio