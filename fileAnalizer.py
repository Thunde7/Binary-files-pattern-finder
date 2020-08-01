from result import Result
import utils
import re
from threading import Thread
from multiprocessing import Process

class FileAnalizer():

    def __init__(self,filename):
        self.filename = filename
        self.res = Result(f"{filename}_patterns.json")

    def find_patterns_and_repeats(self,dic,repeating=0,chunksize=utils.MB):
        patterns, regex = utils.seperate_dict_by_len(dic)
        buffer_size = 512                           # 0.5KB, for eazier pattern and regex checking
        buffer = "Z" * buffer_size * 2              #starting the buffer to all ZZ "bytes", not a hexdec number
        
        if repeating:
            prev = None
            seq_len = 1

        if regex:
            ranges = {}

        for i, byte in enumerate(utils.file_to_bytes_generator(self.filename,chunksize=chunksize)):
            
            buffer = update_buffer(buffer,byte)
            
            if repeating:
                if byte == prev: seq_len += 1
                else:
                    if seq_len > repeating: self.res.add("repeating_byte",(i)-seq_len,seq_len,repeater=format_byte(prev))
                    seq_len = 1
                prev = byte
            if patterns: 
                for length in patterns:
                    buffer_key = buffer[:2*length]
                    if buffer_key in patterns[length]:
                        match_start = i - (buffer_size - 1)      #The match starts when the first byte "hits" the head of the buffer
                        self.res.add(patterns[length][buffer_key],match_start,length)

            if regex:
                for r in regex:
                    #Process(target=regex_match,args=(ranges,regex[r],i,r.upper(),buffer)).run()
                    regex_match(ranges,regex[r],i,r.upper(),buffer)
                    #match = re.match(r.upper(),buffer)
                    #if match: utils.add_range(ranges,regex[r],i-(buffer_size-1),match.end())
        self.res.add_from_dict(ranges)
    
    def write_results(self):
        self.res.write_to_file()

def regex_match(ranges,name,index,regex,buffer):
    match = re.match(regex,buffer)
    if match: utils.add_range(ranges,name,index-(len(buffer)//2-1),match.end())

update_buffer = lambda buffer,byte : buffer[2:] + strip_byte(byte)

format_byte = lambda byte : r"\x" + byte[2:].upper() if len(byte) == 4 else r"\x0" + byte[2:].upper()

strip_byte = lambda byte : format_byte(byte)[2:]

