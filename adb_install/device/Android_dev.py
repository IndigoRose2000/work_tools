import os
import re
import time
import subprocess
from setting import *


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
    file.write(str(order))
    file.write('\n')
    file.write(err.decode('gbk'))
    file.write('=' * 80 + '\n\n')
    file.close()

class Android_device():
    def __init__(self, usb, tools_path):
        self.Usb = usb
        self.tools_path = tools_path
        self.adb_exe = tools_path + '\\adb.exe'
        self.adb_shell = self.adb_exe + ' -s ' + self.Usb + ' shell '

    def ver(self):
        ver = cmd_single_run(f'{self.adb_shell} getprop ro.build.version.release')
        if re.search('.', ver):
            Ver = int(ver.split('.')[0])
        else:
            Ver = int(ver)
        return Ver

    def set_enable(self, pkg_name):
        Ver = self.ver()
        adv_ver_ord = open(f'{config_path}/adv_ver_template.txt').readlines()
        create_txt = open(f'{config_path}/adv_ver.txt', 'w', encoding='utf-8')
        for adv in adv_ver_ord:
            adv_order = adv.replace('pkg_name', pkg_name)
            create_txt.write(adv_order)
        create_txt.close()
        low_ver = f'{self.adb_shell} < {config_path}/low_ver.txt'
        adv_ver = f'{self.adb_shell} < {config_path}/adv_ver.txt'

        lowest_ver = 'echo 0000000000000000090910009000000000000 > /sdcard/sdk/enable.log'
        if Ver >= 9:
            cmd_single_run(adv_ver)
        elif Ver <= 5:
            cmd_single_run(lowest_ver)
        else:
            cmd_single_run(low_ver)

    def install_apk(self, pkg):
        usb = self.Usb
        Ver = self.ver()
        size = str(round((get_size(pkg) / 1024), 2))
        print(f"正在安装{pkg}\r文件大小：{size}MB")
        order = f'{self.adb_exe} -s {usb} install -g {pkg}'
        order_4 = f'{self.adb_exe} -s {usb} install {pkg}'
        if Ver <= 6:
            res = cmd_single_run(order_4)
        else:
            res = cmd_single_run(order)
        return res

    def install_apks(self, apks):
        usb = self.Usb
        tools_path = self.tools_path
        order = f'java -jar {tools_path}\\bundletool.jar install-apks --adb {tools_path}\\adb.exe --apks {apks} --device-id {usb}'
        size = str(round((get_size(apks) / 1024), 2))
        print(f"正在安装{apks}\r文件大小：{size}MB")
        res = cmd_single_run(order, 'gbk')
        return res

    def uninstall_pkg(self, pkg):
        usb = self.Usb
        res = cmd_single_run(f'{self.adb_exe} -s {usb} uninstall {pkg}')
        return res

    def app_list(self, pkg):
        res = cmd_single_run(f'{self.adb_shell} pm list package')
        if not re.search(pkg, res):
            return False

    def start_app(self, pkg_name):
        # 打开app
        Ver = self.ver()
        try:
            order = f'{self.adb_shell} "dumpsys package {pkg_name}|grep -A 1 android.intent.action.MAIN:"'
            res = os.popen(order).read()
            # res = cmd_single_run(order)
            if res == '':
                return print('未找到对应包名，请确认是否安装')
            name_act, res_act, res_msg = [], [], []
            if Ver <= 5:
                res_msg = res.split('\n')[2].split(' ')
            else:
                res_msg = res.split('\n')[1].split(' ')
            for msg in res_msg:
                if msg != '':
                    res_act.append(msg)
            name_act = res_act[1]
            start = cmd_single_run(f'{self.adb_shell} am start {name_act}')
            return start
        except:
            print(f'启动 {pkg_name} 失败')
            return

    def adb_stop(self, pkg):
        # 关闭app
        cmd_single_run(f'{self.adb_shell} am force-stop {pkg}')

    def check_app(self, pkg):
        # 检测app是否闪退（包含检测前台应用、进程、截图）
        usb = self.Usb
        order1 = cmd_single_run(f'{self.adb_shell} "dumpsys window | grep mCurrentFocus"')
        order2 = cmd_single_run(f'{self.adb_shell} "ps | grep {pkg}"')
        time_HMS = time.strftime('%H:%M:%S')

        a, b = 1, 1
        if re.search(pkg, order1) is not None:
            print(usb + ' ' + pkg + '在前台 ' + time_HMS)
        else:
            print(usb + ' ' + pkg + '不在前台 请检查是否有弹窗，或是已经闪退 ' + time_HMS)
            a = 0
        if re.search(pkg, order2) is not None:
            print(usb + ' ' + pkg + '进程存活 ' + time_HMS + '\n')
        else:
            print(usb + ' ' + pkg + '进程死亡 发生闪退 ' + time_HMS + '\n')
            b = 0
        if a == 0 or b == 0:
            return False
        return True

    def screen(self, out_path, name):
        '''截图'''
        usb = self.Usb
        a = f'{self.adb_shell} "screencap -p /sdcard/{name}.png"'
        b = f'{self.adb_exe} -s {usb} pull "/sdcard/{name}.png" {out_path}'
        c = f'{self.adb_shell} "rm -rf /sdcard/{name}.png"'
        d = [a, b, c]
        cmd_orders_run(d)

    def get_log(self, pkg):
        usb = self.Usb
        try:
            ver = self.ver()
            if ver < 9:
                order = f'{self.adb_shell} "cat /sdcard/sdk/log.log"'
            else:
                order = f'{self.adb_shell} "cat /sdcard/Android/data/{pkg}/files/log.log"'
            res = cmd_single_run(order)
            if re.search('No such file or directory', res):
                if ver >= 9:
                    res = cmd_single_run(f'{self.adb_shell} "cat /sdcard/sdk/log.log"')
                    if re.search('No such file or directory', res):
                        print(f'{usb} 未生成log.log')
                        return
                else:
                    print(f'{usb} 未生成log.log')
                    return
            openid = re.search('user_info->uin_.uin_str_:.*', res).group().split('\n')[0]
            # time_YMD = time.strftime('%Y-%m-%d')
            # file = open(rf'{log_path}\{time_YMD}_log.log.txt', 'a', encoding='utf-8')
            # file.write(self.Usb)
            # file.write('\n')
            # file.write(res)
            # file.write('=' * 20 + '\n\n')
            # file.close()
            return openid
        except:
            print('获取log.log失败，未生成log.log或未接入sdk')
            return False

    def get_shell_log(self, pkg):
        try:
            ver = self.ver()
            if ver <= 9:
                order = f'{self.adb_shell} "cat /sdcard/sdk/shell.log | grep OpenID"'
            else:
                order = f'{self.adb_shell} "cat /sdcard/Android/data/{pkg}/files/shell.log | grep OpenID"'
            res = cmd_single_run(order)
            if re.search('No such file or directory', res):
                return '未生成shell.log'
            else:
                shell_log = res
            log = shell_log.split('\n')[-2]
            shell_openid = re.search('OpenID:.*,', log).group()
            return shell_openid
        except:
            print('获取shell.log失败')
            return False

    def pull_log(self, pkg, out_path):
        usb = self.Usb
        try:
            ver = self.ver()
            if ver < 9:
                order = f'{self.adb_exe} -s {usb} pull /sdcard/sdk/log.log {out_path}'
            else:
                order = f'{self.adb_exe} -s {usb} pull /sdcard/Android/data/{pkg}/files/log.log {out_path}'
            res = cmd_single_run(order)
            if re.search('No such file or directory', res):
                if ver >= 9:
                    res = cmd_single_run(f'{self.adb_exe} -s {usb} pull /sdcard/sdk/log.log {out_path}')
                    if re.search('No such file or directory', res):
                        print(f'{usb} 未生成log.log')
                        return False
                else:
                    print(f'{usb} 未生成log.log')
                    return False
        except:
            print('获取log.log失败，未生成log.log或未接入sdk')
            return False

    def log_out(self, pkg, apk, alive_or_not, crash_pkg, out_path):
        openid = self.get_log(pkg)
        shell_openid = self.get_shell_log(pkg)
        if openid == False:
            openid = '无openid'
        if shell_openid == False:
            shell_openid = '无shell_openid'
        self.pull_log(pkg, out_path)
        time_YMD = time.strftime('%Y-%m-%d')
        file = open(rf'{log_path}\{time_YMD}.txt', 'a', encoding='utf-8')
        if alive_or_not == True:
            file.write(f'>>>{apk}\n{pkg}未闪退，运行正常\n{openid}\n{shell_openid}\n\n')
        else:
            for i in range(len(crash_pkg)):
                if crash_pkg == pkg[i]:
                    file.write(f'>>>{apk}\n{pkg}发生预期内闪退\n{openid}\n{shell_openid}\n\n')
                    break
                else:
                    continue
            file.write(f'>>>{apk}\n{pkg}发生闪退\n{openid}\n{shell_openid}\n\n')
        file.close()

    def permission(self, pkg):
        '''给权限'''
        permission = ['android.permission.WRITE_EXTERNAL_STORAGE', 'android.permission.READ_EXTERNAL_STORAGE']
        orders = []
        for perm in permission:
            order = f'{self.adb_shell} pm grant {pkg} {perm}\n'
            orders.append(order)
        cmd_orders_run(orders)


