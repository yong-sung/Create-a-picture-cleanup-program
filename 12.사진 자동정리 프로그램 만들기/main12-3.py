from geopy.geocoders import Nominatim

def geocoding_reverse(lat_lng_str):
    geolocoder = Nominatim(user_agent='South Korea', timeout=None)
    address = geolocoder.reverse(lat_lng_str)
    return address

address = geocoding_reverse('54.1811999999917759, 16.8900000000141404')
print("주소: ",address)

address_list = address[0].split(',')
print("주소리스트: ",address_list)

시도이름 = address_list[2].strip() + "_" + address_list[1].strip()
print("시도이름: ",시도이름)