#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-10-16
# @Author  : Happiless.zhang (Happiless.zhang@fatritech.com)
# @Version : v_1.0
# @note    : 读写配置模块
import configparser
import os

from common.os.os_type import os_type


def get_conf_path(project_name="fatri_data_platform", conf_dir="conf", filename="global.ini"):
    conf_path = ""
    split_char = os_type()[1]
    dirs = os.getcwd().split(split_char)
    project_path_index = dirs.index(project_name)
    for i in range(project_path_index+1):
        conf_path = conf_path + dirs[i] + split_char
    conf_path = conf_path + conf_dir + split_char + filename
    return str(conf_path)


class Config(object):

    def __init__(self, filename=get_conf_path()):
        self.filename = filename
        self.cf = configparser.ConfigParser()
        self.cf.read(filename)

    def get_conf(self, option=None, key=None):
        """
        读取配置
        :param option:      配置分类
        :param key:         配置的键
        :return:
        """
        return self.cf.get(option, key)

    def set_conf(self, option=None, key=None, value=None):
        """
        新增和修改配置
        :param option:      配置的分类
        :param key:         配置的名称
        :param value:       配置的值
        :return:
        """
        secs = self.cf.sections()
        if option not in secs:
            self.cf.add_section(option)
        self.cf.set(option, key, value)

        with open(self.filename, "w+") as f:
            self.cf.write(f)

    def delete_conf(self, option=None, key=None):
        """
        删除配置
        :param option:      配置的分类
        :param key:         配置的名称
        :return:
        """
        secs = self.cf.sections()
        if option in secs:
            if key:
                self.cf.remove_option(option, key)
            else:
                self.cf.remove_section(option)
        else:
            print("没有需要删除的配置")

        with open(self.filename, "w+") as f:
            self.cf.write(f)


if __name__ == '__main__':
    config = Config()
    print(config.get_conf(option="Kafka", key="kafka.bootstrap_servers"))
    # config.delete_conf(option="redis")
    # config.set_conf(option='hive', key="host", value="localhost")
    # config.set_conf(option='hello', key="host", value="localhost")
