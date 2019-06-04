# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zbertj

import signal
import sys
import global_var as g


#默认信号处理函数
def _default_signal_handle(signum, frame):
    print(signum, "thread exit...")
    sys.exit()

#设置默认信号处理函数
def set_default_handle():
    signal.signal(signal.SIGINT, _default_signal_handle)
    signal.signal(signal.SIGTERM, _default_signal_handle)

