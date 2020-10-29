#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-03 09:48:10
# @Author  : Xinhuabu (Huabu.xin@fatritech.com)
# @Link    : ${link}
# @Version : $Id$

import platform

os_list = ['Windows', 'Linux', 'Darwin']


def os_type():
    os_local = platform.system()
    if os_local == 'Windows':
        os_char = '\\'
    else:
        os_char = '/'

    return os_local, os_char