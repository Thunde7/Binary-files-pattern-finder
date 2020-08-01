from result import Result
import utils
import re

class FileAnalizer():

    def __init__(self,filename):
        self.filename = filename
        self.res = Result(f"{filename}_patterns.json")

    def find_patterns_and_repeats(self,dic,repeating=False,chunksize=utils.MB):
        len_to_pattern_dic, regex = utils.seperate_dic_by_len(dic)
        buffer_size = max(len_to_pattern_dic)
        buffer = "Z" * buffer_size * 2              #starting the buffer to all ZZ "bytes", not a hexdec number
        
        
        if repeating:
            prev = None
            seq_len = 1

        if regex:
            ranges = {}

        for i, byte in enumerate(utils.file_to_bytes_generator(self.filename,chunksize=chunksize)):
            if repeating:
                if byte == prev: seq_len += 1
                else:
                    if seq_len > 1: self.res.add("repeating_byte",(i)-seq_len,seq_len,repeater=format_byte(prev))
                    seq_len = 1
                prev = byte

            buffer = update_buffer(buffer,byte)
            for length in len_to_pattern_dic:
                buffer_key = buffer[:2*length]
                if buffer_key in len_to_pattern_dic[length]:
                    match_start = i - (buffer_size - 1)      #The match starts when the first byte "hits" the head of the buffer
                    self.res.add(len_to_pattern_dic[length][buffer_key],match_start,length)

            if regex:
                for r in regex:
                    match = re.match(r.upper(),buffer)
                    if match: utils.add_range(ranges,regex[r],i-(buffer_size-1),match)
    
    def find_regex(self,dic,chunksize=utils.MB):
        buffer_size = 1024 #1KB
        buffer = "Z" * buffer_size * 2
        ranges = {}
        for i, byte in enumerate(utils.file_to_bytes_generator(self.filename,chunksize=chunksize)):
            buffer = update_buffer(buffer,byte)
            for regex in dic:
                match = re.match(regex.upper(),buffer)
                if match:
                    utils.add_range(ranges,dic[regex],i-(buffer_size-1),match)
        self.res.add_from_dict(ranges)

    def write_results(self):
        self.res.write_to_file()



update_buffer = lambda buffer,byte : buffer[2:] + strip_byte(byte)

format_byte = lambda byte : r"\x" + byte[2:].upper() if len(byte) == 4 else r"\x0" + byte[2:].upper()

strip_byte = lambda byte : format_byte(byte)[2:]

