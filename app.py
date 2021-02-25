import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "hungry", "yule", "xuyue", "huoli", "queue", "win", "buffet", "hanlai", "xiangshi", "defeat","interrupt"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "hungry",
            "conditions": "is_going_to_hungry",
        },
        {
            "trigger": "advance",
            "source": "hungry",
            "dest": "yule",
            "conditions": "is_going_to_yule",
        },
        {
            "trigger": "advance",
            "source": "yule",
            "dest": "xuyue",
            "conditions": "is_going_to_xuyue",
        },
        {
            "trigger": "advance",
            "source": "xuyue",
            "dest": "win",
            "conditions": "is_going_to_win",
        },
        {
            "trigger": "advance",
            "source": "yule",
            "dest": "huoli",
            "conditions": "is_going_to_huoli",
        },
        {
            "trigger": "advance",
            "source": "huoli",
            "dest": "xuyue",
            "conditions": "is_going_to_xuyue",
        },
        {
            "trigger": "advance",
            "source": "huoli",
            "dest": "queue",
            "conditions": "is_going_to_queue",
        },
        {
            "trigger": "advance",
            "source": "queue",
            "dest": "defeat",
            "conditions": "is_going_to_defeat",
        },
        {
            "trigger": "advance",
            "source": "hungry",
            "dest": "buffet",
            "conditions": "is_going_to_buffet",
        },
        {
            "trigger": "advance",
            "source": "buffet",
            "dest": "xiangshi",
            "conditions": "is_going_to_xiangshi",
        },
        {
            "trigger": "advance",
            "source": "buffet",
            "dest": "hanlai",
            "conditions": "is_going_to_hanlai",
        },
        {
            "trigger": "advance",
            "source": "xiangshi",
            "dest": "defeat",
            "conditions": "is_going_to_defeat",
        },
        {
            "trigger": "advance",
            "source": "hanlai",
            "dest": "defeat",
            "conditions": "is_going_to_defeat",
        },
        {"trigger": "advance", "source": ["hungry", "yule", "xuyue", "huoli", "queue", "win", "buffet","hanlai","xiangshi","defeat"], "dest": "interrupt","conditions": "is_going_to_interrupt",},
        {"trigger": "go_back", "source": ["hungry", "yule", "xuyue", "huoli", "queue", "win", "buffet","hanlai","xiangshi","defeat","interrupt"], "dest": "user"},
        #{"trigger": "advance", "source": ["hungry", "yule", "buffet","hanlai","xiangshi","defeat"], "dest": "user", "conditions": "is_going_to_user"},

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
        if not isinstance(event.message, TextMessage):
            continue

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
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        # if response == False:
        #     send_text_message(event.reply_token, "這樣好像沒有用ㄟQQ 要不要試著點擊按鈕或者輸入help以獲得幫助呢?")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)