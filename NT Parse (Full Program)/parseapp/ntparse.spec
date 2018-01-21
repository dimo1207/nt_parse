from kivy.deps import sdl2, glew
# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\m_dim\\Documents\\Anaconda3\\main.py'],
             pathex=['C:\\Users\\m_dim\\Documents\\Anaconda3\\parseapp'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='ntparse',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='c:\\Users\\m_dim\\Documents\\Anaconda3\\ntparse_icon.ico')
coll = COLLECT(exe, Tree('C:\\Users\\m_dim\\Documents\\Anaconda3\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='ntparse')
