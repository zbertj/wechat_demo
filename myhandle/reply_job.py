# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zbertj
import itchat
import requests





# def friend_chat_handle_type_1(msg):
#     # print(msg)
#     if msg["Text"] == origin_key:
#         # print(msg["FromUserName"])
#         user_key = {
#             msg["FromUserName"]: origin_key
#         }
#
#         itchat.send_msg("aaaaa", toUserName="filehelper")
#         print(user_key)
#
#     else:
#         pass

def get_response_from_tuling(text):
    url = "http://www.tuling123.com/openapi/api"
    data = {
        'key'    : '74efc2f330374edf97a9656f2c45931d',
        'info'   : text,
        'userid' : 'wechat-robot',
    }
    r = requests.post(url, data=data).json()
    return r.get("text")


def friend_chat_handle_tuling(msg):
    text = msg["Text"]
    url = "http://www.tuling123.com/openapi/api"
    data = {
        'key': '74efc2f330374edf97a9656f2c45931d',
        'info': text,
        'userid': 'wechat-robot',
    }
    r = requests.post(url, data=data).json()
    res_text = r.get("text")
    print("tuling_response: ", res_text)
    msg.user.send(res_text)


