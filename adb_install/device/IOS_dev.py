import time
import tidevice
import os
from tidevice._sync import Sync



def get_size(pkg):
    size = os.path.getsize(pkg)
    return size

class IOS_device():
    def __init__(self, usb):
        self.ios_d = tidevice.Device(usb)
        conn = self.ios_d.start_service("com.apple.afc2")
        self.conn = Sync(conn)

    def ios_device_info(self):
        Device_info = self.ios_d.device_info()
        return Device_info.get('UniqueDeviceID'), Device_info.get('DeviceName'), Device_info.get('ProductVersion')

    def app_info(self, bundle_id):
        info = self.ios_d.installation.lookup(bundle_id)
        self.package = info.get("CFBundleIdentifier", "")
        self.name = info.get("CFBundleDisplayName", "")
        self.path = info.get("Container", "")
        self.version = info.get("CFBundleShortVersionString", "")
        self.browse = bool(info.get("UIFileSharingEnabled", False))

    def jailbreak(self):
        try:
            conn = self.ios_d.start_service("com.apple.afc2")
            self.conn = Sync(conn)
            self.jailbreak = self.conn.exists('/private/var/mobile')
        except:
            self.jailbreak = False
        return self.jailbreak

    def get_apps(self):
        apps = self.ios_d.connect_instruments().app_list()
        return apps

    def install_app(self, ipa_path):
        size = str(round((get_size(ipa_path) / 1024), 2))
        print(f"正在安装{ipa_path}\r文件大小：{size}MB")
        self.ios_d.app_install(ipa_path)

    def uninstall_app(self, bundle_id):
        self.ios_d.app_uninstall(bundle_id)

    def start_app(self, bundle_id):
        self.ios_d.app_start(bundle_id)

    def stop_app(self, bundle_id):
        self.ios_d.app_stop(bundle_id)

    def ls_Documents(self, bundle_id):
        self.app_info(bundle_id)
        if self.jailbreak == False:
            return self.ios_d.app_sync(bundle_id).listdir('/Documents')
        else:
            return self.conn.listdir(f'{self.path}/Documents')

    def set_enable(self, bundle_id, enable_type):
        '''设置enable'''
        ipash_enable = '1111111111111111111111111111111111111111111'
        sdk_enable = '0000000000000000090900009000000000000'
        self.app_info(bundle_id)
        if enable_type == 'shell':
            enable_type = 'ipash_enable'
            enable = ipash_enable
        elif enable_type == 'sdk':
            enable_type = 'enable'
            enable = sdk_enable
        else:
            return print('未知类型的enable，请选择“ipash_enable”或“sdk_enable”')

        if not self.ios_d.app_sync(bundle_id).exists(f'/Documents/{enable_type}.log'):
            if self.jailbreak == False:
                if self.browse == False:  # 包体无浏览权限
                    print('UIFileSharingEnabled = False, 该app无浏览权限')
                    print('未设置enable')
                    return
                self.ios_d.app_sync(bundle_id).push_content(
                    f'/Documents/{enable_type}.log', enable.encode('utf-8'))
            else:
                self.conn.push_content(
                    f'{self.path}/Documents/{enable_type}.log', enable.encode('utf-8'))

    def foreground_app(self):
        processes = self.ios_d.connect_instruments().app_running_processes()
        app_name = path_code = bundle_id = ''
        for p in processes:
            if not p.get('isApplication', False) or not p.get('foregroundRunning', False):
                continue
            app_name = p['name']
            path_code = p['realAppName'].split('/')[5]
            break
        apps = self.get_apps()
        for app in apps:
            try:
                app_path_code = app['BundlePath'].split('/')[6]
                if app['DisplayName'] == app_name or app['ExecutableName'] == app_name and app_path_code == path_code:
                    bundle_id = app['CFBundleIdentifier']
                    break
            except:
                if app['DisplayName'] == app_name:
                    bundle_id = app['CFBundleIdentifier']
                    break
        if app_name == bundle_id == '':
            return False
        return app_name, bundle_id

    def screen(self, file_path):
        Time = str(time.time()).split('.')[0]
        bundle_id = self.foreground_app()[0]
        name = Time + '_' + bundle_id
        file_name = file_path + '\\' + name + '.jpg'
        self.ios_d.screenshot().convert("RGB").save(file_name)

    def pull_log(self, bundle_id, out_path):
        self.app_info(bundle_id)
        if self.jailbreak == False:
            if self.ios_d.app_sync(bundle_id).exists(f'/Documents/logXAYY.log'):
                return False
            else:
                self.conn.pull(f'/Documents/logXAYY.log', out_path)
        else:
            if self.ios_d.app_sync(bundle_id).exists(f'{self.path}/Documents/logXAYY.log'):
                return False
            else:
                self.conn.pull(f'{self.path}/Documents/logXAYY.log', out_path)

    def cat_log(self, bundle_id):
        self.app_info(bundle_id)
        if self.jailbreak == False:
            if self.ios_d.app_sync(bundle_id).exists(f'/Documents/logXAYY.log'):
                return False
            else:
                return self.conn.iter_content(f'/Documents/logXAYY.log')
        else:
            if self.ios_d.app_sync(bundle_id).exists(f'{self.path}/Documents/logXAYY.log'):
                return False
            else:
                return self.conn.iter_content(f'{self.path}/Documents/logXAYY.log')





