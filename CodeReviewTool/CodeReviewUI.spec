# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [ ('CodeReviewUI.ui', '.'), ('CodeReviewUI_Detail.ui', '.'), ('folder_icon.png', '.'), ('folder_icon.png', '.') ]

a = Analysis(
    ['CodeReviewUI.py'],
    pathex=['C:\\Users\\KIMJH\\Documents\\GitHub\\PythonPjt\\CodeReviewTool'],
    binaries=[],
    datas= added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CodeReviewUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
