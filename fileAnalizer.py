from result import Result
from buffer import Buffer
import utils
import re
from threading import Thread
from multiprocessing import Process

import time

class FileAnalizer():

    def __init__(self,filename,chunksize=None):
        self.filename = filename
        self.res = Result(f"{filename}_patterns.json")
        self.chunksize = chunksize if chunksize else 2 * utils.MB

    def find_patterns(self,dic,repeating=0):
        buff = Buffer(self.chunksize)

        ranges = {}

        if repeating:
            prev = None
            seq_len = 1

        for i, chunk in enumerate(utils.file_to_chunks_generator(self.filename,chunksize=self.chunksize)):
            buff.update(chunk)

            new_ranges = buff.pattern_ranges_in_buffer(dic)
            update_ranges(ranges,new_ranges,i,self.chunksize)

            if repeating:
                for j,byte in enumerate(chunk):
                    if byte == prev: seq_len += 1
                    else:
                        if seq_len > repeating: self.res.add("repeating_byte",(i+j)-seq_len,seq_len,repeater=utils.format_byte(prev))
                        seq_len = 1
                    prev = byte

        self.res.add_from_dict(ranges)
    
    def write_results(self):
        self.res.write_to_file()

def update_ranges(old_ranges,new_ranges,current_chunk_index,chunksize):
    for name, rng_list in new_ranges.items():
        for rng in rng_list:
            start = rng["start"] + (current_chunk_index-1) * chunksize//2 
            length = (rng["end"] - rng["start"])
            if name not in old_ranges: old_ranges[name] = {}
            if start in old_ranges[name]:
                length = max(length,old_ranges[name][start])
            old_ranges[name][start] = length


