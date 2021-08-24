import files
import shutil

PATH = '/media/kooper/HDD/Call of Duty  Modern Warfare 2019'
images_loc = files.list_files(f'{PATH}/images')
labels_loc = files.list_files(f'{PATH}/annotations')
# labels_loc = files.list_files(f'{PATH}/annotated')
DEST = f'{PATH}/datasets/cod_mw'
length = 0

# for fname in loc:
#     #if file[-4:] != '.txt':
#     #    continue
#     length += 1

length = len(images_loc)

for ind, fname in enumerate(images_loc):
    # if fname[-4:] != '.txt':
    #     continue
    fname = fname[:-4]
    if ind < int(length/5): # Test
        shutil.copy(f'{PATH}/images/{fname}.jpg', f'{DEST}/images/test/{fname}.jpg')
        try:
            shutil.copy(f'{PATH}/annotations/{fname}.txt', f'{DEST}/labels/test/{fname}.txt')
        except:
            continue

    elif ind > int(length/5) and ind < int(2*length/5): # Validate
        shutil.copy(f'{PATH}/images/{fname}.jpg', f'{DEST}/images/val/{fname}.jpg')
        try:
            shutil.copy(f'{PATH}/annotations/{fname}.txt', f'{DEST}/labels/val/{fname}.txt')
        except:
            continue

    else: # Train
        shutil.copy(f'{PATH}/images/{fname}.jpg', f'{DEST}/images/train/{fname}.jpg')
        try:
            shutil.copy(f'{PATH}/annotations/{fname}.txt', f'{DEST}/labels/train/{fname}.txt')
        except:
            continue
