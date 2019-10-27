import os, sys
import numpy as np
import tensorflow as tf
import cv2
from model4tl import AlexNetModel

tf.app.flags.DEFINE_integer('num_classes', 10, 'Number of classes')
FLAGS = tf.app.flags.FLAGS


def main(_):
	# Placeholders
	x = tf.placeholder(tf.float32, [1, 227, 227, 3])
	dropout_keep_prob = tf.placeholder(tf.float32)

	# Model
	model = AlexNetModel(num_classes=FLAGS.num_classes, dropout_keep_prob=dropout_keep_prob)
	test = model.inference(x, training=False)

	# Image
	record()
	image = cv2.imread('./sample_spec.png')
	image = cv2.resize(image, (227, 227))
	image = image.astype(np.float32)
	mean_color=[132.2766, 139.6506, 146.9702]
	image -= np.array(mean_color)
	image = np.resize(image, [1, 227, 227, 3])

	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())

        # Load the pretrained weights
		saver = tf.train.Saver()
		saver.restore(sess, "/Users/acheketa/workspace/yhack/justlisten/classifier/training/alexnet_20191027_004206/checkpoint/model_epoch100.ckpt")
		scores = sess.run(test, feed_dict={x:image, dropout_keep_prob: 1.})
		
		print("\n\nResults: {}".format(scores))

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

if __name__ == '__main__':
	tf.app.run()
