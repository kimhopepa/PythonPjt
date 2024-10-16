# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [ ('CodeReviewCheck.ui', '.'), 
				('CodeReviewCheck_Detail.ui', '.'), 
				('folder_icon.png', '.'), 
				('hw_main_form.png', '.') ]


# 여기에 암호화 키를 설정합니다. (16, 24, 32 바이트 길이의 키를 사용해야 합니다.)
cipher_key = 'your_secure_key'  # 여기에 원하는 키를 입력하세요. 

# 암호화 설정
if cipher_key:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad  # 필요한 경우 패딩 추가
    from base64 import b64encode  # Base64 인코딩을 사용하려면 필요

    # AES 블록 암호 설정
    block_cipher = AES.new(cipher_key.encode('utf-8'), AES.MODE_EAX)
else:
    block_cipher = None

a = Analysis(
    ['CodeReviewCheck.py'],
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
    name='CodeReviewCheck',
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
	icon='hw_main_form.ico',
	version='version.txt',    # 버전 정보 설정
)
