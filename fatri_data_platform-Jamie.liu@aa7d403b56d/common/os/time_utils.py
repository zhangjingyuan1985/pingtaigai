#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-10-01 16:26:18
# @Author  : Liumin (Jamie.Liu@fatritech.com)

import datetime

def get_time(start_time):
    step_end_time = datetime.datetime.now()
    step_end_time_str = step_end_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    step_dur_time = str((step_end_time - start_time).seconds)
    return step_end_time_str, step_dur_time