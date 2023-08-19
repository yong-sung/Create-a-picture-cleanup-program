from PIL import Image
from PIL.ExifTags import TAGS
from glob import glob

import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) # 기본 경로를 main12-1.py로 설정

사진들 = (glob(r'사진\*.jpg'))
사진들.extend(glob(r'사진\*.png'))

print("사진들:",사진들)

image = Image.open(사진들[0])
info = image._getexif()
image.close()

taglabel = {}
for tag, value in info.items():
    decoded = TAGS.get(tag, tag)
    taglabel[decoded] = value
    
print("사진정보: ",taglabel)

print("사진촬영날짜: ",taglabel['DateTime'])
print("사진촬영장소: ",taglabel['GPSInfo'])
