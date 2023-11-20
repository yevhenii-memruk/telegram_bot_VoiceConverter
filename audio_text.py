from os import path

import speech_recognition as sr
from pydub import AudioSegment


class AudioConverter:

    def __init__(self, audio: str, file_name: str):
        self.audio = audio
        self.file_name = file_name
        self.recognized_text = None


    def converter_ogg_to_wav(self):
        sound = AudioSegment.from_ogg(self.audio)
        sound.export(self.file_name, format="wav")


    def audio_recognizer(self):
        r = sr.Recognizer()
        with sr.AudioFile(self.file_name) as source:
            audio = r.record(source) 

        try:
            self.recognized_text = r.recognize_google(audio, language="ru-RU") # "en-US"
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")


if __name__ == "__main__":
    test = AudioConverter(audio="audio/user_voice.ogg", file_name="result.wav")
    test.converter_ogg_to_wav()
    test.audio_recognizer()
    print(test.recognized_text)