import os
import re
import pathlib
import subprocess
import time
from setting import *
from device.IOS_dev import IOS_device
from device.Android_dev import Android_device
from gooey import Gooey, GooeyParser
from tidevice._ipautil import IPAReader

mobile_phone_emulator = {
    '5555': '127.0.0.1:5555',
    '5556': '127.0.0.1:5556',
    'MuMu': '127.0.0.1:7555',
    'MuMu12': '127.0.0.1:16384',
    '逍遥': '127.0.0.1:21503',
    '夜神': '127.0.0.1:62001',
    '夜神64': '127.0.0.1:62025',
    '手机模拟大师': '127.0.0.1:9974',
    '5554': 'emulator-5554',
}

@Gooey(program_name="兼容自动化（apk/aab/ipa）", language="chinese", default_size=(1200, 600))
def init():
    Android_devices = android_dev_info()
    IOS_devices = ios_dev_info()
    MPE_devices = mobile_phone_emulator
    a_d, i_d, M_d = [], [], []
    if Android_devices != 'no device':
        for msg in Android_devices:
            if msg[1] != 'device':
                a_d.append(msg[0] + ' ' + 'disconnect')
            else:
                a_d.append(msg[0])
    else:
        a_d = ['no devices']
    if IOS_devices != 'no ios device':
        for msg in IOS_devices:
            i_d.append(f'{msg[0]}  Name: {msg[1]}  Ver: {msg[2]}')
    else:
        i_d = ['no devices']
    for MPE_dev in MPE_devices.keys():
        M_d.append(MPE_dev)

    min = ['1', '3', '5', '10', '15', '30']
    parser = GooeyParser(description='请选择配置')
    machine = parser.add_subparsers(dest='result')
    android = machine.add_parser('android')
    android.add_argument('devices', widget='Dropdown', metavar='设备', choices=a_d, default=a_d[0])
    android.add_argument('time', widget='Dropdown', metavar='运行时间', choices=min, default='3')
    android.add_argument('path', widget="DirChooser", metavar='安装包文件夹')
    android.add_argument('clean', widget='Dropdown', metavar='是否卸载已验证安装包', choices=['是', '否'], default='否')

    ios = machine.add_parser('ios')
    ios.add_argument('devices', widget='Dropdown', metavar='设备', choices=i_d, default=i_d[0])
    ios.add_argument('time', widget='Dropdown', metavar='运行时间', choices=min, default='3')
    ios.add_argument('enable', widget='Dropdown', metavar='enable类型', choices=['sdk', 'shell'], default='sdk')
    ios.add_argument('path', widget="DirChooser", metavar='安装包文件夹')
    ios.add_argument('clean', widget='Dropdown', metavar='是否卸载已验证安装包', choices=['是', '否'], default='否')

    MPE = machine.add_parser('安卓模拟器')
    MPE.add_argument('devices', widget='Dropdown', metavar='设备', choices=M_d, default=M_d[0])
    MPE.add_argument('time', widget='Dropdown', metavar='运行时间', choices=min, default='3')
    MPE.add_argument('path', widget="DirChooser", metavar='安装包文件夹')
    MPE.add_argument('clean', widget='Dropdown', metavar='是否卸载已验证安装包', choices=['是', '否'], default='否')

    args = parser.parse_args()
    if args.result == 'android':
        OS = 'android'
        Devices = args.devices
        Path = args.path
        Time = args.time
        Clean = args.clean
        return [OS, Devices, Path, Time, Clean]
    if args.result == 'ios':
        OS = 'ios'
        Devices = args.devices
        Path = args.path
        Time = args.time
        Clean = args.clean
        Enable = args.enable
        return [OS, Devices, Path, Time, Clean, Enable]
    if args.result == '安卓模拟器':
        OS = 'MPE'
        Devices = args.devices
        Path = args.path
        Time = args.time
        Clean = args.clean
        return [OS, Devices, Path, Time, Clean]

def devices():
    order = f'{tools_path}\\adb.exe devices'
    check = cmd_single_run(order, 'gbk').split('\r\n')
    if len(check) == 3:
        return 'no device'
    elif len(check) < 3:
        check = cmd_single_run(order, 'gbk').split('\r\n')
    try:
        check.pop(-1)
        check.pop(-1)
        check.pop(0)
        return check
    except:
        return 'no device'

