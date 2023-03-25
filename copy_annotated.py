import files
import shutil
import os
import random

PATH = '/media/kooper/HDD/Call of Duty  Modern Warfare 2019'
annotations = files.list_files(f'{PATH}/annotations')
annotated = files.list_files(f'{PATH}/annotated')
frames = files.list_files(f'{PATH}/frames')

for i in annotations:
    print(i)
    i = i.split('.xml')[0]
    if f'{i}.xml' in annotated:
        newName = random.randint(100_000_000, 999_999_999)
        shutil.copy(f'{PATH}/frames/{i}.jpg', f'{PATH}/annotated/{newName}.jpg')
        shutil.copy(f'{PATH}/annotations/{i}.xml', f'{PATH}/annotated/{newName}.xml')
    else:
        shutil.copy(f'{PATH}/frames/{i}.jpg', f'{PATH}/annotated/{i}.jpg')
        shutil.copy(f'{PATH}/annotations/{i}.xml', f'{PATH}/annotated/{i}.xml')
for ia in frames:
    os.remove(f'{PATH}/frames/{ia}')
for ia in annotations:
    os.remove(f'{PATH}/annotations/{ia}')
