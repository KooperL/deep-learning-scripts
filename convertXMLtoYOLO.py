from xml.dom import minidom
import os
import glob
import files

def convert_coordinates(size, box):
    inv_width = 1.0/size[0]
    inv_height = 1.0/size[1]
    x1 = (box[0]+box[1])/2.0
    y1 = (box[2]+box[3])/2.0
    w1 = box[1]-box[0]
    h1 = box[3]-box[2]
    x = x1*inv_width
    w = w1*inv_width
    y = y1*inv_height
    h = h1*inv_height
    return x, y, w, h

def convert_xml2yolo(lut, fdir, fname):

        xmldoc = minidom.parse(f'{fdir}/{fname}')
        fname_out = (f'{fdir}/{fname[:-4]}.txt')
        with open(fname_out, 'w') as f:
            size = xmldoc.getElementsByTagName('size')[0]
            width = int((size.getElementsByTagName('width')[0]).firstChild.data)
            height = int((size.getElementsByTagName('height')[0]).firstChild.data)
            itemlist = xmldoc.getElementsByTagName('object')
            for item in itemlist:
                classid = (item.getElementsByTagName('name')[0]).firstChild.data
                if classid in lut:
                    label_str = str(lut[classid])
                else:
                    # label_str = '-1'
                    label_str = '0'
                    print (f'warning: label {classid} not in look-up table')

                # get bbox coordinates
                bbox = (item.getElementsByTagName('bndbox')[0])
                xmin = (bbox.getElementsByTagName('xmin')[0]).firstChild.data
                ymin = (bbox.getElementsByTagName('ymin')[0]).firstChild.data
                xmax = (bbox.getElementsByTagName('xmax')[0]).firstChild.data
                ymax = (bbox.getElementsByTagName('ymax')[0]).firstChild.data
                box = (float(xmin), float(xmax), float(ymin), float(ymax))
                box_new = convert_coordinates((width,height), box)
                #print(bb)

                f.write(f'{label_str} ' + ' '.join([("%.6f" % dim) for dim in box_new]) + '\n')
        print (f'Wrote {fname_out}')
   
if __name__ == '__main__':

    PATH = '/media/kooper/HDD/Call of Duty  Modern Warfare 2019'
    path = files.list_files(f'{PATH}/annotations')
    # dic = {
    #     'soldier': 1,    
    #     'scout': 0,
    #     'pyro': 2,
    #     'demoman': 3,
    #     'heavy': 4,
    #     'engineer': 5,
    #     'medic': 6,
    #     'sniper': 7,
    #     'spy': 8,
    #     'player': 9,
    #     }

    dic = {
        'player': 0,
        'dead': 1,}
    for fname in path:
        if fname[-4:] != '.xml':
            continue    
        convert_xml2yolo(dic, f'{PATH}/annotations', fname)
