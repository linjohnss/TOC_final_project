import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from func import handel_favorite
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackEvent

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", 
    "introduce", 
    "menu", 
    "restaurant", 
    "restaurant_keyword",
    "nearby_search", 
    "convenience_store", 
    "convenience_store_keyword",
    "public_transportation",
    "public_transportation_keyword",
    "favorite"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "introduce",
            "conditions": "is_going_to_introduce",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "favorite",
            "conditions": "is_going_to_favorite",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "restaurant",
            "conditions": "is_going_to_restaurant",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "convenience_store",
            "conditions": "is_going_to_convenience_store",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "public_transportation",
            "conditions": "is_going_to_public_transportation",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "menu",
            "conditions": "change_traffic_type",
        },
        {
            "trigger": "advance",
            "source": ["restaurant", "convenience_store", "public_transportation"],
            "dest": "nearby_search",
            "conditions": "is_going_to_nearby_search",
        },
        {
            "trigger": "advance",
            "source": "restaurant_keyword",
            "dest": "restaurant",
            "conditions": "is_text",
        },
        {
            "trigger": "advance",
            "source": "convenience_store_keyword",
            "dest": "convenience_store",
            "conditions": "is_text",
        },
        {
            "trigger": "advance",
            "source": "public_transportation_keyword",
            "dest": "public_transportation",
            "conditions": "is_text",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "restaurant_keyword",
            "conditions": "is_restaurant_keyword",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "convenience_store_keyword",
            "conditions": "is_convenience_store_keyword",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "public_transportation_keyword",
            "conditions": "is_public_transportation_keyword",
        },
        {"trigger": "go_back", "source": ["introduce", "menu", "nearby_search", "favorite"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        # if not isinstance(event.message, TextMessage):
        #     continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            if isinstance(event, PostbackEvent):
                print("action")
                reply_token = event.reply_token
                if handel_favorite(event):
                    send_text_message(reply_token, "已收藏!")
                else:
                    send_text_message(reply_token, "取消收藏!")
                
            continue

        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "請按指示操作")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
