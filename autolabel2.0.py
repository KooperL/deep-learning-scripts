import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
 
# from mss import mss
import cv2
import numpy
import sys

from shutil import copy

import files
import convertXMLtoYOLO

model_PATH = '/media/kooper/HDD/yolov5-master'
game_PATH = '/media/kooper/HDD/Call of Duty  Modern Warfare 2019'

# libgtk-x11-2.0.so.0
# libpipewire-0.3.so.0
# Steam “Fatal Error: Failed to load steamui.so”


sys.path.append(model_PATH)
import custom

WIDTH, HEIGHT = 864, 480
RATIO = HEIGHT/WIDTH
TOP, LEFT = 500, 500




# to do, dic for labels


# def new_window(coords):
#     tk.TopLevel(root)
dic = {'0': 'player', '1': 'dead'}

def _from_rgb(rgb):
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

def xmlMain(content, name, height=HEIGHT, width=WIDTH, depth=3):
    global ANNOTATIONS
    ANNOTATIONS += 1
    with open(f'{game_PATH}/annotated/{name[:-4]}.xml', 'w') as f:
        f.write(f'''<annotation>
    <folder>frames</folder>
    <filename>{name}</filename>
    <path>{game_PATH}/images/{name}</path>
    <source>
        <database>Unknown</database>
    </source>
    <size>
        <width>854</width>
        <height>{height}</height>
        <depth>{depth}</depth>
    </size>
    <segmented>0</segmented>
    {content}
</annotation>''')

def xmlobject(cat, xmin, ymin, xmax, ymax):
    return f'''
        <object>
            <name>{cat}</name>
            <pose>Unspecified</pose>
            <truncated>0</truncated>
            <difficult>0</difficult>
            <bndbox>
                <xmin>{xmin}</xmin>
                <ymin>{ymin}</ymin>
                <xmax>{xmax}</xmax>
                <ymax>{ymax}</ymax>
            </bndbox>
        </object>'''


# class MSSSource:
#     def __init__(self):
#         self.sct = mss()

#     def frame(self):
#         monitor = {'top': TOP, 'left': LEFT, 'width': WIDTH, 'height': HEIGHT}
#         im = numpy.array(self.sct.grab(monitor))
#         im = numpy.flip(im[:, :, :3], 2)  # 1
#         im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)  # 2
#         return True, im

#     def release(self):
#         pass


def next_file():
    global name
    global IMAGES
    try:
        name = next(frames)
        label['text'] = name
        print('\n\n\n\n----------------------')
        print(f'New image: {name}')
        print(f'IMAGE NO: {IMAGES}')
        print(f'ANNOTATION NO: {ANNOTATIONS}')
        IMAGES += 1
        annotate()
    except StopIteration:
        ans = input('FINISHED. Convert to YOLO format? (y) \n')
        if ans == 'y':
            for fname in files.list_files(f'{game_PATH}/annotated'):
                if fname[-4:] != '.xml':
                    continue
                convertXMLtoYOLO.convert_xml2yolo(dic, f'{game_PATH}/annotated/{fname}')
        else:
            cv2.destroyAllWindows()
            root.destroy()


