from typing import Generator
import os
import json

MB = 1048576
KB = 1024


def file_to_chunks_generator(filename, chunksize=4*MB, upto_offset=0) -> Generator:
    '''
    Generates the 'chunksize` sized chunks from `filename`
    \nArgs:
    \n\tfilename (str): file full name (including path).
    \n\tchucksize (int): the chunksize (in bytes) to be read from the file.
    \t(default is 4,194,304 bytes (4MB))
    \n\tupto_offset (int): offset of the last byte to be read
    \t(default is 0(readAll))
    \nReturns:
    \n\tgenerator: a generator of the hex str of the bytes.
    '''
    with open(filename, "rb") as input:
        i = 0
        upto_offset = int(
            upto_offset) if upto_offset else os.path.getsize(filename)
        while i < upto_offset:
            chunk = input.read(chunksize)
            if chunk:
                yield format_chunk(chunk)
                i += chunksize
            else:
                break


def get_dict_from_json(input) -> dict:
    '''
    Creats a Pattern dictionary from a json file
    \nArgs:
    \n\tinput: the json file with the dictionary
    \n Returns:
    \n\t dict: the pattern dictionary
    '''
    with open(input, "r") as inp:
        dic = json.load(inp)
    return dic


def write_dict_to_json(dic, output, indent=2) -> None:
    '''
    Writes a Pattern dictionary to a json file
    \nArgs:
    \n\tdic: the Pattern dictionary
    \n\toutput: the json file
    '''
    with open(output, "w") as out:
        out.write(json.dumps(dic, indent=indent))


def format_byte(byte): return r"\x" + \
    byte[2:].upper() if len(byte) == 4 else r"\x0" + byte[2:].upper()


def strip_byte(byte): return format_byte(byte)[2:]


def format_chunk(chunk): return [strip_byte(hex(byte)) for byte in chunk]
