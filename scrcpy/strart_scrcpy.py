import os
import time
import subprocess
from gooey import Gooey, GooeyParser


tools_path = os.path.abspath('Tools')
log_path = os.path.abspath(r'temp\log')
screen_path = os.path.abspath(r'temp\screen')
config_path = os.path.abspath(r'Tools\config')
unzip_path = os.path.abspath(r'temp\aab_splits')


@Gooey(program_name="scrcpy投屏", language="chinese")
def init():
    Android_devices = android_dev_info()
    a_d = []
    if Android_devices != 'no device':
        for msg in Android_devices:
            if msg[1] != 'device':
                a_d.append(msg[0] + ' ' + 'disconnect')
            else:
                a_d.append(msg[0])
    else:
        a_d = ['no devices']

    parser = GooeyParser(description='请选择配置')
    machine = parser.add_subparsers(dest='result')
    android = machine.add_parser('android')
    android.add_argument('devices', widget='Dropdown', metavar='设备', choices=a_d, default=a_d[0])
    android.add_argument('max_size', widget='TextField', metavar='max-size', default='960')

    args = parser.parse_args()
    if args.result == 'android':
        devices = args.devices
        max_size = args.max_size
        return [devices, max_size]

def cmd_single_run(order, decode_type='gbk'):
    '''只有一条执行的cmd指令'''
    obj = subprocess.Popen(order, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info, err = obj.communicate()
    result = info.decode(decode_type)
    if err:
        time_YMD = time.strftime('%Y-%m-%d')
        write_err(time_YMD, order, err)
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

def main():
    Init = init()
    usb = Init[0]
    max_size = Init[1]

    cmd_single_run(rf'taskkill /IM {tools_path}/scrcpy.exe /F')
    cmd_single_run(rf'taskkill /IM {tools_path}/adb.exe /F')
    cmd_single_run(rf"{tools_path}/scrcpy -s {usb} --max-size {max_size}")

if __name__ == "__main__":
    main()

