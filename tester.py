import main
import utils
import random
import os
import json

dic = { '5D00008000': 'lzma',
        '504B03040A' : 'coral_zip',
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

def gen_dict_from_file(input,output=None):
    res = {}
    gen = utils.file_to_bytes_generator(input)
    size = os.path.getsize(input)
    for i,byte in enumerate(gen):
        if i * 5 < size and random.randrange(0,100) > 97:
            pat = "".join([strip(next(gen)) for _ in range(random.randrange(3,10))])
            res[pat] = f"random_{i}"
    if output:
        with open(output,"w") as out:
            out.write(json.dumps(res,indet=2))
    return res

strip = lambda byte : byte[2:] if len(byte) == 4 else "0" + byte[2:]

def get_dict_from_json(input):
    with open(input,"r") as inp:
        dic = json.load(inp)
    return dic

def better_test(input,output):
    dic = gen_dict_from_file(input)
    main.find_patterns(input,dic,output)


if __name__ == "__main__":
    #better_test("game.7z","game.json")
    main.find_patterns("coral.zip",dic,"coral.json")
    # better_test("coral.zip","coral.json")