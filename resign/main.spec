# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py', 'public.py'],
    pathex=[r'D:\code\python\All_project\venv\Lib\site-packages', 'D:\code\python\All_project\venv\Lib\site-packages\paddle\libs'],
    binaries=[(r'D:\code\python\All_project\venv\Lib\site-packages\paddle\libs', r'.')],
    datas=[],
    hiddenimports=['gooey', 'openpyxl'],
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
     console=False,
	 icon='Android_robot.ico')
	 
coll = COLLECT(exe,
     a.binaries,
     a.zipfiles,
     a.datas,
     strip=False,
     upx=True,
     upx_exclude=[],
     name='main')
