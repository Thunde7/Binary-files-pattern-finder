import main


dic = { '5D00008000': 'lzma',
    '27051956': 'uImage',
    '18286F01': 'zImage',
    '1F8B0800': 'gzip',
    '303730373031': 'cpio',
    '303730373032': 'cpio',
    '303730373033': 'cpio',
    '894C5A4F000D0A1A0A': 'lzo',
    '5D00000004': 'lzma',
    'FD377A585A00': 'xz',
    '314159265359': 'bzip2',
    '425A6839314159265359': 'bzip2',
    '04224D18': 'lz4',
    '02214C18': 'lz4',
    '1F9E08': 'gzip',
    '71736873': 'squashfs',
    '51434454': 'dtb',
    '68737173': 'squashfs',
    'D00DFEED': 'fit',
    '7F454C46': 'elf'
    }

filename = "XXXXXXXXX.zip"


main.find_patterns(filename,dic)