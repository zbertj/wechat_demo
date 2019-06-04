# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zbertj
import re
import datetime
from myhandle import reply_job
import itchat
import global_var as g


#判断是否是个合法用户
def is_legal_user(msg):
    id = msg["FromUserName"]
    data = itchat.search_friends(userName=msg['FromUserName'])
    nickname = data.get("NickName", None)
    if nickname in g.applet_nickname_list:
        return True, nickname
    else:
        return False, ""

#判断是否是个合法用户
def is_legal_applet_user(msg):
    id = msg["FromUserName"]
    data = itchat.search_friends(userName=msg['FromUserName'])
    nickname = data.get("NickName", None)
    if nickname in g.applet_nickname_list:
        return True, nickname
    else:
        return False, ""

#判断是否是个合法用户
def is_legal_prevent_withdraw_user(msg):
    id = msg["FromUserName"]
    data = itchat.search_friends(userName=msg['FromUserName'])
    nickname = data.get("NickName", None)
    if nickname in g.prevent_withdraw_nickname_list:
        return True, nickname
    else:
        return False, ""

def is_self_cmd(msg):
    id = msg["FromUserName"]
    data = itchat.search_friends(userName=msg['FromUserName'])
    nickname = data.get("NickName", None)
    to_user = msg["ToUserName"]
    if nickname == g.applet_nickname_list[0] and to_user == "filehelper":
        return True
    else:
        return False

# ----------------------------------------------------------------
def switch_all(msg):
    if is_self_cmd(msg):
        text = msg["Text"]
        if text == "status":
            if g.auto_reply == True:
                msg.user.send("自动回复已开启")
            else:
                msg.user.send("自动回复已关闭")

            if g.applet == True:
                msg.user.send("小程序已开启")
            else:
                msg.user.send("小程序已关闭")

            if g.prevent_withdraw == True:
                msg.user.send("防撤回已开启")
            else:
                msg.user.send("防撤回已关闭")


        if text == "auto reply off":
            g.auto_reply = False
            msg.user.send("自动回复已关闭")
        elif text == "auto reply on":
            g.auto_reply = True
            msg.user.send("自动回复已开启")

        if text == "applet off":
            g.applet = False
            msg.user.send("小程序已关闭")
        elif text == "applet on":
            g.applet = True
            msg.user.send("小程序已开启")


        if text == "prevent withdraw off":
            g.prevent_withdraw = False
            msg.user.send("防撤回已关闭")
        elif text == "prevent withdraw on":
            g.prevent_withdraw = True
            msg.user.send("防撤回已开启")







# ----------------------------------------------------------------
def friend_chat_auto_reply_router(msg):
    if msg.get("MsgType", -1) == 1:
        text = msg["Text"]
        if text in ["switch on"]:
            g.auto_reply = False
        if text in ["auto reply off", "auto reply on", "applet off", "applet on", "prevent withdraw off", "prevent withdraw on"]:
            return
        # just for legal user
        ok, nickname = is_legal_user(msg)
        is_applet_on = g.applet_status_info.get(nickname, {}).get("applet_on", False)
        if ok and g.auto_reply and is_applet_on is False:
            reply_job.friend_chat_handle_tuling(msg)  # robort handler



