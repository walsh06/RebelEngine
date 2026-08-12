import atexit
import threading
import wave

import pyaudio

_audio = None
_audioLock = threading.Lock()
_tempSounds = []


def _getAudio():
    """Return the shared PyAudio instance, creating it on first use."""
    global _audio
    with _audioLock:
        if _audio is None:
            _audio = pyaudio.PyAudio()
        return _audio


def shutdown():
    """Release every sound resource. Called automatically at exit."""
    global _audio
    for sound in list(_tempSounds):
        sound.close()
    del _tempSounds[:]
    with _audioLock:
        if _audio is not None:
            _audio.terminate()
            _audio = None

atexit.register(shutdown)

def _reapTempSounds():
    for sound in list(_tempSounds):
        if not sound.isPlaying():
            sound.close()

class RBSound(object):
    """A sound loaded into memory that plays without blocking the caller.
    Playback is driven by PortAudio on its own thread, so play() returns
    immediately and the game loop keeps running.
    """
    CHUNK = 1024

    def __init__(self, soundPath):
        self.soundPath = soundPath

        with wave.open(soundPath, 'rb') as waveFile:
            sampleWidth = waveFile.getsampwidth()
            channels = waveFile.getnchannels()
            rate = waveFile.getframerate()
            self._frameSize = sampleWidth * channels
            frames = []
            data = waveFile.readframes(self.CHUNK)
            while data:
                frames.append(data)
                data = waveFile.readframes(self.CHUNK)
            self._sound = b"".join(frames)

        self._offset = len(self._sound)
        self._lock = threading.Lock()

        audio = _getAudio()
        self._stream = audio.open(format=audio.get_format_from_width(sampleWidth),
                                  channels=channels,
                                  rate=rate,
                                  output=True,
                                  start=False,
                                  stream_callback=self._readNextChunk)

    def _readNextChunk(self, inData, frameCount, timeInfo, status):
        """Feed PortAudio from its own thread. Pads with silence once finished."""
        wanted = frameCount * self._frameSize
        with self._lock:
            chunk = self._sound[self._offset:self._offset + wanted]
            self._offset += len(chunk)

        if len(chunk) < wanted:
            chunk += b"\x00" * (wanted - len(chunk))
            return (chunk, pyaudio.paComplete)
        return (chunk, pyaudio.paContinue)

    def play(self):
        """Start playing from the beginning, restarting if already playing."""
        if self._stream is None:
            raise RuntimeError("sound is closed")
        self._haltStream()
        with self._lock:
            self._offset = 0
        self._stream.start_stream()

    def stop(self):
        """Stop playback immediately. Safe to call when not playing."""
        if self._stream is None:
            return
        self._haltStream()
        with self._lock:
            self._offset = len(self._sound)

    def isPlaying(self):
        return self._stream is not None and self._stream.is_active()

    def close(self):
        """Release the stream. The sound cannot be played afterwards."""
        if self._stream is None:
            return
        self._haltStream()
        self._stream.close()
        self._stream = None

    def _haltStream(self):
        # A stream whose callback returned paComplete is inactive but not yet
        # stopped, and stopping an already stopped stream raises.
        if not self._stream.is_stopped():
            self._stream.stop_stream()

    def __enter__(self):
        return self

    def __exit__(self, excType, excValue, traceback):
        self.close()


class RBTempSound(RBSound):
    """A fire-and-forget sound that starts playing as soon as it is created.
    Each instance owns its own stream, so overlapping copies of the same sound
    play on top of each other. Instances are kept alive until playback ends and
    are then closed, so the caller need not hold a reference.
    """

    def __init__(self, soundPath):
        super(RBTempSound, self).__init__(soundPath)
        _reapTempSounds()
        _tempSounds.append(self)
        self.play()

    def close(self):
        super(RBTempSound, self).close()
        if self in _tempSounds:
            _tempSounds.remove(self)


