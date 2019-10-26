# file list to .txt

import os

labels = ['alex', 'adam', 'joseph']
modes = ['train_sample']

for mode in modes:
    data_path = '/Users/acheketa/workspace/yhack/justlisten/classifier/data/spectrogram/'
    f = open('./' + mode +'.txt', 'w+')

    for idx, label in enumerate(labels):
        file_path = os.path.join(data_path, label)
        imgs = os.listdir(file_path)

        for img in imgs:
            img_path = os.path.join(file_path, img)
            f.write(img_path + ' ' + str(idx) + '\n')

    f.close()
