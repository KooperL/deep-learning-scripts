from mss import mss
import cv2
import numpy as np
import sys
from PIL import Image
import tracker

#IndexError: invalid index of a 0-dim tensor. Use `tensor.item()` in Python or `tensor.item<T>()` in C++ to convert a 0-dim tensor to a number


PATH = '/media/kooper/HDD/Call of Duty  Modern Warfare 2019/yolov5-master'
sys.path.append(PATH)
import custom

# WIDTH, HEIGHT = 640, 480
WIDTH, HEIGHT = 1280, 720 
TOP, LEFT = 455, 80

tracker = tracker.EuclideanDistTracker()

class MSSSource:
    def __init__(self):
        self.sct = mss()

    def frame(self):
        monitor = {'top': TOP, 'left': LEFT, 'width': WIDTH, 'height': HEIGHT}
        im = np.array(self.sct.grab(monitor))
        im = np.flip(im[:, :, :3], 2)  # 1
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)  # 2
        return True, im

    def release(self):
        pass


if __name__ == '__main__':
    while (True):
        source = MSSSource()
        ret, frame = source.frame()
        minimap = (frame[:300, :300])
        compass = frame
        # minimap = Image.fromarray(minimap)#.show()
        # hsv = cv2.cvtColor(minimap, cv2.COLOR_RGB2HSV)
        # blue_mask = cv2.inRange(hsv, np.array([0,100,100]), np.array([100,255,255]))
        # red_mask = cv2.inRange(hsv, np.array([100,100,100]), np.array([255,255,255]))
        cv2.imshow('', compass)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

    # out.release()
    source.release()
    cv2.destroyAllWindows()
