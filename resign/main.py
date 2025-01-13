from public import *
import shutil
import os


info = {}
tools_path = os.path.abspath('Tools')

Init = init()
if Init[0] == 'resign':
    info['pkg'], info['jar'], info['keystore'], info['keystore_password'], info['sign_or_not'], \
    info['align'], info['v1'], info['v2'], info['v3'] =\
    Init[1], Init[2], Init[3], Init[4], Init[5], Init[6], Init[7], Init[8], Init[9]

    old_pkg_pame = info['pkg']
    new_pkg_pame = old_pkg_pame.split('.apk')[0] + '_resigned.apk'
    if info['align'] == True:
        align(old_pkg_pame, new_pkg_pame, tools_path)
    else:
        shutil.copyfile(old_pkg_pame, new_pkg_pame)

    if info['sign_or_not'] == True:
        sign(new_pkg_pame, info['jar'], info['keystore'], info['keystore_password'], [info['v1'], info['v2'], info['v3']])
        check_sign(new_pkg_pame, tools_path)
        check_sign_ver(new_pkg_pame, tools_path)

if Init[0] == 'extract':
    info['pkg'], info['jar'], info['keystore'], info['ks_password'], info['key_alias'], info['key_pass'] =\
        Init[1], Init[2], Init[3], Init[4], Init[5], Init[6]

    new_file = f'{info["pkg"]}.apks'
    res = extract(info['pkg'], new_file, info['jar'], info['keystore'], info['ks_password'], info['key_alias'], info['key_pass'])
    print(res)
