import utils
import random
import os
import json
import time
from fileAnalizer import FileAnalizer

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
    "[(0-9)(A-F)]{2,}" : "[(0-9)(A-F)]{2,}",
    "([A-F]{2}){2,}":"Only letters",
    "00([(A-F)(0-9)][(1-9)(A-F)])*" : "zero"}


strip = lambda byte : byte[2:].upper() if len(byte) == 4 else "0" + byte[2:].upper()

def gen_dict_from_file(input,output=None):
    res = {}
    gen = utils.file_to_bytes_generator(input)
    size = os.path.getsize(input)
    i = 0
    for byte in gen:
        if i * 5 < size:
            if random.randrange(0,100) > 98:
                pat_len = random.randrange(3,10) 
                pat = "".join([strip(byte)] + [strip(next(gen)) for _ in range(pat_len)])
                res[pat] = f"random_that_started_at_{i}_with_len_{pat_len+1}"
                i += pat_len
            i += 1 
        else: break
    if output:
        with open(output,"w") as out:
            out.write(json.dumps(res,indet=2))
    return res

def random_test(input,repeating,chunksize=utils.MB):
    dic = gen_dict_from_file(input)
    pre_made_test(input,dic,repeating)

def pre_made_test(input,dic,repeating,chunksize=utils.MB):
    t0 = time.time()
    fa = FileAnalizer(input)
    fa.find_patterns_and_repeats(dic,repeating=repeating,chunksize=chunksize)
    fa.write_results()
    print(time.time()-t0)

if __name__ == "__main__":
    #random_test("game.7z",4)
    #pre_made_test("game.7z",dic,4)
    pre_made_test("coral.zip",dic,4,chunksize=1048576)