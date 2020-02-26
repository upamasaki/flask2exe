# flask2exe

## pyinstallerでexeファイルを作成する

pyinstallerで○○.specファイルを作成する．

```
(venv)flaskApp>pyinstaller runserver.py -F
```

.specの編集を行う．以下参考

```spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
               ('flask2exe\\templates', 'flask2exe\\templates'), 
               ('flask2exe\\static', 'flask2exe\\static'),
               ('flask2exe\\logs', 'flask2exe\\logs'), 
               ('flask2exe\\module', 'flask2exe\\module'), 
              ]
#sample1.py, sample2.py, config.pyを追加
hidden_imports = [
         'flask2exe.views'
         ]
#カレントディレクトリとflask2exeを追加
paths = [
         './',
         './flask2exe',
         ]

a = Analysis(['runserver.py'],
             pathex=paths,
             binaries=[],
             datas=added_files,
             hiddenimports=hidden_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='runserver',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )

```

exeファイルの作成

```
(venv)flaskApp>pyinstaller runserver.spec -F
```


参考サイト
<br>
https://max999blog.com/python-flask-pyinstaller-make-exe-file/

