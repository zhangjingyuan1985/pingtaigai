#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-08-13 11:03:57
# @Author  : Xinhuabu
# @Link    : ${link}
# @Version : $Id$
# 依赖安装：pip3 install pycryptodome

import logging,traceback

def log(log_text,type='info'):
    if type == 'info':
        logging.info(log_text)
    elif type == 'warning':
        logging.warning(log_text)
    elif type == 'error':
        logging.error(log_text)
    elif type == 'critical':
        logging.critical(log_text)
    else:
        logging.error('logging type error!')

def err_detail(log_file):
    traceback.print_exc(file=open(log_file,'w'))