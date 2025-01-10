from utils.utils import *
from setting import *
from device import Android_dev as Android, IOS_dev as IOS


def apk_run(usb, Apk, Time):
    link = Android.Android_device(usb, tools_path)
    i = 0
    for apk in Apk:
        pkg_name = get_pkg_name(apk)
        if link.app_list(pkg_name) != False:
            link.uninstall_pkg(pkg_name)
        link.install_apk(apk)
        print('安装成功，开始运行')
        link.set_enable(pkg_name)
        link.permission(pkg_name)
        link.start_app(pkg_name)
        time.sleep(30)
        if link.check_app(pkg_name) == False:
            time.sleep(3)
        else:
            t = int(Time)*60
            time.sleep(t)
        name = pkg_name + '_' + str(i)
        link.screen(screen_path, name)
        check = link.check_app(pkg_name)
        log_name = log_path + '\\Android\\' + usb + '_' + str(round(time.time())) + '_log.log'
        link.log_out(pkg_name, apk, check, crash_pkg, log_name)
        link.adb_stop(pkg_name)
        time.sleep(1)
        i = i+1

def apks_run(usb, apks, Time):
    link = Android.Android_device(usb, tools_path)
    for apks_path in apks:
        pkg_name = get_apks_name(apks_path)
        if link.app_list(pkg_name) != False:
            link.uninstall_pkg(pkg_name)
        link.install_apks(apks_path)
        print('安装成功，开始运行')
        link.set_enable(pkg_name)
        link.permission(pkg_name)
        link.start_app(pkg_name)
        time.sleep(30)
        if link.check_app(pkg_name) == False:
            time.sleep(3)
        else:
            time.sleep(int(Time) * 60)
        name = pkg_name + '_' + str(round(time.time(), 0))
        link.screen(screen_path, name)
        app_state = link.check_app(pkg_name)
        log_name = log_path + '\\Android\\' + usb + '_' + str(round(time.time())) + '_log.log'
        link.log_out(pkg_name, apks_path, app_state, crash_pkg, log_name)
        link.adb_stop(pkg_name)
        time.sleep(1)


def ipa_run(usb, ipas, enable_type, Time):
    link = IOS.IOS_device(usb)
    print(f'{usb} 是否越狱: ', link.jailbreak())
    for ipa in ipas:
        apps = link.get_apps()
        bundle_id = get_bundle_id(ipa)
        for app in apps:
            if bundle_id == app['CFBundleIdentifier']:
                link.uninstall_app(bundle_id)
                time.sleep(0.5)
        link.install_app(ipa)
        link.set_enable(bundle_id, enable_type)
        link.start_app(bundle_id)
        time.sleep(30)
        app_msg = link.foreground_app()
        if app_msg[1] == bundle_id:
            print(f'{bundle_id} 30s试运行正常')
        else:
            print(f'{bundle_id} 试运行失败')
            link.screen(screen_path)
            return
        link.stop_app(bundle_id)
        link.start_app(bundle_id)
        time.sleep(int(Time) * 60)
        if app_msg[1] == bundle_id:
            print(f'{bundle_id} {Time}min运行正常', end='\n\n')
        else:
            print(f'{bundle_id} {Time}min内运行异常闪退', end='\n\n')
        log_name = log_path + '\\ios\\' + usb + '_' + str(round(time.time())) + '_logXAYY.log'
        link.pull_log(bundle_id, log_name)
        link.screen(screen_path)
        link.stop_app(bundle_id)


