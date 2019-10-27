"""
divide dataset into train and validation
"""

import os, shutil, random

div_ratio = [7, 3]		# train, val
file_dir = '/Users/acheketa/workspace/yhack/justlisten/classifier/data/spectrogram/'
names = ['alex', 'joseph', 'adam']

for name in names:
	imgs = os.listdir(os.path.join(file_dir, name))
	val_num = int(len(imgs) * div_ratio[1] / sum(div_ratio))

	for _ in range(val_num):
		img = random.choice(imgs)
		imgs.remove(img)
		current_dir = os.path.join(file_dir, name, img)
		target_dir 	= os.path.join(file_dir, 'val', name, img)
		shutil.move(current_dir, target_dir)
