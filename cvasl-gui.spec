# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

# Collect data files from packages
datas = []

# Add Dash assets
datas += [(os.path.join('src', 'cvasl_gui', 'assets'), os.path.join('cvasl_gui', 'assets'))]

# Collect data files from dash and related packages
datas += collect_data_files('dash')
datas += collect_data_files('dash_bootstrap_components')
datas += collect_data_files('plotly')
datas += collect_data_files('cvasl')

# Collect all submodules that might be dynamically imported
hiddenimports = []
hiddenimports += collect_submodules('dash')
hiddenimports += collect_submodules('dash_bootstrap_components')
hiddenimports += collect_submodules('plotly')
hiddenimports += collect_submodules('cvasl')
hiddenimports += collect_submodules('waitress')
hiddenimports += collect_submodules('flask')
hiddenimports += collect_submodules('werkzeug')
hiddenimports += collect_submodules('pandas')
hiddenimports += collect_submodules('numpy')
hiddenimports += collect_submodules('sklearn')

# Additional hidden imports that are often needed
hiddenimports += [
    'engineio.async_drivers.threading',
    'pkg_resources.py2_warn',
    'cvasl_gui.components',
    'cvasl_gui.tabs',
    'cvasl_gui.jobs',
]

a = Analysis(
    [os.path.join('src', 'cvasl_gui', 'index.py')],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='cvasl-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='cvasl-gui',
)
