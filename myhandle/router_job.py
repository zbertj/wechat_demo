# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zbertj
import re
import datetime
from myhandle import reply_job
import itchat
import global_var as g


product_list = """1.图灵机器人
2.玩游戏
3.其他
0.推出程序(switch off)"""



#判断是否是个合法用户
def is_legal_user(msg):
    id = msg["FromUserName"]
    data = itchat.search_friends(userName=msg['FromUserName'])
    nickname = data.get("NickName", None)
    if nickname in g.applet_nickname_list:
        return True, nickname
    else:
        return False, ""

#----------------------------------------------------------------
def friend_chat_applet_router(msg):
    if msg["MsgType"] == 1:
        from_user = msg["FromUserName"]
        text = msg["Text"]

        # just for legal user
        ok, nickname = is_legal_user(msg)
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
                        msg.user.send(product_list)
                        return
                    if text == "show list":#show list
                        msg.user.send(product_list)
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
                        msg.user.send("图灵机器人准备就绪")
                        return
                    #function2
                    if text == "2":
                        print("选择了2")
                        return
                    #function3
                    if text == "3":
                        print("选择了3")
                        return

                    #err cmd
                    msg.user.send("这是个错误的指令哦")
                    msg.user.send(product_list)

            elif text == "switch on":
                g.applet_status_info.update({
                    nickname: {
                        "applet_on": True,
                        "robort_on": False
                    }
                })
                msg.user.send("程序成功开启")
                msg.user.send(product_list)
                return


#----------------------------------------------------------------
def friend_chat_prevent_withdraw_router(msg):
    if msg["MsgType"] == 1:
        data = itchat.search_friends(userName=msg['FromUserName'])
        nickname = data.get("NickName",None)
        # print(nickname,"to",":", msg["Text"])

        if nickname in g.prevent_withdraw_nickname_list:
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


#----------------------------------------------------------------
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