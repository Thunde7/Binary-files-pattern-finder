import json
import utils

class result():
    def __init__(self,indent=2):
        self.dic = {}
        self.indent = indent

    def add(self,name,start,length,repeater=None):
        item = {"range" : (start,start+length)} if not repeater else \
                {"range" : (start,start+length), "repeating_byte" : repeater}
        if name not in self.dic:
            self.dic[name] = []
        self.dic[name].append(item)

    def write_to_file(self,filename):
        with open(filename,"w") as out:
            out.write(json.dumps(self.dic,indent=self.indent))


def find_patterns(filename,dic,is_relative=False):
    if is_relative:
        filename = utils.get_cannon_path(filename)
    
    res = result()

    windows, seperated_dic = utils.seperate_dic(dic)
    
    for i,byte in enumerate(utils.file_to_bytes_generator(filename)):
        utils.update_windows(windows,byte)
        for size in windows:
            if windows[size] in seperated_dic[size]:
                print("aha")
                result.add(seperated_dic[size][windows[size]],i-size,size)

    res.write_to_file("a.json")
