import os, sys
import numpy as np
import tensorflow as tf
import cv2
from model4tl import AlexNetModel

def speaker_id(input_wav):
	"""
	- input_wav: a path of .wav file that needs to be analyzed
	- output_sid: an array of one hot vectors referring to individual speakers, (number of 10 sec) x 3
	"""
	
	# 1. Generate spectrogram image
	# Outputs input/spec_*.png
	from audio2img import audio2img_wav
	audio2img_wav(input_wav)

	# 2. Feed into the identifier
	# Outputs output_sid
	output_sid = []
	input_imgs = os.listdir('./input')
	ckpt = "/Users/acheketa/workspace/yhack/justlisten/classifier/training/alexnet_20191027_004206/checkpoint/model_epoch100.ckpt"
	for img in input_imgs:
		sid = identifier('./input/' + img, ckpt, num_classes=3)
		output_sid.append(sid)
	
	return output_sid, pie_chart(output_sid)


def identifier(in_img, ckpt, num_classes):
	tf.reset_default_graph()

	# Placeholders
	x = tf.placeholder(tf.float32, [1, 227, 227, 3])
	dropout_keep_prob = tf.placeholder(tf.float32)

	# Model
	model = AlexNetModel(num_classes=num_classes, dropout_keep_prob=dropout_keep_prob)
	test = model.inference(x, training=False)

	# Image
	# record()
	image = cv2.imread(in_img)
	image = cv2.resize(image, (227, 227))
	image = image.astype(np.float32)
	mean_color=[132.2766, 139.6506, 146.9702]
	image -= np.array(mean_color)
	image = np.resize(image, [1, 227, 227, 3])

	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())

        # Load the pretrained weights
		saver = tf.train.Saver()
		saver.restore(sess, ckpt) 
		scores = sess.run(test, feed_dict={x:image, dropout_keep_prob: 1.})[0]
		scores_onehot = np.where(scores == max(scores), 1, 0)
		
	return scores_onehot


def record():
	import sounddevice as sd
	from scipy.io.wavfile import write

	fs = 48000
	seconds = 10

	recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
	sd.wait()
	write('output.wav', fs, recording)
	
	# generate spectrogram image
	sys.path.insert(0, '../utils')
	from audio2img import audio2img_sample
	audio2img_sample('./output.wav')

def pie_chart(speaker_id):
	import matplotlib.pyplot as plt

	# Pie chart
	labels = ['Alex', 'Adam', 'Joseph']
	sizes = np.array(speaker_id).sum(axis=0)
	
	#colors
	colors = ['#ff9999','#66b3ff','#99ff99']
	 
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, colors = colors, labels=labels, autopct='', startangle=90)
	#draw circle
	centre_circle = plt.Circle((0,0),0.70,fc='white')
	fig = plt.gcf()
	fig.gca().add_artist(centre_circle)
	# Equal aspect ratio ensures that pie is drawn as a circle
	ax1.axis('equal')  
	plt.tight_layout()
	plt.savefig("speaker_id")
	plt.close()