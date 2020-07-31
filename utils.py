from typing import Generator, Tuple

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
            if chunk:
                for b in chunk: yield hex(b)
                #yield from chunuk
            else: break

def seperate_dic_by_len(dic) -> dict:
    ''' Creats a new dictionary by the keys length for easier search later on
    \n Args:
    \n\t dic (dict): the original dictionary
    \nReturns:
    \n\t dict: a dictionary which maps the length to a dict of keys in that length
    '''
    patterns = {}
    for key in dic:
        length = len(key)//2 #get byte len
        if length not in patterns:
            patterns[length] = {}
        patterns[length][key.upper()] = dic[key] #upper to match the hex string
    return patterns



def get_dict_from_json(input):
    with open(input,"r") as inp:
        dic = json.load(inp)
    return dic