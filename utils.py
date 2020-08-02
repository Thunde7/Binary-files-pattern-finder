from typing import Generator, Tuple

MB = 1048576
KB = 1024

def file_to_bytes_generator(filename,chunksize=8*KB) -> Generator:
    ''' Generates the single bytes from `filename` in `chunksize` sized chunks
    \nArgs:
    \n\tfilename (str): file full name (including path).
    \n\tchucksize (int): the chunksize to be read from the file.
    \t(default is 8192(8KB))
    \nReturns:
    \n\tgenerator: a generator of the hex str of the bytes.
    '''
    with open(filename,"rb") as input:
        i=0
        while i < 8*MB:
            chunk = input.read(chunksize)
            if chunk:
                for b in chunk: yield hex(b)
                #yield from chunk
                i += chunksize
            else: break

def file_to_chunks_generator(filename,chunksize=8*KB) -> Generator:
    ''' Generates the single bytes from `filename` in `chunksize` sized chunks
    \nArgs:
    \n\tfilename (str): file full name (including path).
    \n\tchucksize (int): the chunksize to be read from the file.
    \t(default is 8192(8KB))
    \nReturns:
    \n\tgenerator: a generator of the hex str of the bytes.
    '''
    with open(filename,"rb") as input:
        i=0
        while i < 8*MB:
            chunk = input.read(chunksize)
            if chunk:
                yield format_chunk(chunk)
                i += chunksize
            else: break

def get_dict_from_json(input) -> dict:
    '''
    Creats a Pattern dictionary from a json file
    \nArgs:
    \n\tinput: the json file with the dictionary
    \n Returns:
    \n\t dict: the pattern dictionary
    '''
    with open(input,"r") as inp:
        dic = json.load(inp)
    return dic

format_byte = lambda byte : r"\x" + byte[2:].upper() if len(byte) == 4 else r"\x0" + byte[2:].upper()
strip_byte = lambda byte : format_byte(byte)[2:]

format_chunk = lambda chunk : [strip_byte(hex(byte)) for byte in chunk]
