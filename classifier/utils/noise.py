import random
#import librosa
from scipy.io import wavfile
from tensorflow.python.platform import gfile
import numpy as np

LEN = 16000
NOISE_VOLUME = 0.1
NOISE_FREQUENCY = 0.8

# call noises.wav
noise_paths = '/home/data/speech_commands/etc/_background_noise_/*.wav'
noises = []
for noise_path in gfile.Glob(noise_paths):
    #noise = librosa.core.load(noise_path, sr=None, duration=1)[0] * NOISE_VOLUME
    noise = wavfile.read(noise_path)[1][:LEN] * NOISE_VOLUME
    noises.append(noise)

# call train audio
wav_path = './sc09_wav/train/*/*.wav'
waves = gfile.Glob(wav_path)
random.shuffle(waves)

# add background noise
for idx, wave in enumerate(waves):
    data = wavfile.read(wave)[1]
    if idx <= len(waves) * NOISE_FREQUENCY:
        #data, _ = librosa.core.load(wave, sr=None, duration=1)
        if len(data) < LEN:
            data = np.pad(data, (0, max(0, LEN - len(data))), "constant")
        else:
            data = data[:LEN]
        index = random.randint(0, 4)
        noise_data = noises[index]
        wavfile.write('./sc09_wav/aug/' + wave[17:], LEN, data + noise_data)
    else:
        #librosa.output.write_wav('./sc09_wav/aug/' + wave[17:], file, sr=LEN)
        wavfile.write('./sc09_wav/aug/' + wave[17:], LEN, data)
