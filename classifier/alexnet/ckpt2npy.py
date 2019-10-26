import tensorflow as tf
import numpy as np
import sys
from model import AlexNetModel


# Edit just these
FILE_PATH = '/home/finetune/training/alexnet_20190220_005707/checkpoint/model_epoch7.ckpt'
NUM_CLASSES = 20
OUTPUT_FILE = 'sc_epoch7.npy'


if __name__ == '__main__':
    x = tf.placeholder(tf.float32, [128, 227, 227, 3])
    model = AlexNetModel(num_classes=NUM_CLASSES)
    model.inference(x)

    saver = tf.train.Saver()
    layers = ['conv1', 'conv2', 'conv3', 'conv4', 'conv5', 'fc8']
    data = {
        'conv1': [],
        'conv2': [],
        'conv3': [],
        'conv4': [],
        'conv5': [],
        'fc8': []
    }

    with tf.Session() as sess:
        saver.restore(sess, FILE_PATH)

        for op_name in layers:
          with tf.variable_scope(op_name, reuse = True):
            biases_variable = tf.get_variable('biases')
            weights_variable = tf.get_variable('weights')
            data[op_name].append(sess.run(biases_variable))
            data[op_name].append(sess.run(weights_variable))

        np.save(OUTPUT_FILE, data)

