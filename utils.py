from typing import Generator, Tuple
import os

def file_to_bytes_generator(filename,chunksize=1048576) -> Generator:
    ''' Generates the single bytes from `filename` in `chunksize` sized chunks
    \nArgs:
    \n\tfilename (str): file full name (including path).
    \n\tchucksize (int): the chunksize to be read from the file.
    \t(default is 1048576(1MB))
    \nReturns:
    \n\tgenerator: a generator of the hex str of the bytes.
    '''
    with open(filename,"rb") as input:
        while True:
            chunk = input.read(chunksize)
            print(i)
            if chunk:
                for b in chunk: yield hex(b)
                #yield from chunuk
            else: break

gen_cannon_path = lambda filename : os.path.join(ps.getcwd(),filename)

def is_regex(key):
    #todo 
    return False


def seperate_dic_by_len(dic) -> Tuple[list,dict]:
    ''' Creats a new dictionary by the keys length for easier search later on, also seperates the regex out
    \n Args:
    \n\t dic (dict): the original dictionary
    \nReturns:
    \n\t list: all of the possible key sizes
    \n\t dict: a dictionary which maps the length to a dict of keys in that length, and regex to all regexes
    '''
    sep = {"regex": {}}
    lengths = []
    for key in dic:
        if not is_regex(key):
            length = len(key)//2 #get byte len
            if length not in sep:
                sep[length] = {}
                lengths.append(length) #adding the length to the lengths array for later use
            sep[length][key.lower()] = dic[key] #lower to match the hex string
        else:
            sep["regex"][key.lower()] = dic[key]
    return lengths, sep



format_byte = lambda byte : byte[2:] if len(byte) == 4 else "0" + byte[2:]
update_buffer = lambda buffer,byte : buffer[2:] + format_byte(byte)

# def update_buffer(old_buffer,byte) -> int:
#     '''Add the new byte to the buffer, strip the first old byte(if necessery)
#     \nArgs:
#     \n\t old_buffer: the old buffer
#     \n\t byte: the new byte
#     \n\t max_key_length: the longest key length we have, to make sure our buffer isnt too long
#     \n Returns:
#     \n\t int: the new buffer
#     '''
#     return old_buffer[2:] + format_byte(byte)
