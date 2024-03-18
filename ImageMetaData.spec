# -*- mode: python ; coding: utf-8 -*-

import PyInstaller.config
block_cipher = None

# Variables.
OUTPUT_DIR = "C:\\Users\\ricks\\Downloads\\Python\\ImageMetaData\\exec"

PyInstaller.config.CONF['distpath'] = OUTPUT_DIR

# Create the Command Line executable.
command = Analysis([
            'C:\\Users\\ricks\\Downloads\\Python\\ImageMetaData\\ImageMetaData.py',
            'C:\\Users\\ricks\\Downloads\\Python\\ImageMetaData\\functions\\functions.py'
            ],
            pathex=[],
            binaries=None,
            datas=[
			('C:\\Users\\ricks\\Downloads\\Python\\ImageMetaData\\README.md','.')
            ],
            hiddenimports=[],
            hookspath=[],
            runtime_hooks=[],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher
            )

command.excludedimports=[]

pyz = PYZ(command.pure, command.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
            command.scripts,
            [],
            exclude_binaries=True,
            name='ImageMetaData',
            debug=True,
            bootloader_ignore_signals=False,
            strip=False,
            upx=False,
            console=True, # True = Enable the command line in background to debug.
            icon='C:\\Users\\ricks\\Downloads\\Python\\ImageMetaData\\images\\icon.ico')

coll = COLLECT(exe, Tree('C:\\Users\\ricks\\Downloads\\Python\\ImageMetaData\\functions'),
                command.binaries,
                command.zipfiles,
                command.datas,
                strip=False,
                upx=False,
                name='ImageMetaData',
                icon='C:\\Users\\ricks\\Downloads\\Python\\ImageMetaData\\images\\icon.ico')