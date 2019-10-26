# file list to .txt

import os

labels = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
#labels = os.listdir('./sc09_img/sc09_cyclegan')
modes = ['sc09_cyclegan']

for mode in modes:
    data_path = '/home/data/speech_commands/sc09_img/' + mode
    f = open('./' + mode +'.txt', 'w+')

    for idx, label in enumerate(labels):
        file_path = os.path.join(data_path, label)
        waves = os.listdir(file_path)

        for wave in waves:
            wav_path = os.path.join(file_path, wave)
            f.write(wav_path + ' ' + str(idx) + '\n')

    f.close()
