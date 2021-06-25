#!/usr/bin/env python
# encoding=utf-8
import sys
import os
import re
import time
import datetime
import copy
import json


def incre_files_tail(file_dir, file_reg, msg_reg=None, msg_format=None, check_nterval_sec=60):
    """
    监控递增文件日志并输出(根据文件名排序）
    注：要监控的是这样的一类（符合正则表达式）文件：文件必须是写完后，新生成一个文件，类似递增式产生
    :param file_dir:
    :param file_reg:文件匹配正则表达式,例如 ^postgresql-.*.log$
    :param msg_reg: 消息内容匹配正则表达式,例如 PANIC|FATAL
    :param msg_format: 消息内容格式化，入参为消息、返回值为格式化消息
    :param check_nterval_sec:最新文件检查间隔
    :return:
    """
    file_dir = file_dir if file_dir.endswith('/') else (file_dir + '/')
    # 启动检查，获取最新文件
    tail_file = None
    switch_file = False
    while not tail_file:
        try:
            files = os.listdir(file_dir)
            files_check = [x for x in files if re.findall(file_reg, x)]
            files_check.sort()
            if files_check:
                tail_file = os.path.join(file_dir, files_check[-1])
            else:
                time.sleep(5)
        except Exception as e:
            print(e)

    # tail 文件，如果有最新文件出现，切换到最新文件tail
    while True:
        try:
            check_time = datetime.datetime.now()
            f = open(tail_file)
            # 切换从开头开始，否则从末尾开始
            if not switch_file:
                f.seek(0, 2)
            while True:
                curr_position = f.tell()
                line = f.readline()
                if not line:
                    f.seek(curr_position)
                    # 检查最新文件
                    if (datetime.datetime.now() - check_time).total_seconds() > check_nterval_sec:
                        check_time = datetime.datetime.now()
                        files = os.listdir(file_dir)
                        files_check = [x for x in files if re.findall(file_reg, x)]
                        files_check.sort()
                        if files_check:
                            if os.path.join(file_dir, files_check[-1]) != tail_file:
                                tail_file = os.path.join(file_dir, files_check[-1])
                                switch_file = True
                                if f:
                                    f.close()
                                break
                else:
                    if msg_reg:
                        if re.findall(msg_reg, line):
                            if msg_format:
                                line = msg_format(line.strip())
                                print(line)
                    else:
                        if msg_format:
                            line = msg_format(line.strip())
                            print(line)
                    # 防止立即结束丢失数据，有数据等待输出后再检查最新文件
                    check_time = datetime.datetime.now()

        except Exception as e:
            print(e)


if __name__ == '__main__':
    """
    监控递增文件日志并输出(根据文件名排序）
    注：要监控的是这样的一类（符合正则表达式）文件：文件必须是写完后，新生成一个文件，类似递增式产生
    """
    tail_dir = sys.argv[1]
    ip = sys.argv[2]
    id = sys.argv[3]

    data_demo = {
        "data": {
            "host_ip": ip,
            "app_name": id,
            "app_desc": "postgres log",
            "warn_str": "PANIC_FATAL",
            "warn_info": ""
        }
    }


    def msg_format(msg):
        data = copy.deepcopy(data_demo)
        data['data']['warn_info'] = msg
        json_data = json.dumps(data)
        return json_data
    incre_files_tail(tail_dir, '^postgresql-.*.log$', msg_reg='PANIC:|FATAL:|ERROR:', msg_format=msg_format, check_nterval_sec=60)
