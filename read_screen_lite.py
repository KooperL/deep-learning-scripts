from mss import mss
import cv2
import numpy as np
import sys
import math

# import tracker

#IndexError: invalid index of a 0-dim tensor. Use `tensor.item()` in Python or `tensor.item<T>()` in C++ to convert a 0-dim tensor to a number


# PATH = '/media/kooper/HDD/Call of Duty  Modern Warfare 2019/yolov5-master'
# PATH = 'C:\\Users\\guthe\\OneDrive\\yolov5-master'
PATH = '/media/kooper/HDD/yolov5-master'
sys.path.append(PATH)
import custom

# WIDTH, HEIGHT = 640, 480 # Previous models expect data at this WIDTH, 640...
# HEIGHT,HEIGHT1 = 854, 480 # 16:9
WIDTH, HEIGHT = 864, 486 # 32 int step   486 vs 480???
TOP, LEFT = 500, 500
FOV = 100

MIDDLE = np.array([WIDTH/2, HEIGHT/2])


# trained_on_x, trained_on_y = 640, 480
# scale = trained_on_x/WIDTH

# scale = HEIGHT1/HEIGHT
scale = 1

# tracker = tracker.EuclideanDistTracker()

class MSSSource:
    def __init__(self):
        self.sct = mss()

    def frame(self):
        monitor = {'top': TOP, 'left': LEFT, 'width': WIDTH, 'height': HEIGHT}
        im = np.array(self.sct.grab(monitor))
        im = np.flip(im[:, :, :3], 2)  # 1
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)  # 2
        #im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        return True, im

    def release(self):
        pass



if __name__ == '__main__':
    # model, pt, onnx, session, classify, device, stride, modelc, half = custom.run(weights=f'{PATH}/runs/train/exp30/weights/best.pt') # 23 cod, 28 tf2 gray
    model_output = custom.run(weights=f'{PATH}/runs/train/exp37/weights/best.pt') # COD best 35
    # fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    #out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
    source = MSSSource()
    video = cv2.VideoCapture(0)

    while (True):
        ret, img = source.frame()
        #ret, img = video.read()
        # if not ret:
        #     break
        img = cv2.resize(img, (WIDTH, HEIGHT))

        detections = []
        model_infer = custom.read(*model_output, source=img, imgsz=WIDTH)
        if len(model_infer):
            for obj in model_infer:
                x1, y1, x2, y2 = int(obj[0].item()), int(obj[1].item()*scale), int(obj[2].item()), int(obj[3].item()*scale)
                # midx = (x1 + x2) / 2
                # midy = (y1 + y2) / 2
                # apx_distance = round((y2-y1), 2)
                # apx_distance = round(1-(x2-x1)**4, 1)
                # cv2.putText(img, f'D: {apx_distance}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
                cv2.rectangle(img, (x1, y1), (x2, y2), (255*(obj[5].item()==1),255*(obj[5].item()==0),0), 1)
                # cv2.line(img, (int(WIDTH/2), int(HEIGHT/2)), (int(midx), int(midy)), (150,150,150), 1)

            mid_values = [np.array([(i[0].item()+i[2].item())/2, (i[1].item()+i[3].item())/2]) for i in model_infer]
            mouse_offsets = [MIDDLE-i for i in mid_values]
            closest = (np.argmin(np.absolute(mouse_offsets), axis=0))[0]

            cv2.line(img, (int(WIDTH/2), int(HEIGHT/2)), (int(MIDDLE[0]-mouse_offsets[closest][0]), int(MIDDLE[1]-mouse_offsets[closest][1])), (150,150,150), 1)


        #out.write(img)
        cv2.imshow('hello', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# cx in tracker not true mid

    # out.release()
    source.release()
    cv2.destroyAllWindows()


# Need to flatten the rate of change for the distance
