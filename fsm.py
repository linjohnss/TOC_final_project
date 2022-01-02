from transitions.extensions import GraphMachine

from utils import (send_text_message, 
                    send_search_result, 
                    send_location_message,
                    send_menu,
                    send_keyword_message)
from func import nearby_search, show_favorite

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.keyword = ''
        self.type = ''
        self.radius = 1000

    def is_going_to_introduce(self, event):
        text = event.message.text
        return text.lower() == "介紹"

    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "選單"
    
    def is_going_to_restaurant(self, event):
        type = event.message.text
        return type.lower() == "找餐廳"

    def is_restaurant_keyword(self, event):
        type = event.message.text
        return type.lower() == "餐廳關鍵字"

    def is_convenience_store_keyword(self, event):
        type = event.message.text
        return type.lower() == "便利商店關鍵字"
    
    def is_going_to_public_transportation(self, event):
        type = event.message.text
        return type.lower() == "找大眾運輸"
    
    def is_public_transportation_keyword(self, event):
        type = event.message.text
        return type.lower() == "大眾運輸關鍵字"
    
    def is_going_to_convenience_store(self, event):
        type = event.message.text
        return type.lower() == "找便利商店"
    
    def is_going_to_nearby_search(self, event):
        type = event.message.type
        return type.lower() == "location"

    def is_text(self, event):
        type = event.message.type
        return type.lower() == "text"
    
    def is_going_to_favorite(self, event):
        text = event.message.text
        return text.lower() == "收藏"
    
    def change_traffic_type(self, event):
        text = event.message.text
        if(text == '走路'):
            self.radius = 500
            return True
        elif (text == '機車'):
            self.radius = 1000
            return True
        elif ( text == '開車'):
            self.radius = 3000
            return True
        

    def on_enter_introduce(self, event):
        print("I'm entering introduce")
        reply_token = event.reply_token
        send_text_message(reply_token, "我可以替你找找附近有什麼!\n\n您可以按下選單進行操做~\n")
        self.go_back()
    
    def on_enter_favorite(self, event):
        print("I'm entering favorite")
        reply_token = event.reply_token
        result = show_favorite(event)
        send_search_result(reply_token, None, result[0], result[1], result[2], result[3])
        self.go_back()

    def on_enter_menu(self, event):
        print("I'm entering menu")
        reply_token = event.reply_token
        send_menu(self, reply_token)

    def on_enter_restaurant(self, event):
        print("I'm entering reataurant")
        reply_token = event.reply_token
        self.type = 'food'
        self.score = 4
        send_location_message(reply_token)
    
    def on_enter_convenience_store(self, event):
        print("I'm entering convenience_store")
        reply_token = event.reply_token
        self.type = 'convenience_store'
        self.score = 0
        send_location_message(reply_token)
    
    def on_enter_public_transportation(self, event):
        print("I'm entering public_transportation")
        reply_token = event.reply_token
        self.type = 'transit_station'
        self.score = 0
        send_location_message(reply_token)
    
    def on_enter_restaurant_keyword(self, event):
        print("I'm entering restaurant_keyword")
        reply_token = event.reply_token
        send_keyword_message(reply_token)

    def on_enter_convenience_store_keyword(self, event):
        print("I'm entering convenience_store_keyword")
        reply_token = event.reply_token
        send_keyword_message(reply_token)
    
    def on_enter_public_transportation_keyword(self, event):
        print("I'm entering public_transportation_keyword")
        reply_token = event.reply_token
        send_keyword_message(reply_token)

    def on_enter_nearby_search(self, event):
        print("I'm entering nearby_search")
        reply_token = event.reply_token
        restaurant = nearby_search(self, event)
        print(restaurant[1])
        send_search_result(
            reply_token,
            restaurant[0],
            restaurant[1],
            restaurant[2],
            restaurant[3],
            restaurant[4]
        )
        self.keyword = ''
        self.type = ''
        self.go_back()

    def on_exit_restaurant_keyword(self, event):
        self.keyword = event.message.text

    def on_exit_convenience_store_keyword(self, event):
        self.keyword = event.message.text
    
    def on_exit_public_transportation_keyword(self, event):
        self.keyword = event.message.text

    

    