# file list to .txt
import os

modes = ['train', 'val']

for mode in modes:
	data_path = '/Users/acheketa/workspace/yhack/justlisten/classifier/utils/LibriSpeech/'
	imgs = os.listdir(data_path)
	f = open('./' + mode +'.txt', 'w+')
	labels = os.listdir(data_path.replace('utils', 'data') + 'train-clean-100')
	
	for img in imgs:
		label = os.path.basename(img).split('-')[0]
		img_path = os.path.join(data_path, img)
		f.write(img_path + ' ' + str(labels.index(label)) + '\n')
	
	f.close()
