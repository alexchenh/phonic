import os, glob
import audiosegment
import matplotlib.pyplot as plt
import numpy as np

def audio2img(name):
	subdirs = os.listdir(os.path.join(file_dir, name))
	for subdir in subdirs:
		audio_files = glob.glob(os.path.join(file_dir, name, subdir, '*.flac'))
		for audio_file in audio_files:
			audio = audiosegment.from_file(audio_file)

			# trim audio
			slice_num  = int(len(audio) / 10000)
			segs = [audio[i*10000:i*10000 + 10000] for i in range(0, slice_num)]

			for num, seg in enumerate(segs):
				freqs, times, amplitudes = seg.spectrogram(window_length_s=0.03, overlap=0.5)
				amplitudes = 10 * np.log10(amplitudes + 1e-9)

				# Plot
				plt.pcolormesh(times, freqs, amplitudes)
				plt.axis('off')
				plt.savefig('LibriSpeech/' + os.path.basename(audio_file).replace('.flac', '') + '_{}.png'.format(num), bbox_inches='tight', pad_inches=0)

file_dir = "/Users/acheketa/workspace/yhack/justlisten/classifier/data/LibriSpeech/train-clean-100"
names = os.listdir(file_dir)
for name in names:
	audio2img(name)
