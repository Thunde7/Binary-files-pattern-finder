import json
import utils

class result():
    def __init__(self,indent=2):
        self.dic = {}
        self.indent = indent

    def add(self,name,start,length,repeater=None):
        item = {"range" : f'({start},{start+length})',"length" : length} if not repeater else \
                {"range" : f'({start},{start+length})', "length" : length, "repeating_byte" : repeater}
        if name not in self.dic:
            self.dic[name] = []
        self.dic[name].append(item)

    def write_to_file(self,filename):
        with open(filename,"w") as out:
            out.write(json.dumps(self.dic,indent=self.indent))


def find_patterns(filename,dic,output,is_relative=False):
    if is_relative:
        filename = utils.get_cannon_path(filename)
    
    res = result()

    key_lengths, dic_by_key_len = utils.seperate_dic_by_len(dic)
    
    max_key_length = max(key_lengths)
    min_key_length = min(key_lengths)
    curr_buff = "00" * max_key_length

    for i,byte in enumerate(utils.file_to_bytes_generator(filename)):
        curr_buff = utils.update_buffer(curr_buff,byte)
        for length in key_lengths:
            if curr_buff[:2*length] in dic_by_key_len[length]:
                res.add(dic_by_key_len[length][curr_buff[:2*length]],
                i-min_key_length-(length+1),length)

    res.write_to_file(output)
