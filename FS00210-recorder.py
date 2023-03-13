# code by: utf-8
# Sinbing code
import os
import csv
import sys
import serial
import datetime
import binascii
from serial.tools import list_ports


def datetime_now():
    return datetime.datetime.now().strftime("%H:%M:%S")


def get_ports():
    ports = list_ports.comports()
    while True:
        p_name = ''
        for p in ports:
            p_name = p_name +p.device +' '
        if len(ports) > 1:
            print('搜索到串口设备： ' +p_name)
            user_input_ports = input('请输入需要使用的串口(如: COM1  输入"r"重新搜索)  \n: ')
            if user_input_ports != 'r':
                print(f'正在监听串口设备 {user_input_ports}\n')
                return user_input_ports

        else:
            print(f'正在监听唯一串口设备 {p.device}\n')
            return p.device

def csv_write(csv_path: str, csv_name: str, data_list: list):
    # 不存在csv文件时，写入首行表头
    if not os.path.exists(os.path.join(csv_path, csv_name)):
        title_data = ''
        title = ['记录时间', 'PM1.0 浓度(μg/m³) CF=1', 'PM2.5 浓度(μg/m³) CF=1', 'PM10 浓度(μg/m³) CF=1', \
'PM1.0 浓度(μg/m³) 大气环境', 'PM2.5 浓度(μg/m³) 大气环境', 'PM10 浓度(μg/m³) 大气环境', \
'0.3μm 以上直径颗粒物(0.1L空气)', '0.5μm 以上直径颗粒物(0.1L空气)', '1.0μm 以上直径颗粒物(0.1L空气)', \
'2.5μm 以上直径颗粒物(0.1L空气)', '5μm 以上直径颗粒物(0.1L空气)', '10μm 以上直径颗粒物(0.1L空气)']
        for data in title:
            title_data += f'{data}, '
        title_data = title_data[:-2] +'\n'
        with open(os.path.join(csv_path, csv_name), 'w', encoding='utf_8_sig') as f:
            f.write(title_data)
            f.flush()

    # 整理数据格式为: time, data1, data2, data3...
    write_data = f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}, '
    for data in data_list:
        write_data += f'{data}, '
    write_data = write_data[:-2] +'\n'

    # 追加写入数据, 以utf_8_sig编码让excel能读取中文
    with open(os.path.join(csv_path, csv_name), 'a', encoding='utf_8_sig') as f:
        f.write(write_data)
        f.flush()


def init():
    # 获取程序位置
    if hasattr(sys, "_MEIPASS"):
        progame_path = os.path.dirname(os.path.realpath(sys.executable))
    else:
        progame_path = os.path.split(os.path.realpath(__file__))[0]

    # 问问要不要CVS数据表输出
    while True:
        CVS = input('是否需要输出CVS数据表\n 0: 不要\n 1: 要\n    输入数字: ')
        try:
            CVS = int(CVS)
        except:
            print('请只输入数字！\n')
        if CVS == 0:
            CVS_flag = False
            break
        elif CVS == 1:
            CVS_flag = True
            break
        else:
            print('    请重新输入')
    return progame_path, CVS_flag



if __name__ == '__main__':
    # 初始化; 获取串口列表, 选择串口; 设置通信参数
    data_line, data_list, byte_count, csv_name = '', [], 0, f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_PM传感器数据.csv'
    progame_path, csv_output = init()
    ser = serial.Serial(get_ports(), baudrate=9600, bytesize=8, timeout=2)
    # Main
    while True:
        data = ser.read()
        if data:
            hex_data = str(binascii.hexlify(data)).split('\'')[1]
            data_line += hex_data
            byte_count += 1
            # 传感器主动上报-每 0.5s回传 32Byte, 程序以 32Byte作为分割数据的依据
            if byte_count == 32:
                # print(datetime_now() +' | '+ data_line)

                # 运算校验码, 校验数据完整性&传输中是否出错
                hex_check = 0
                for i in range(0, 29):
                    hex_check += int(data_line[2*i:2*i+2], 16)
                    # print(f'i={i}  hex_check={hex_check}, hex={data_line[2*i:2*i+2]}')
                # print(f'校验: {hex_check} === {int(data_line[-4:], 16)}')

                # 数据校验通过 -> 输出
                if hex_check == int(data_line[-4:], 16):
                    # 数据表: 
                    # 00 PM1.0 (CF=1 标准颗粒物 大气环境下 μg/m³)   01 PM2.5 (CF=1 标准颗粒物 大气环境下 μg/m³)
                    # 02 PM10  (CF=1 标准颗粒物 大气环境下 μg/m³)   03 PM1.0 (大气环境下 μg/m³)
                    # 04 PM2.5 (大气环境下 μg/m³)                  05 PM10  (大气环境下 μg/m³)
                    # 06 直径在 0.3μm 以上颗粒物个数 (0.1L空气)     07 直径在 0.5μm 以上颗粒物个数 (0.1L空气)
                    # 08 直径在 1.0μm 以上颗粒物个数 (0.1L空气)     09 直径在 2.5μm 以上颗粒物个数 (0.1L空气)
                    # 10 直径在 5μm   以上颗粒物个数 (0.1L空气)     11 直径在 10μm  以上颗粒物个数 (0.1L空气)
                    for i in range(3, 15):
                        data_list.append(int(data_line[4*i-3:4*i], 16))
                    print(f'{datetime_now()}: 颗粒物浓度(μg/m³): PM1.0: {data_list[3]}  PM2.5: {data_list[4]}  PM10: {data_list[5]} | \
0.1L空气颗粒物(个): 0.3μm: {data_list[6]}  0.5μm: {data_list[7]}  1.0μm: {data_list[8]}  2.5μm: {data_list[9]}  5μm: {data_list[10]}  10μm: {data_list[11]}')

                    if csv_output:
                        csv_write(progame_path, csv_name, data_list)

                # 校验失败 -> 弃用数据
                else:
                    print(f'{datetime_now()} ## 数据校验失败，弃用此次数据（若连续失败请重启程序）')

                # 本轮数据处理完毕，重置变量
                data_line, data_list, byte_count = '', [], 0