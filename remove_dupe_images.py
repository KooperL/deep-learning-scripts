import files
import os
PATH = '/media/kooper/HDD/Call of Duty  Modern Warfare 2019'
#images_loc = files.list_files(f'{PATH}/images')
images_loc = files.list_files(f'{PATH}/annotated')
frames_loc = files.list_files(f'{PATH}/frames')
for i in images_loc:
	if i in frames_loc:
		os.remove(f'{PATH}/frames/{i}')
