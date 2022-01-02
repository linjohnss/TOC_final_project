import os
import googlemaps
import pygsheets
import random
from linebot import LineBotApi

places_api_key = os.getenv("GOOGLE_PLACES_API_KEY")
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)
UID = 0
def nearby_search(self, event):
    gmaps = googlemaps.Client(places_api_key)
    #radar_results = gmaps.places_radar(location = (event.message.latitude, event.message.longitude), radius = 100, type = "cafe")
    print(self.type)
    radar_results = gmaps.places_nearby(
                location=(event.message.latitude, event.message.longitude),
                type= self.type,
                keyword = self.keyword,
                radius=self.radius,
                language="zh-TW"
            )
    
    radar_results = radar_results['results']
    print(radar_results)
    selected =[]
    #return radar_results
    for i in range(len(radar_results)):
        try:
            if self.type == 'transit_station':
                selected.append(i)
            elif radar_results[i]["rating"] >= self.score and \
                radar_results[i]["business_status"] == 'OPERATIONAL' and \
                radar_results[i]["opening_hours"]["open_now"]:
                selected.append(i)
        except:
            KeyError
    if len(selected) == 0:
        print("nothing to eat")

    #restaurant = radar_results[random.choice(selected)]
    result = []
    result.append([])
    result.append([])
    result.append([])
    result.append([])
    result.append([])
    selected_num = 6
    if(len(selected) < 6):
        selected_num = len(selected)
    for i in range(selected_num):
        restaurant = radar_results[selected[i]]
        if restaurant.get('photos') is None:
            img = "https://cdn-icons.flaticon.com/png/512/3585/premium/3585596.png?token=exp=1641070146~hmac=0dc18da509b75c07671dcd9e5fe691b9"
        else:
            img = "https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth={}"\
                    .format(places_api_key, restaurant["photos"][0]["photo_reference"], restaurant["photos"][0]["width"])
        #print(restaurant)
        name = '無' if restaurant.get('name') is None else restaurant['name']
        score = 0 if restaurant.get('score') is None else restaurant['score']
        address = '無' if restaurant.get('vicinity') is None else restaurant['vicinity']
        location_uri = "https://www.google.com/maps/search/?api=1&query={},{}&query_place_id={}"\
            .format(restaurant["geometry"]["location"]["lat"], restaurant["geometry"]["location"]["lng"], restaurant["place_id"])
        
        result[0].append(img)
        result[1].append(name)
        result[2].append(score)
        result[3].append(address)
        result[4].append(location_uri) 


    return result

def handel_favorite(event):
    auth_json_path = os.getenv("AUTH_JSON_PATH")
    gc = pygsheets.authorize(service_file=auth_json_path)
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1of-7cEEA-t1A70qSwZZjU5-DBzUbmGV8rS8bErGLjLA/')
    worksheet = sh.sheet1
    result = event.postback.data.split('!')
    length = len(worksheet.get_all_records())+1
    if(result[0] == 'DELETE'):
        worksheet.delete_rows(length- int(result[1]))
        return False
    else:
        worksheet.append_table([result[0], result[1],result[2],result[3]])
        return True

def show_favorite(event):
    auth_json_path = os.getenv("AUTH_JSON_PATH")
    gc = pygsheets.authorize(service_file=auth_json_path)
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1of-7cEEA-t1A70qSwZZjU5-DBzUbmGV8rS8bErGLjLA/')
    worksheet = sh.sheet1
    data = worksheet.get_all_records()
    result = []
    result.append([])
    result.append([])
    result.append([])
    result.append([])
    data_num = len(data)-1
    while data_num >= 0:
        result[0].append(data[data_num]['name'])
        result[1].append(data[data_num]['score'])
        result[2].append(data[data_num]['address'])
        result[3].append(data[data_num]['location'])
        data_num = data_num -1
    return result
    

    

