import os
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.models import MessageEvent, PostbackEvent, TextSendMessage, TemplateSendMessage, ButtonsTemplate,PostbackTemplateAction, MessageTemplateAction, URITemplateAction,ImageSendMessage


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)


def send_text_message(reply_token, text):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_button_message(reply_token,url,title,text,a):
    buttons_template = TemplateSendMessage(
    alt_text='Buttons Template',
    template=ButtonsTemplate(
        title=title,
        text=text,
        thumbnail_image_url=url,
        actions=[
            MessageTemplateAction(
                label=a,
                text=a
            ),
        ]
    )
    )
    line_bot_api.reply_message(reply_token, buttons_template)

def send_choose_message(reply_token,url,title,text,a,b):
    buttons_template = TemplateSendMessage(
    alt_text='Buttons Template',
    template=ButtonsTemplate(
        title=title,
        text=text,
        thumbnail_image_url=url,
        actions=[
            MessageTemplateAction(
                label=a,
                text=a
            ),
            MessageTemplateAction(
                label=b,
                text=b
            ),
        ]
    )
    )
    line_bot_api.reply_message(reply_token, buttons_template)

"""
def send_image_url(id, img_url):
    pass
"""