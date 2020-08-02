import fileAnalizer
import time
import argparse

dic = { '5D00008000': 'lzma',
        '504B03040A' : 'coral_zip',
    '27051956': 'uImage',
    '18286F01': 'zImage',
    '1F8B0800': 'gzip',
    '1F8B0808': 'gzip',
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
    '7F454C46': 'elf',
    "([0-9][A-F]){2,}" : "less then A0",
    "([A-F]{2}){3,}" : "Only letters",
    "([0-9]{2}){3,}" : "Only numbers",
    "([A-F][0-9])([0-9][A-F])([A-F]{4})": "sigs",
    }#"00+" : "zeros"}


def main():
    t0 = time.time()
    fa = fileAnalizer.FileAnalizer("coral.zip")
    fa.find_patterns(dic,repeating=4)
    fa.write_results()
    print(time.time() - t0)


if __name__ == "__main__":
    main()