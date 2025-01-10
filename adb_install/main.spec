# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py', 'task.py', 'setting.py', r'utils\__init__.py', r'utils\utils.py', r'device\__init__.py', r'device\Android_dev.py', r'device\IOS_dev.py'],
    pathex=[r'D:\code\python\All_project\venv\Lib\site-packages', 'D:\code\python\All_project\venv\Lib\site-packages\paddle\libs'],
    binaries=[(r'D:\code\python\All_project\venv\Lib\site-packages\paddle\libs', r'.')],
    datas=[],
    hiddenimports=['gooey', 'tidevice'],
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
     a.scripts,
     [],
     exclude_binaries=True,
     name='main',
     debug=False,
     bootloader_ignore_signals=False,
     strip=False,
     upx=True,
     console=False)
	 
coll = COLLECT(exe,
     a.binaries,
     a.zipfiles,
     a.datas,
     strip=False,
     upx=True,
     upx_exclude=[],
     name='main')
