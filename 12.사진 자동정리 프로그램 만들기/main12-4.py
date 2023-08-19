from PIL import Image
from PIL.ExifTags import TAGS
from glob import glob
from geopy.geocoders import Nominatim

# 현재 스크립트의 디렉토리를 작업 디렉토리로 설정
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) # 기본 경로를 main12-1.py로 설정

# 'glob' 함수를 사용해 '사진' 디렉토리에서 확장자가 '.jpg'와 '.png' 인 이미지 파일들의 경로를 찾아 리스트로 저장
사진들 = (glob(r'사진\*.jpg'))
사진들.extend(glob(r'사진\*.png'))

# 주어진 좌표를 사용해 역지오코딩을 수행, 해당 좌표의 주소 정보를 반환
def geocoding_reverse(lat_lng_str):
    geolocoder = Nominatim(user_agent='South Korea', timeout=None)
    address = geolocoder.reverse(lat_lng_str)
    return address

for 사진 in 사진들:
    image = Image.open(사진)
    info = image._getexif();
    image.close()
    
    if info is None:
        print(f"{사진}에 대한 EXIF 메타데이터를 찾을 수 없습니다.")
        continue
    
    taglabel = {}
    
    # 'TAGS' 딕셔너리를 사용해 태그 번호를 해석해 읽기 쉬운 태그 이름으로 변환, 'taglabel' 딕셔너리에 저장
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        taglabel[decoded] = value
    
    if 'GPSInfo' not in taglabel:
        print(f"{사진}에는 GPS 정보가 없습니다.")
        continue
    
    위도 = (((taglabel['GPSInfo'][2][2] / 60.0) + taglabel['GPSInfo'][2][1]) / 60.0) + taglabel['GPSInfo'][2][0]
    경도 = (((taglabel['GPSInfo'][4][2] / 60.0) + taglabel['GPSInfo'][4][1]) / 60.0) + taglabel['GPSInfo'][4][0]
    address = geocoding_reverse(str(위도) + "," + str(경도)) # 계산된 위도와 경도를 사용해 'geocoding_reverse' 함수를 호출해 주소 정보를 가져옴.
    address_list = address[0].split(',')
    if len(address_list) == 6:
        시도이름 = address_list[3].strip() + "_" + address_list[2].strip()
    elif len(address_list) == 5:
        시도이름 = address_list[2].strip() + "_" + address_list[1].strip()
    print("시도이름: ",시도이름)
    
    사진촬영시간 = taglabel.get('DataTime')
    if 사진촬영시간 is None:
        
        # 'DateTime' 키가 없는 경우에 대한 처리
        print(f"'DateTime' 키를 찾을 수 없습니다.")
        continue
    사진이름_변경 = "사진\\" + 시도이름 + "_" + 사진촬영시간.replace(":","-") + "." + 사진.split(".")[1]
    
    print(사진이름_변경)
    
    # 원래 파일 이름을 새로 생성한 파일 이름으로 변경
    os.rename(사진,사진이름_변경)
