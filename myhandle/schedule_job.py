# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zbertj

import time
import schedule
import itchat
import global_var as g
import threading


def sendmsg(job):
    user_name = "filehelper"
    if job[-1] == "filehelper":
        user_name = "filehelper"
    else:
        friend = itchat.search_friends(name=job[-1])
        user_name = friend[0]["UserName"]
    msg = job[-3]
    print("schedule send: ", msg)
    itchat.send_msg(msg, toUserName=user_name)

def job_sendmsg(job):
    threading.Thread(target=sendmsg, args=(job,)).start()


def schedule_job_run():
    # schedule.every(3).minutes.do(job1)
    # schedule.every(5).minutes.do(job2)
    if g.schedule_job_list != []:
        for job in g.schedule_job_list:
            if job[4] == "sendmsg":
                if job[0] == "seconds":
                    schedule.every(int(job[1])).seconds.do(job_sendmsg, job)

                elif job[0] == "minutes":
                    schedule.every(int(job[1])).minutes.do(job_sendmsg, job)

                elif job[0] == "minute" and job[3] != "0":
                    schedule.every().minutes.at(job[3]).do(job_sendmsg, job)

                elif job[0] == "hours":
                    schedule.every(int(job[1])).hours.do(job_sendmsg, job)

                elif job[0] == "hour" and job[3] != 0:
                    schedule.every().hour.at(job[3]).do(job_sendmsg, job)

                elif job[0] == "days" :
                    schedule.every(int(job[1])).day.at(job[3]).do(job_sendmsg, job)

                elif job[0] == "day" and job[3] != 0:
                    schedule.every().day.at(job[3]).do(job_sendmsg, job)


    #定时任务
    while True:
        schedule.run_pending()
        time.sleep(1)