#----------------------------------------------------------------
def friend_chat_applet_router(msg):
    if msg["MsgType"] == 1:
        from_user = msg["FromUserName"]
        text = msg["Text"]

        # just for legal user
        ok, nickname = is_legal_applet_user(msg)
        if ok:
            is_applet_on = g.applet_status_info.get(nickname, {}).get("applet_on", False)
            if is_applet_on:
                is_robort_on = g.applet_status_info.get(nickname, {}).get("robort_on", False)
                if is_robort_on:#in robort
                    if text == "exit":#robort exit, set robort_switch false
                        g.applet_status_info.update({
                            nickname: {
                                "applet_on": True,
                                "robort_on": False
                            }
                        })
                        msg.user.send("图灵机器人成功退出")
                        return
                    if text == "switch off":#program exit, set robort_switch false and set status false
                        g.auto_reply = True
                        g.applet_status_info.update({
                            nickname: {
                                "applet_on": False,
                                "robort_on": False
                            }
                        })
                        msg.user.send("程序关闭")
                        return
                    reply_job.friend_chat_handle_tuling(msg)#robort handler
                else:   #out of robort
                    if text == "switch off":#program exit
                        g.auto_reply = True
                        g.applet_status_info.update({
                            nickname: {
                                "applet_on": False,
                                "robort_on": False
                            }
                        })
                        msg.user.send("程序关闭")
                        return
                    if text == "switch on":#program already on
                        msg.user.send("程序成功已开启")
                        msg.user.send(g.product_list)
                        return
                    if text == "show list":#show list
                        msg.user.send(g.product_list)
                        return
                    #function1 图灵机器人
                    if text == "1" or text == "图灵机器人" or text == "1.图灵机器人":
                        # print("选择了图灵机器人")
                        g.applet_status_info.update({
                            nickname: {
                                "applet_on": True,
                                "robort_on": True
                            }
                        })
                        msg.user.send("图灵机器人准备就绪,输入exit可退出")
                        return
                    #function2
                    if text == "2":
                        print("选择了2")
                        msg.user.send("还在开发中")
                        msg.user.send(g.product_list)
                        return
                    #function3
                    if text == "3":
                        print("选择了3")
                        msg.user.send("还在开发中")
                        msg.user.send(g.product_list)
                        return

                    #err cmd
                    msg.user.send("这是个错误的指令哦")
                    msg.user.send(g.product_list)

            elif text == "switch on":
                g.applet_status_info.update({
                    nickname: {
                        "applet_on": True,
                        "robort_on": False
                    }
                })
                msg.user.send("程序成功开启")
                msg.user.send(g.product_list)
                return




#----------------------------------------------------------------
def friend_chat_prevent_withdraw_router(msg):
    if msg["MsgType"] == 1:
        ok, nickname = is_legal_prevent_withdraw_user(msg)
        if ok:
            msg_time_send = datetime.datetime.fromtimestamp(msg['CreateTime']).strftime('%Y-%m-%d %H:%M:%S')
            msg_id = msg['MsgId']
            msg_content = None
            msg_link = None

            if  msg['Type'] == 'Text' or msg['Type'] == 'Friends':
                msg_content = msg['Text']

            msg_info = {
                msg_id: {
                    "msg_from": nickname,
                    "msg_time_send": msg_time_send,
                    "msg_type": msg["Type"],
                    "msg_content": msg_content,
                    "msg_link": msg_link
                }
            }
            print(msg_info)
            g.prevent_withdraw_msg_info_list.append(msg_info)


            # 超过最大长度100时，删除第一条， 第一条也是时间最早的一条
            if len(g.prevent_withdraw_msg_info_list) >= g.prevent_withdraw_max_store_size:
                g.prevent_withdraw_msg_info_list.pop(0)

def friend_chat_note_router(msg):
    print(msg.get("Text", "00000"))
    if "撤回了一条消息" in msg.get("Text", "00000"):
        recall_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg.get("Content", "")).group(1)
        # print(recall_msg_id)
        # print(g.msg_info_list)
        for msg_info in g.prevent_withdraw_msg_info_list[:]:
            for id in msg_info:  # 只有一条
                info = msg_info[id]
                if recall_msg_id == id:
                    # print(info)
                    if info["msg_type"] == "Text":
                        need_send_info = "who: %s\ntime: %s\ncontent: %s\nlink: %s" % (
                            info["msg_from"], info["msg_time_send"], info["msg_content"], info["msg_link"])
                        # print(need_send_info)
                        itchat.send_msg(need_send_info, toUserName=g.prevent_withdraw_send_to)
                        g.prevent_withdraw_msg_info_list.remove(msg_info)






