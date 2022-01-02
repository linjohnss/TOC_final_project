import os

from linebot import LineBotApi, WebhookParser
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    URITemplateAction,
    MessageTemplateAction,
    CarouselTemplate,
    CarouselColumn,
    QuickReplyButton,
    QuickReply,
    LocationAction,
    MessageAction,
    PostbackTemplateAction
)

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_search_result(reply_token, img, name, score, address, location):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token,
    TemplateSendMessage(
        alt_text='Carousel template',
        template = CarouselTemplate(
            carouselcolumn(img, name, score, address, location)
        )
    ))
    return "OK"

def send_menu(self, reply_token):
    if(self.radius == 500):
        traffic_image_url = "https://as2.ftcdn.net/v2/jpg/01/88/76/05/1000_F_188760538_4ptIF2mbkz63FgMPFUTyM6d5ByeLufro.jpg"
        traffic_type = "走路"
        label1= "機車"
        text1="機車"
        label2="開車"
        text2="開車"

    elif(self.radius == 1000):
        traffic_image_url = 'https://cdn-icons-png.flaticon.com/512/2830/2830175.png'
        traffic_type = "騎機車"
        label1= "走路"
        text1="走路"
        label2="開車"
        text2="開車"
    else:
        traffic_image_url = "https://cdn-icons-png.flaticon.com/512/1085/1085961.png"
        traffic_type = "開車"
        label1= "走路"
        text1="走路"
        label2="騎機車"
        text2="騎機車"
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token,
    TemplateSendMessage(
        alt_text='Carousel template',
        template = CarouselTemplate(
            columns=[
            CarouselColumn(
                thumbnail_image_url='https://cdn-icons-png.flaticon.com/128/685/685352.png',
                title='餐廳',
                text='什麼類型?',
                actions=[
                    MessageTemplateAction(
                        label='隨便',
                        text='找餐廳'
                    ),
                    MessageTemplateAction(
                        label='我想要...',
                        text='餐廳關鍵字'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://cdn-icons-png.flaticon.com/512/679/679739.png',
                title='便利商店',
                text='什麼類型?',
                actions=[
                    MessageTemplateAction(
                        label='隨便',
                        text='找便利商店'
                    ),
                    MessageTemplateAction(
                        label='我想要...',
                        text='便利商店關鍵字'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://cdn-icons-png.flaticon.com/512/0/308.png',
                title='大眾運輸',
                text='什麼類型?',
                actions=[
                    MessageTemplateAction(
                        label='隨便',
                        text='找大眾運輸'
                    ),
                    MessageTemplateAction(
                        label='我想要...',
                        text='大眾運輸關鍵字'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url= traffic_image_url,
                title='更換交通工具',
                text='目前為'+ traffic_type + '要更換為甚麼類型?',
                actions=[
                    MessageTemplateAction(
                        label=label1,
                        text=text1
                    ),
                    MessageTemplateAction(
                        label=label2,
                        text=text2
                    )
                ]
            )
            ]
        )
    ))
    return "OK"

def send_location_message(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, 
        TextSendMessage(text="請給我您的位置",
            quick_reply=QuickReply(
                items=[QuickReplyButton(action=LocationAction(label="傳送位置"))])))
    return "OK"

def send_keyword_message(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, 
        TextSendMessage(text="請輸入相要尋找的關鍵字",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label="速食",text="速食")),
                    QuickReplyButton(action=MessageAction(label="711",text="711")),
                    QuickReplyButton(action=MessageAction(label="中式",text="中式")),
                    QuickReplyButton(action=MessageAction(label="全家",text="全家")),
                    QuickReplyButton(action=MessageAction(label="公車",text="公車")),
                    QuickReplyButton(action=MessageAction(label="轉運站",text="轉運站")),
                ])))
    return "OK"

def carouselcolumn(img, name, score, address, location):
    column = []
    
    if len(name) < 6:
        column_num = len(name)
    else:
        column_num = 6
    for i in range(column_num):
        if(img is not None):
            column.append(CarouselColumn(
                title=name[i],
                text="Google 評分:"+str(score[i])+"\n"+address[i],
                thumbnail_image_url=img[i],
                actions=[
                    URITemplateAction(
                    label='位置',
                    uri=location[i]
                    ),
                    PostbackTemplateAction(
                        label='收藏',
                        data = name[i]+'!'+str(score[i])+'!'+address[i]+'!'+location[i]
                    )
                ]
            ))
        else:
            column.append(CarouselColumn(
                title=name[i],
                text="Google 評分:"+str(score[i])+"\n"+address[i],
                actions=[
                    URITemplateAction(
                    label='位置',
                    uri=location[i]
                    ),
                    PostbackTemplateAction(
                        label='取消收藏',
                        data = 'DELETE!'+str(i)#name[i]+'!'+str(score[i])+'!'+address[i]+'!'+location[i]
                    )
                ]
            ))
    if( len(name)== 0):     
        column.append(CarouselColumn(
            title="找不到",
            text="找不到",
            thumbnail_image_url="https://cdn-icons.flaticon.com/png/512/3585/premium/3585596.png?token=exp=1641070146~hmac=0dc18da509b75c07671dcd9e5fe691b9",
            actions=[
                MessageTemplateAction(
                    label='試試其他的吧',
                    text='選單'
                )
            ]
        ))
    return column