def annotate():
    labels = []
    coords = read()
    canvas.delete('select')
    file_xml = None
    to_add = ''
    if len(coords):
        for obj in coords:
            canvas.delete('select')
            x1, y1, x2, y2 = int(obj[0].item()), int(obj[1].item()), int(obj[2].item()), int(obj[3].item())
            canvas.create_rectangle(x1, y1, x2, y2 , width=1, outline=_from_rgb(((255*(obj[5].item()==1),255*(obj[5].item()==0),0))), fill='', tag='select')
            # midx = (x1 + x2) / 2
            # midy = (y1 + y2) / 2
            # apx_distance = round(1-(x2-x1)**4, 2)
            cat_raw = input('Label ML attempt. Identify this as: \nplayer: \'0\', \ndead: \'1\', \nFALSE positive: \'\' \n')
            if cat_raw == '0' or  cat_raw == '1':
                # labels.append(dic[cat_raw])
                to_add += xmlobject(dic[cat_raw], int(obj[0].item()), int(obj[1].item()), int(obj[2].item()), int(obj[3].item()))
            # elif cat_raw == '9':
            #     to_add += xmlobject(dic[0], click.pressedx, click.pressedy, click.releasedx, releasedy)
            continue
    #         cv2.rectangle(
    #             frame,
    #             (obj[0], obj[1]),
    #             (obj[2], obj[3]),
    #             (255,0,0), 2)
    #         cv2.line(
    #             frame,
    #             (int(WIDTH/2), int(HEIGHT/2)),
    #             (int((obj[0]+obj[2])/2), int((obj[1]+obj[3])/2)),
    #             (255,0,0), 2)
    # label['image'] = ImageTk.PhotoImage(Image.fromarray(frame))
    while True:
        draw_cat = input('Select player bounding box then hit (0: player, 1: dead) to add new object.\nLeave empty to continue. \n')
        if draw_cat == '0' or  draw_cat == '1':
            xmin = (click.pressedx*(click.pressedx<click.releasedx))+(click.releasedx*(click.pressedx>click.releasedx))
            ymin = (click.pressedy*(click.pressedy<click.releasedy))+(click.releasedy*(click.pressedy>click.releasedy))
            xmax = (click.pressedx*(click.pressedx>click.releasedx))+(click.releasedx*(click.pressedx<click.releasedx))
            ymax = (click.pressedy*(click.pressedy>click.releasedy))+(click.releasedy*(click.pressedy<click.releasedy))

            to_add += xmlobject(dic[draw_cat], xmin, ymin, xmax, ymax)
        else:
            break
    if len(to_add):
        file_xml = xmlMain(content=to_add, name=name)
        print(file_xml)
    copy(f'{frameFolder}/{name}', f'{frameFolder}/../annotated/{name}') #shutil.
    next_file()

def read():
    # while name[-4:] != '.jpg':
    #     continue
    img = Image.open(f'{frameFolder}/{name}')
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
    frame = np.asarray(img)
    frame = frame[:, :, [2, 1, 0]] #BGR TO RGB
    frame = numpy.flip(frame[:, :, :3], 2) #?????

    img = ImageTk.PhotoImage(Image.fromarray(frame))
    canvas.background = img
    bg = canvas.create_image(0, 0, anchor=tk.NW, image=img)

    coords = custom.read(*model_output, source=frame, imgsz=WIDTH)
    return coords


frameFolder = f'{game_PATH}/frames'
frames = iter(files.list_files(frameFolder))
model_output = custom.run(weights=f'{model_PATH}/runs/train/exp35/weights/best.pt')
name = None

def lmb_motion(e):
    canvas.delete('select')
    canvas.create_rectangle(click.pressedx, click.pressedy, e.x, e.y, width=2, outline='blue', fill='', tag='select')

def motion(e):
    canvas.delete('mouse_lines')
    canvas.create_rectangle(0, e.y, WIDTH, e.y, width=2, outline='black', fill='', tag='mouse_lines')
    canvas.create_rectangle(e.x, 0, e.x, HEIGHT, width=2, outline='black', fill='', tag='mouse_lines')

class LMB_Actions():
    def __init__(self):
        self.pressedx = None
        self.pressedy = None
        self.releasedx = None
        self.releasedy = None


def lmb_pressed(e):
    click.pressedx = max(min(e.x, WIDTH), 0)
    click.pressedy = max(min(e.y, HEIGHT), 0)

def lmb_released(e):
    click.releasedx = max(min(e.x, WIDTH), 0)
    click.releasedy = max(min(e.y, HEIGHT), 0)

IMAGES = 0
ANNOTATIONS = 0

click = LMB_Actions()

# def main():
    # WIDTH, HEIGHT = 1920, 1080
    # if not len(frames):
    #     return 'No frames detected'
root = tk.Tk()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    
canvas.bind('<Button>', lmb_pressed)
canvas.bind('<ButtonRelease>', lmb_released)
canvas.bind('<B1-Motion>', lmb_motion)
canvas.bind('<Motion>', motion)

#fourcc = cv2.VideoWriter_fourcc(*'DIVX')
#out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
continueButton = tk.Button(root, text='Next', command = next_file)
label = tk.Label(root, text=name)#bg='brown')

label.pack()
continueButton.pack()
canvas.pack()
root.mainloop()
# out.release()
# source.release()
cv2.destroyAllWindows()
root.destroy()


# if __name__ == '__main__':
#     main()
