from result import Result
import utils

class FileAnalizer():

    def __init__(self,filename):
        self.filename = filename
        self.res = Result(f"{filename}_patterns.json")

    def find_patterns_and_repeats(self,dic,repeating=False):
        len_to_pattern_dic = utils.seperate_dic_by_len(dic)
        max_key_length = max(len_to_pattern_dic)
        min_key_length = min(len_to_pattern_dic)
        buffer_size = 2 * max_key_length                #2 digits per byte in the longest pattern
        buffer = "Z" * buffer_size                      #starting the buffer to all Z, not a hexdec digit

        if repeating:
            prev = None
            seq_len = 1

        for i,byte in enumerate(utils.file_to_bytes_generator(self.filename)):
            if repeating:
                if byte == prev: seq_len += 1
                else:
                    if seq_len > 1: self.res.add("repeating_bye",(i)-seq_len,seq_len,repeater=utils.format_byte(prev))
                    seq_len = 1
                prev = byte

            buffer = update_buffer(buffer,byte)
            for length in len_to_pattern_dic:
                buffer_key = buffer[:2*length]
                if buffer_key in len_to_pattern_dic[length]:
                    match_start = i - max_key_length                #The match starts when the first byte "hits" the head of the buffer
                    self.res.add(len_to_pattern_dic[length][buffer_key],match_start,length)
    
    def write_results(self):
        self.res.write_to_file()



update_buffer = lambda buffer,byte : buffer[2:] + strip_byte(byte)

format_byte = lambda byte : r"\x" + byte[2:].upper() if len(byte) == 4 else r"\x0" + byte[2:].upper()

strip_byte = lambda byte : format_byte(byte)[2:]

