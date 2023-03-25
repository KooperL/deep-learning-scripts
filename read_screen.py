from mss import mss
import cv2
import numpy as np
import sys
import math

import tracker_traj

# PATH = '/media/kooper/HDD/Call of Duty  Modern Warfare 2019/yolov5-master'
PATH = '/media/kooper/HDD/yolov5-master'
sys.path.append(PATH)
import custom

# WIDTH, HEIGHT = 640, 480 # Previous models expect data at this WIDTH, 640...
HEIGHT,HEIGHT1 = 854, 480 # 16:9
WIDTH, HEIGHT = 864, 480 # 32 int step
TOP, LEFT = 500, 500
FOV = 100

# trained_on_x, trained_on_y = 640, 480
# scale = trained_on_x/WIDTH

scale = HEIGHT1/HEIGHT
scale = 1

tracker = tracker_traj.EuclideanDistTracker()

velocity_history = {}


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
    #fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    #out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
    
    source = MSSSource()
    vid = cv2.VideoCapture(0)

    while (True):
        ret, img = source.frame()
        #ret, img = vid.read()

        img = cv2.resize(img, (WIDTH, HEIGHT))

        if not ret:
            break
        detections = []
        coords = custom.read(*model_output, source=img, imgsz=WIDTH)
        if len(coords):
            for obj in coords:
                x1, y1, x2, y2 = int(obj[0].item()), int(obj[1].item()*scale), int(obj[2].item()), int(obj[3].item()*scale)
                # midx = (x1 + x2) / 2
                # midy = (y1 + y2) / 2
                # apx_distance = round((y2-y1), 2)
                # apx_distance = round(1-(x2-x1)**4, 1)
                # cv2.putText(img, f'D: {apx_distance}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
                # cv2.rectangle(img, (x1, y1), (x2, y2), (255*(obj[5].item()==1),255*(obj[5].item()==0),0), 1)
                # cv2.line(img, (int(WIDTH/2), int(HEIGHT/2)), (int(midx), int(midy)), (150,150,150), 1)

                if obj[5].item() == 0:
                    detections.append([x1, y1, x2, y2]) 

        boxes_ids = tracker.update(detections)
        for box_id in boxes_ids:
            x1, y1, w, h, cx, cy, z, id = box_id
            x2 = x1 + w
            y2 = y1 + h
            # cv2.putText(img, str(z), (x1, y1 - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.putText(img, str(id), (x1, y1-h), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            # cv2.rectangle(img, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 3)
            stats = tracker.history[id]

            x1, y1, w, h, midx, midy, z, id = box_id

            # x2 = x1 + w
            # y2 = y1 + h

            x2 = w
            y2 = h

            try:
                # print(stats)
                time_difference = (stats[0][1] - stats[len(stats)-1][1]).total_seconds()
                distance = np.sqrt(np.sum((stats[0][0] - stats[len(stats)-1][0])**2))   # FAILS IF OFF SCREEN
                direction = stats[0][0] - stats[len(stats)-1][0]
                if time_difference != 0 and distance != 0:
                    speed = distance/time_difference
                    velocity = (speed/distance)*direction
                    displacement = velocity * 1 # time
                    aim_here = (displacement + stats[0][0])# + (gravity*time)
                    aim_here = [int(i) for i in aim_here]

                    if id in velocity_history:
                        velocity_history[id].insert(0, aim_here)
                        if len(velocity_history[id]) > 10:
                            velocity_history[id].pop()
                    else:
                        velocity_history[id] = [aim_here]

                    # cv2.line(img, (int(aim_here[0]), int(aim_here[1])), (midx, midy), (0,0,255), 1)
                    if len(velocity_history[id]) > 1:
                        smooth_aim_here = np.mean(velocity_history[id], axis=0)
                        # print(smooth_aim_here)
                        # print(type(smooth_aim_here[1]))
                        cv2.line(img, (int(smooth_aim_here[0]), int(smooth_aim_here[1])), (midx, midy), (0,0,255), 1)

                        ## Parabola time
                        # pts = np.array([[25, 70], [25, 160], 
                        #     [110, 200], [200, 160], 
                        #     [200, 70], [110, 20]],
                        #    np.int32)
                        # pts = np.array([[i, (-i**2)+(i*smooth_aim_here[1])] for i in range(WIDTH-midx)])
                        # print(pts)
                        # pts = pts.reshape((-1, 1, 2))
                        # cv2.polylines(img, [pts], False, (255,0,0), 2)



                # tracker.history[object_id] = objects_bbs_ids
                # apx_distance = round((y2-y1), 2)
                cv2.putText(img, f'D: {z}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 1)
                # cv2.line(img, (int(WIDTH/2), int(HEIGHT/2)), (int(midx), int(midy)), (150,150,150), 1)
            except ValueError:
                pass

        #out.write(img)
        cv2.imshow('hello', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# cx in tracker not true mid

    # out.release()
    source.release()
    cv2.destroyAllWindows()


# Need to flatten the rate of change for the distance
