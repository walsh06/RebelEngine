import pyaudio
import wave
import time

class RBSound(object):

    def __init__(self, soundPath):
        self.soundPath = soundPath
        self.wf = wave.open(self.soundPath, 'rb')

        self.CHUNK = 1024
        self.p = pyaudio.PyAudio()
        data = self.wf.readframes(self.CHUNK)
        self._sound = data
        while data != '':
            data = self.wf.readframes(self.CHUNK)
            self._sound += data

        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.wf.getnchannels(),
                                  rate=self.wf.getframerate(),
                                  output=True)

    def play(self):
        self.stream.write(self._sound)


class RBTempSound(object):

    def __init__(self, soundPath):
        self.soundPath = soundPath
        self.wf = wave.open(self.soundPath, 'rb')

        self.CHUNK = 1024
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.wf.getnchannels(),
                                  rate=self.wf.getframerate(),
                                  output=True)
        data = self.wf.readframes(self.CHUNK)
        while data != '':
            self.stream.write(data)
            data = self.wf.readframes(self.CHUNK)
