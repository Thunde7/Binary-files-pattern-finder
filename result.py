import json
import utils


class Result():
    def __init__(self, filename, indent=2):
        self.dic = {}
        self.filename = filename
        self.indent = indent

    def add(self, name, start, length, repeater=None) -> None:
        '''
        Adds the new result range
        \nArgs:
        \n\t name (str): the name of the pattern
        \n\t start (int)
        \n\t length (int)
        \n\t repeater (str): if the ranges represents a repeated sequence, specifies the repeating byte
        \t (default is None) 
        '''
        item = {"range": f'({utils.strip_byte(hex(start))},{utils.strip_byte(hex(start+length-1))})', "length": length} if not repeater else \
            {"range": f'({utils.strip_byte(hex(start))},{utils.strip_byte(hex(start+length-1))})',
             "length": length, "repeating_byte": repeater}
        if name not in self.dic:
            self.dic[name] = []
        self.dic[name].append(item)

    def add_from_dict(self, ranges) -> None:
        '''
        Adds all ranges from the `ranges` dictionary
        '''
        for name in ranges:
            for start, length in ranges[name].items():
                self.add(name, start, length)

    def write_to_file(self) -> None:
        with open(self.filename, "w") as out:
            out.write(json.dumps(self.dic, indent=self.indent))