def android_dev_info():
    Devices = devices()
    android_devices = []
    if Devices == 'no device':
        return 'no device'
    for device in Devices:
        android_devices.append(device.split('\t'))
    return android_devices

def ios_devices():
    order = 'tidevice list'
    check = cmd_single_run(order, 'utf-8').split('\n')
    time.sleep(2)
    if len(check) == 2:
        return 'no ios device'
    check.pop(-1)
    check.pop(0)
    return check

def ios_dev_info():
    ios_datas = ios_devices()
    if ios_datas == 'no ios device':
        return 'no ios device'
    DeviceIds, ios_info = [], []
    for ios_data in ios_datas:
        DeviceIds.append(ios_data.split(' ')[0])
    for DeviceId in DeviceIds:
        ios = IOS_device(DeviceId)
        ios_info.append(ios.ios_device_info())
    return ios_info

def adb_connect(device):
    comm = rf'{tools_path}\adb.exe connect {device}'
    cmd_single_run(comm)

def get_size(pkg):
    size = os.path.getsize(pkg)
    return size

def cmd_single_run(order, decode_type='gbk'):
    '''只有一条执行的cmd指令'''
    obj = subprocess.Popen(order, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info, err = obj.communicate()
    result = info.decode(decode_type)
    if err:
        time_YMD = time.strftime('%Y-%m-%d')
        write_err(time_YMD, order, err)
    return result

def cmd_orders_run(orders, decode_type='gbk'):
    '''只有多条执行的cmd指令'''
    obj = subprocess.Popen('cmd', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for order in orders:
        obj.stdin.write(order.encode('utf-8'))
    info, err = obj.communicate()
    result = info.decode(decode_type)
    if err:
        time_YMD = time.strftime('%Y-%m-%d')
        write_err(time_YMD, orders, err)
    return result

def write_err(time_YMD, order, err):
    file = open(rf'{log_path}\{time_YMD}_err.txt', 'a', encoding='utf-8')
    file.write(time.strftime('%H-%M-%S'))
    file.write('\n')
    file.write(str(order))
    file.write('\n')
    file.write(err.decode('gbk'))
    file.write('=' * 80 + '\n\n')
    file.close()

def check_endswith(path):
    apks, apk, aab, ipa = [], [], [], []
    for pkg in pathlib.Path(path).glob("**/*"):
        check_aab = pkg.name.endswith('.aab')
        check_apks = pkg.name.endswith('.apks')
        check_apk = pkg.name.endswith('.apk')
        check_ipa = pkg.name.endswith('.ipa')
        if check_aab == True:
            aab.append(str(pkg))
        if check_apks == True:
            apks.append(str(pkg))
        if check_apk == True:
            apk.append(str(pkg))
        if check_ipa == True:
            ipa.append(str(pkg))
    return aab, apks, apk, ipa

def get_pkg_name(pkg):
    order = rf'{tools_path}\aapt2.exe dump badging {pkg}'
    res = cmd_single_run(order, decode_type='utf-8')
    pkg_name = str(re.search("package: name='.*'", res).group()).split("'")[1]
    return pkg_name

def get_apks_name(apks):
    rm = rf'rd /s /q {unzip_path}'
    order = fr'{tools_path}\unzip -od {unzip_path} {apks}'
    cmd_single_run(rm)
    cmd_single_run(order)
    time.sleep(2)
    apk = []
    for i in pathlib.Path(unzip_path).glob("**/*"):
        check_apk = i.name.endswith('.apk')
        if check_apk == True:
            apk.append(str(i))
    res = os.popen(fr'{tools_path}\aapt2.exe dump badging {apk[0]}').readline()
    pkg_name = str(re.search("package: name='.*'", res).group()).split("'")[1]
    time.sleep(2)
    cmd_single_run(rm)
    return pkg_name

def get_bundle_id(ipa_file):
    ipa_info = IPAReader(ipa_file)
    bundle_id = ipa_info.get_bundle_id()
    return bundle_id

def extract(ori_file, new_file):
    '''aab提取'''
    print(f'提取aab文件{ori_file}')
    order = f'java -jar {tools_path}\\bundletool.jar build-apks --bundle={ori_file} --output={new_file}.apks --overwrite --ks="{tools_path}\\test.keystore" --ks-pass=pass:123456 --ks-key-alias=test --key-pass=pass:123456'
    cmd_single_run(order)

def ext_aab(aab):
    for x in range(len(aab)):
        name = str(aab[x])
        extract(aab[x], name)





