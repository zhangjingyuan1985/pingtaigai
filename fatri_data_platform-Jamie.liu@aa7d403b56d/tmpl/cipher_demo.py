#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-10-15 11:45:01
# @Author  : Xinhuabu (Huabu.xin@fatritech.com)
# @Link    : ${link}
# @Version : $Id$
# @note    : 演示数据加密解密的样例

#导入公用模块common里的相关包
#加密解密的包为common.cipher.crypt
#Cipher_AES是AES对称加密解密操作的类
from common.cipher.crypt import Cipher_AES

#创建一个类实例a用于加密
a = Cipher_AES()
#对a的内容进行加密
cipher_text = a.encrypt("hello world!")
#输出密文内容
print(cipher_text)

#创建一个类实例b用于解密
b = Cipher_AES()
#对刚才的密文进行解密操作还原明文内容
text = b.decrypt("zbGxagRsTMpwf4aIWdMROg==")
#输出还原的明文
print(text)

