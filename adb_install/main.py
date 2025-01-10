from task import *
from setting import *
from device import Android_dev as Android, IOS_dev as IOS

Init = init()
device_os = Init[0]
path = Init[2]
Time = Init[3]
clean = Init[4]


def main():
    aab, apks, apk, ipa = check_endswith(path)
    if device_os == 'android':
        usb = Init[1].split('\t')[0]
        an_dev = Android.Android_device(usb, tools_path)
        ext_aab(aab)
        aab, apks, apk, ipa = check_endswith(path)
        apk_run(usb, apk, Time)
        apks_run(usb, apks, Time)
        if clean == '是':
            for a in apk:
                pkg_name = get_pkg_name(a)
                an_dev.uninstall_pkg(pkg_name)
            for a in apks:
                pkg_name = get_apks_name(a)
                an_dev.uninstall_pkg(pkg_name)
            print('Android 测试应用已删除')

    if device_os == 'ios':
        usb = Init[1].split(' ')[0]
        enable_type = Init[5]
        ios_dev = IOS.IOS_device(usb)
        ipa_run(usb, ipa, enable_type, Time)
        if clean == '是':
            for ipa_single in ipa:
                bundle_id = get_bundle_id(ipa_single)
                ios_dev.uninstall_app(bundle_id)
            print('IOS 测试应用已删除')

    if device_os == 'MPE':
        MPE_name = Init[1].split('\t')[0]
        usb = mobile_phone_emulator.get(MPE_name)
        adb_connect(usb)
        an_dev = Android.Android_device(usb, tools_path)
        aab, apks, apk, ipa = check_endswith(path)
        ext_aab(aab)
        apk_run(usb, apk, Time)
        apks_run(usb, apks, Time)
        if clean == '是':
            for a in apk:
                pkg_name = get_pkg_name(a)
                an_dev.uninstall_pkg(pkg_name)
            for a in apks:
                pkg_name = get_apks_name(a)
                an_dev.uninstall_pkg(pkg_name)
            print('Android 测试应用已删除')

if __name__ == '__main__':
    main()

