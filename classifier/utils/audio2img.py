import audiosegment
import matplotlib.pyplot as plt
import numpy as np

def audio2img(name, file_num):
	audio = audiosegment.from_file(file_dir + "/{}_{}.m4a".format(name, file_num))

	# trim audio
	slice_num  = int(len(audio) / 10000)
	segs = [audio[i*10000:i*10000 + 10000] for i in range(0, slice_num)]

	for num, seg in enumerate(segs):
		freqs, times, amplitudes = seg.spectrogram(window_length_s=0.03, overlap=0.5)
		amplitudes = 10 * np.log10(amplitudes + 1e-9)

		# Plot
		plt.pcolormesh(times, freqs, amplitudes)
		plt.axis('off')
		plt.savefig("{}_file{}_{}.png".format(name, file_num, num), bbox_inches='tight', pad_inches=0)
		plt.close()

file_dir = "/Users/acheketa/workspace/yhack/justlisten/classifier/data/train_data"
names = ['alex', 'adam', 'joseph']
for name in names:
	audio2img(name, '1')
	audio2img(name, '2')
