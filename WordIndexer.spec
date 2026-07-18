# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all


pyside6_datas, pyside6_binaries, pyside6_hiddenimports = collect_all("PySide6")


datas = [
    ("dictionaries", "dictionaries"),
    ("docs", "docs"),
    ("examples", "examples"),
    ("branding", "branding"),
    ("LICENSE", "."),
    *pyside6_datas,
]

binaries = [*pyside6_binaries]
hiddenimports = [
    "wordindexer.gui",
    "wordindexer.gui.app",
    *pyside6_hiddenimports,
]


analysis = Analysis(
    ["wordindexer/gui_launcher.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(analysis.pure)

executable = EXE(
    pyz,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name="WordIndexer",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="branding/WordIndexer_user.ico",
)

COLLECT(
    executable,
    analysis.binaries,
    analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="WordIndexer",
)
