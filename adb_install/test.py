# from public import phone_link
#
# link = phone_link('18fdf3fd')
#
# link.install_apk(r'D:\shell\need_shell\Tools.apk')

# import minidevice

# d = 'zpa66l5lyhf6lj5t'


# from pyplist import XMLParser as plt
#
#
#
# # 读取 XML 格式的 plist 文件
# f = open(r'D:\sdk\7.2.2.18249\demo\Info.plist', 'rb').read()
# a = plt.parseFile(r'D:\sdk\7.2.2.18249\demo\Info.plist')
#
# print(a)

# # 修改配置并写回文件
# config['key'] = 'value'
# with open('config.plist', 'wb') as f:
#     plist.dump(config, f)

# ===========================================================================
# import time
# import zipfile
# import shutil
#
# import pyautogui
# import pygetwindow as gw
# import autoit

# window = gw.getActiveWindow()
# windows = gw.getAllWindows()
# print(windows)
# print(window)
#
#
# autoit.run('E:\VOWSoft iPod Software\plist Editor Pro\plistEditor.exe')
# plist = gw.getWindowsWithTitle('D:\shell\IOS_Shell\ipa_sign\Info.plist')
# print(gw.getAllTitles())
# time.sleep(0.5)
# print(plist)
# p = plist[0]
# print(p)
# print(p.title)
# p.activate()
# time.sleep(0.5)
# print(p.isActive)


# ===============================================================================
# import time
# import zipfile
# import shutil
# import autoit
# from autoit import properties
# import pywinauto
# from pywinauto.application import Application

# print(autoit.win_get_text('D:\shell\IOS_Shell\ipa_sign\Info.plist', 'XML View'))
# a = pywinauto.Application('uia')
# plist = pywinauto.Application('uia').connect(title='D:\shell\IOS_Shell\ipa_sign\Info.plist')
# print(plist.window_text())
# print(pyautogui.Window(title='D:\shell\IOS_Shell\ipa_sign\Info.plist').isActive())


# autoit.run('E:\VOWSoft iPod Software\plist Editor Pro\plistEditor.exe')
# autoit.win_wait_active('plist Editor Pro for Windows', 3)
# print(autoit.win_get_handle('plist Editor Pro for Windows'))
# print(autoit.win_get_handle())
# autoit.win_menu_select_item('plist Editor Pro for Windows', '', 'File', 'Open')
# autoit.control_click('plist Editor Pro for Windows', '', 'File', 'Open')
# print(autoit.control_get_text)
# autoit.control_click('D:\shell\IOS_Shell\ipa_sign\Info.plist', '', 'File', 'Open')

# time.sleep(1)
# autoit.win_close('plist Editor Pro for Windows')

# =============================================================================
# import time
# import os
# import zipfile
# import shutil
# import autoit
# from autoit import properties
# import pywinauto
# from pywinauto import Application
#
# import win32gui

# hwnd_title = {}
#
#
# def get_all_hwnd(hwnd, mouse):
#     if (win32gui.IsWindow(hwnd)
#             and win32gui.IsWindowEnabled(hwnd)
#             and win32gui.IsWindowVisible(hwnd)):
#         hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
#
#
# win32gui.EnumWindows(get_all_hwnd, 0)
# for h, t in hwnd_title.items():
#     if t:
#         print(h, t)
# if __name__ == '__main__':
#     pass

# print(win32gui.FindWindow('wxWindowNR', 'D:\shell\IOS_Shell\ipa_sign\Info.plist'))
# print(win32gui.GetMenu(1775702))
# print(win32gui.GetSubMenu(4294935298, 0))


# os.popen('D:\shell\IOS_Shell\ipa_sign\Info.plist')
# time.sleep(2)
# plist = gw.getWindowsWithTitle('D:\shell\IOS_Shell\ipa_sign\Info.plist')
# time.sleep(1)
# p = plist[0]
# p.activate()
# # print(autoit.win_get_text('D:\shell\IOS_Shell\ipa_sign\Info.plist'))
# autoit.control_send('D:\shell\IOS_Shell\ipa_sign\Info.plist', 'XML View', '^a')

# app = Application(backend='uia')
# app.connect(process=1324)
# d = app.window()
# d.print_control_identifiers()
# print(app.is64bit())

# ============================================================================
# a = 'asdfzcvdfaermfghdzcvdaadasdqeasd'
#
# b = a.replace('12', 'ab')
# print(a)
# print(b)

# from gooey import Gooey, GooeyParser
#
# @Gooey(program_name="自动安装运行脚本（apk、aab）", language="chinese", default_size=(1100, 600))
# def init():
#     parser = GooeyParser(description='请选择配置')
#     machine = parser.add_subparsers(dest='result')
#     android = machine.add_parser('android')
#     android.add_argument('devices', widget='Dropdown', metavar='设备', choices=['0', '1'], default='0')
#
#     args = parser.parse_args()
#     if args.result == 'android':
#         OS = 'android'
#         Devices = args.devices
#
# init()


# import os
# import time
#
# print(type(time.time()))

# print(os.popen('adb -s b7b2e062 shell am start com.tencent.sdk/com.tencent.foogame.MainActivity', 'r').read())

# def start_app(usb, pkg_name):
#     # 打开app
#     res = os.popen(f'adb -s {usb} shell "dumpsys package {pkg_name}|grep -A 1 android.intent.action.MAIN:"', 'r').read()
#     sstr = []
#     print(res)
#     for msg in res.split('\n')[2].split(' '):
#         if msg != '':
#             sstr.append(msg)
#     print(sstr)
#     name_act = sstr[1]
#     start = os.popen(f'adb -s {usb} shell am start {name_act}', 'r').read()
#     return start
#
# start_app('b7b2e062', 'com.tencent.sdk')

from public import *

usb = 'b7b2e062'
android = Android_device(usb)
res = android.start_app_test('com.tencent.sdk')
print(res)
