from typing import Generator, Tuple

MB = 1048576

def file_to_bytes_generator(filename,chunksize=MB) -> Generator:
    ''' Generates the single bytes from `filename` in `chunksize` sized chunks
    \nArgs:
    \n\tfilename (str): file full name (including path).
    \n\tchucksize (int): the chunksize to be read from the file.
    \t(default is 1048576(1MB))
    \nReturns:
    \n\tgenerator: a generator of the hex str of the bytes.
    '''
    with open(filename,"rb") as input:
        i=0
        while i<2:
            chunk = input.read(chunksize)
            i += 1
            if chunk:
                for b in chunk: yield hex(b)
                #yield from chunuk
            else: break

def seperate_dict_by_len(dic) -> Tuple[dict,dict] :
    ''' Creats a new dictionary by the keys length for easier search later on
    \n Args:
    \n\t dic (dict): the original dictionary
    \nReturns:
    \n\t dict: a dictionary which maps the length to a dict of keys in that length
    \n\t dict : the regex patterns dictionary
    '''
    patterns = {}
    regex = {}
    for key in dic:
        if any([x in key for x in ["[","]","{","}","*",".","+"]]):    
            regex[key] = dic[key]
        else:
            length = len(key)//2 #get byte len
            if length not in patterns:
                patterns[length] = {}
            patterns[length][key.upper()] = dic[key] #upper to match the hex string
    return patterns, regex

def add_range(ranges,name,start,end):
    if name in ranges:
        prev = ranges[name][-1]
        if prev["start"] < start and start <= prev["end"]:
            prev["end"] = max(prev["end"],start+end//2-1)
        else:
            ranges[name].append({"start" : start,"end" : start+end//2-1}) 
    else:
        ranges[name] = [{"start" : start,"end" : start+end//2-1}]


def get_dict_from_json(input):
    with open(input,"r") as inp:
        dic = json.load(inp)
    return dic