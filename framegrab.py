import cv2
from os import listdir, remove
from os.path import isfile, join
import itertools
import random
import files
from PIL import Image #( resize tings)

#PATH = '/media/kooper/HDD/Runescape'
#PATH = '/media/kooper/HDD/Team Fortress 2'
PATH = '/media/kooper/HDD/Call of Duty  Modern Warfare 2019'


def grabframe(path, fileName):
    print(f'READING: {path}/{fileName}')
    vidcap = cv2.VideoCapture(f'{path}/{fileName}')
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    print('fps: ', fps)
    success = True
    count = 0
    while success:
        success, image = vidcap.read()
        # print('Read a new frame: ', success)
#        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        if count % (3 * int(fps)) == 1: # 3 seconds
    #        cv2.waitKey(10000)
            image = image[100:-100, 100:-100] # tf2 avoid hud
            image = cv2.resize(image, (854,480))
            # cv2.imshow('cv2screen', image)
            writePath = f'{PATH}/frames'
            frameName = random.randint(100_000_000, 999_999_999)
            if f'{fileName}.jpg' not in files.list_files(writePath):
                cv2.imwrite(f'{writePath}/{frameName}.jpg', image)
            else:
                while f'{frameName}.jpg' in files.list_files(writePath):
                    frameName = random.randint(100_000_000, 999_999_999)
                    print('looping here')
                cv2.imwrite(f'{writePath}/{frameName}.jpg', image)
       
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break
            #break
        count += 1

for i in files.list_files(f'{PATH}/720'):
    grabframe(f'{PATH}/720', i)
cv2.destroyAllWindows()
