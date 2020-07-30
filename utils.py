from typing import Generator
import os

def file_to_bytes_generator(filename,chunksize=1048576) -> Generator:
    ''' Generates the single bytes from 'filename' in `chunksize` sized chunks
    \nArgs:
    \n\tfilename (str): file full name (including path).
    \n\tchucksize (int): the chunksize to be read from the file.
    \t(default is 1048576(1MB))
    \nReturns:
    \n\tgenerator: a generator of the str of the bytes.
    '''
    with open(filename,"rb") as input:
        while True:
            chunk = input.read(chunksize)
            if chunk:
                for b in chunk: yield hex(b)
                #yield from chunk
            else: break

def get_cannon_path(filename):
    return os.path.join(os.getcwd(),filename)

def is_regex(key):
    #todo 
    return False


def seperate_dic(dic):
    res = {"regex": {}}
    windows = {}
    for key in dic:
        if not is_regex(key):
            length = len(key)
            if length not in res:
                res[length] = {}
                windows[length] = "/x"
            res[length][key] = dic[key]
        else:
            res["regex"][key] = dic[key]

    return windows,res

def update_windows(windows,byte):
    stripped_byte = byte[2:] if len(byte) == 4 else "0" + byte[2:]
    for size in windows:
        window = windows[size]
        if len(window) == 2*size:
            window = "/x" + window[4:]
        window += stripped_byte
        windows[size] = window

