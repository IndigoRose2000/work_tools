import subprocess
import time
import re
from gooey import Gooey, GooeyParser




@Gooey(program_name="重签名&提取apks", language="chinese", default_size=(600, 700))
def init():
    parser = GooeyParser(description="resign")
    model = parser.add_subparsers(dest='result')
    sign = model.add_parser('重签名')
    sign.add_argument('pkg', widget="TextField", metavar="包")
    sign.add_argument('jar', widget="TextField", metavar=r"jar", default=r'Tools\apksigner.jar')
    sign.add_argument('ks', widget="TextField", metavar=r"keystore", default=r'Tools\test.keystore')
    sign.add_argument('ks_password', widget="TextField", metavar=r"keystore_password", default=r'123456')
    sign.add_argument('-e', '--sign_or_not', action='store_true', metavar="是否重签名", widget='CheckBox', default=True)
    sign.add_argument('-d', '--align', action='store_true', metavar="4k对齐", widget='CheckBox', default=True)
    sign.add_argument('-a', '--v1_signing', action='store_true', widget='CheckBox', default=True)
    sign.add_argument('-b', '--v2_signing', action='store_true', widget='CheckBox', default=True)
    sign.add_argument('-c', '--v3_signing', action='store_true', widget='CheckBox', default=True)
    extract = model.add_parser('提取apks')
    extract.add_argument('pkg', widget="TextField", metavar="aab包")
    extract.add_argument('jar', widget="TextField", metavar=r"jar", default=r'Tools\bundletool.jar')
    extract.add_argument('ks', widget="TextField", metavar=r"keystore", default=r'Tools\test.keystore')
    extract.add_argument('ks_password', widget="TextField", metavar=r"keystore_password", default=r'123456')
    extract.add_argument('key_alias', widget="TextField", metavar=r"key_alias", default=r'test')
    extract.add_argument('key_pass', widget="TextField", metavar=r"key_pass", default=r'123456')

    args = parser.parse_args()
    if args.result == '重签名':
        model = 'resign'
        pkg = args.pkg
        jar = args.jar
        ks = args.ks
        ks_password = args.ks_password
        sign_or_not = args.sign_or_not
        align = args.align
        v1 = args.v1_signing
        v2 = args.v2_signing
        v3 = args.v3_signing
        return [model, pkg, jar, ks, ks_password, sign_or_not, align, v1, v2, v3]
    if args.result == '提取apks':
        model = 'extract'
        pkg = args.pkg
        jar = args.jar
        ks = args.ks
        ks_password = args.ks_password
        key_alias = args.key_alias
        key_pass = args.key_pass
        return [model, pkg, jar, ks, ks_password, key_alias, key_pass]


def cmd_single_run(order):
    '''只有一条执行的cmd指令'''
    obj = subprocess.Popen(order, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info, err = obj.communicate()
    result = info.decode('gbk')
    return result

def extract(ori_file, new_file, jar, keystore_path, ks_pass, key_alias, key_pass):
    '''aab提取'''
    order = rf'java -jar {jar} build-apks --bundle={ori_file} --output={new_file} --overwrite --ks="{keystore_path}" --ks-pass=pass:{ks_pass} --ks-key-alias={key_alias} --key-pass=pass:{key_pass}'
    res = cmd_single_run(order)
    return res

def align(ori_file, new_file, tools_path):
    '''4k对齐'''
    time_HMS = time.strftime('%H:%M:%S')
    order = rf'{tools_path}\zipalign.exe -p -f -v 4 {ori_file} {new_file}'
    info = cmd_single_run(order)
    if re.search(r'Verification succesful', info) != None:
        print('4k对齐: '+new_file+' '+time_HMS)
    else:
        print('4k对齐失败: '+new_file+' '+time_HMS)
    return f'{new_file}_resign.apk'


def sign(pkg, jar, keystore, keystore_password, sign_version):
    '''重签名'''
    order = rf'java -jar {jar} sign --ks {keystore} --v1-signing-enabled {str(sign_version[0]).lower()} --v2-signing-enabled {str(sign_version[1]).lower()} --v3-signing-enabled {str(sign_version[2]).lower()} {pkg}'
    obj = subprocess.Popen(order, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    obj.stdin.write(keystore_password.encode('utf-8'))
    obj.stdin.write('\n'.encode('utf-8'))
    info, err = obj.communicate()
    result = info.decode('gbk')
    print(result, end='')
    return result

def check_sign(pkg, tools_path):
    '''检查是否重签名'''
    order = rf'{tools_path}\jarsigner.exe -verify {pkg}'
    obj = subprocess.Popen(order, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    info, err = obj.communicate()
    result = info.decode('gbk')
    if re.search(r'jar 已验证', result) != None:
        print('已验证签名 ' + str(pkg))
    elif re.search(r'jar 未签名', result) != None:
        print('未签名' + str(pkg))
    else:
        print('（提示中出现弱算法签名时，可以忽略提示）')
        print(result, end='')

def check_sign_ver(pkg, tools_path):
    '''检查重签名的等级'''
    order = rf'java -jar {tools_path}\apksigner.jar verify -v {pkg}'
    obj = subprocess.Popen(order, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info, err = obj.communicate()
    result = info.decode('gbk')
    print(result, end='')
    return result






