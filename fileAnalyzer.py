from result import Result
from buffer import Buffer
import utils
import re


class FileAnalyzer():
    '''
    Analizes files according to dictionaries
    '''

    def __init__(self, filename, chunksize=4 * utils.MB):
        '''
        Initiates a file analyzer
        \nArgs:
        \n\t filename (str): the filename to analize
        \n\t chunksize (int): the size of chunks to be read at a time from the file
        \t(default is 4,194,304 byts (4MB))
        '''
        self.filename = filename
        self.res = Result(f"{filename}_patterns.json")
        self.chunksize = chunksize
        self.match_ranges = {}

    def find_patterns(self, dic, upto_offset=0, repeating=0) -> None:
        '''
        Find the patterns from the dictionary in the file upto the offset given, add them to the result
        \nArgs:
        \n\tdic (dict): The pattern dictionary
        \n\t`upto_offset` (int): the offset of the last byte to be read
        \t (default is 0(read the whole file))
        \n\t repeating (int): the shortest repeated byte sequance to write down
        \t (default is 0(don't search for repeated bytes))
        '''
        buff = Buffer(self.chunksize * 2)  # 2 chunks per buffer
        # in case of a match seperating between two chunks

        if repeating:
            repet_ex = re.compile(r"(..)\1{" + str(repeating) + ",}")

        # re searches faster for pre compiled expresions
        regex = {re.compile(key): val for key, val in dic.items()}

        for i, chunk in enumerate(utils.file_to_chunks_generator(self.filename, chunksize=self.chunksize, upto_offset=upto_offset)):
            buff.update(chunk)

            new_ranges = buff.pattern_ranges_in_buffer(dic)
            self.update_ranges(new_ranges, i)

            if repeating:
                for match in re.finditer(repet_ex, "".join(chunk)):
                    self.res.add("reapiting byte", i+match.start()//2, match.end()//2-match.start()//2,
                                 repeater=utils.format_byte(hex(int(match.groups()[0]))))

        self.res.add_from_dict(self.match_ranges)

    def write_results(self) -> None:
        self.res.write_to_file()

    def update_ranges(self, new_ranges, current_chunk_index) -> None:
        ''''
        updates the current ranges according to the new ranges
        \nArgs:
        \n\t `new_ranges` (dict): a dictionary from the
        \t name to a dictionary of the spans of the matches
        \n\t current_chunk_index (int)
        '''
        for name, rng_list in new_ranges.items():
            for rng in rng_list:
                start = rng["start"] + \
                    (current_chunk_index-3) * self.chunksize//2
                length = (rng["end"] - rng["start"])
                if name not in self.match_ranges:
                    self.match_ranges[name] = {}
                if start in self.match_ranges[name]:
                    length = max(length, self.match_ranges[name][start])
                self.match_ranges[name][start] = length
