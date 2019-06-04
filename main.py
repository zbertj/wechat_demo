# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zbertj

import itchat
import time
from threading import Thread
from myutil import signal
from myhandle import schedule_job
from myhandle import router_job
from itchat.content import *
import global_var as g
import configparser

# 单聊
@itchat.msg_register(INCOME_MSG, isFriendChat=True)
def friend_chat_msg_handle(msg):
        #小程序功能
        router_job.friend_chat_applet_router(msg)
        #防撤回功能
        router_job.friend_chat_prevent_withdraw_router(msg)

# 再次注册NOTE即通知类型
@itchat.msg_register(NOTE, isFriendChat=True)
def msg_handle_note(msg):
    router_job.friend_chat_note_router(msg)

# # 群聊
# @itchat.msg_register(INCOME_MSG, isGroupChat=True)
# def msg_handle_group_chat(msg):
#     if g.init_ok:
#         pass
#
# # 公众号
# @itchat.msg_register(INCOME_MSG, isMpChat=True)
# def msg_handle_mp_chat(msg):
#     if g.init_ok:
#         pass

def login_call():
    # 筛选自己的id
    nickname = itchat.search_friends().get("NickName",None)
    g.prevent_withdraw_nickname_list.append(nickname)
    g.applet_nickname_list.append(nickname)

    # 筛选指定id
    for name in g.prevent_withdraw_name_list:
        if name == "":
            continue
        for data in itchat.search_friends(name=name):
            nickname = data.get("NickName",None)
            # print("name:", nickname)
            g.prevent_withdraw_nickname_list.append(nickname)

    for name in g.applet_name_list:
        if name == "":
            continue
        for data in itchat.search_friends(name=name):
            nickname = data.get("NickName",None)
            # print("name:", nickname)
            g.applet_nickname_list.append(nickname)
    print("-----prevent_withdraw_nickname_list-----")
    print(g.prevent_withdraw_nickname_list)
    print("-----applet_nickname_list-----")
    print(g.applet_nickname_list)
    print()


def init():
    # 获取配置文件
    cf = configparser.ConfigParser()
    cf.read("./config.conf", encoding='UTF-8')

    # [wechat_prevent_withdraw]
    name = cf.get("wechat_prevent_withdraw", "name")
    g.prevent_withdraw_name_list = name.split(",")
    g.prevent_withdraw_max_store_size = cf.getint("wechat_prevent_withdraw", "max_store_size")
    g.prevent_withdraw_send_to = cf.get("wechat_prevent_withdraw", "send_to")

    # [wechat_applet]
    name = cf.get("wechat_applet", "name")
    g.applet_name_list = name.split(",")

    # [wechat_schedule]
    job_size = cf.getint("wechat_schedule", "job_size")
    if job_size > 0:
        for i in range(job_size):
            job_n = "job_%s" % (i+1)
            job_ = cf.get("wechat_schedule", job_n)
            one_job_list = job_.split(" ")
            g.schedule_job_list.append(one_job_list)
    print("-----schedule_job_list-----")
    print(g.schedule_job_list)




if __name__ == '__main__':
    init()
    # 信号处理
    signal.set_default_handle()

    # 异步微信登陆启动
    itchat.auto_login(hotReload=True, loginCallback=login_call)
    t = Thread(target=itchat.run, args=())
    t.setDaemon(True)
    t.start()

    # 定时任务功能
    schedule_job.schedule_job_run()
