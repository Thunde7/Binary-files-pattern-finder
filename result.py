import json

class Result():
    def __init__(self,filename,indent=2):
        self.dic = {}
        self.filename = filename
        self.indent = indent

    def add(self,name,start,length,repeater=None):
        item = {"range" : f'({start},{start+length-1})',"length" : length} if not repeater else \
                {"range" : f'({start},{start+length-1})', "length" : length, "repeating_byte" : repeater}
        if name not in self.dic:
            self.dic[name] = []
        self.dic[name].append(item)

    def add_from_dict(self,ranges):
        for name in ranges:
            for start,length in ranges[name].items():
                self.add(name,start,length)


    def write_to_file(self):
        with open(self.filename,"w") as out:
            out.write(json.dumps(self.dic,indent=self.indent))

