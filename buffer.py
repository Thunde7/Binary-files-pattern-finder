import utils
import re


class Buffer():

    def __init__(self, size):
        self.str = "ZZ" * size  # starting to a non hexedecimal digit
        self.size = size

    def update(self, bytes_):
        self.str = self.str[len(bytes_):] + "".join(bytes_)

    def __len__(self):
        return len(self.str)

    def __str__(self):
        return self.str

    def pattern_ranges_in_buffer(self, dic) -> dict:
        '''
        Find all of the dict's patterns in the current buffer
        \nArgs:
        \n\t dic (dict): the pattern dictionary
        '''
        patt_list = dic.keys()  # done for easier readablity later
        ranges_dict = {}
        # find all matches extremely fast
        for match_list in [(key, re.finditer(key, self.str)) for key in patt_list]:
            for item in match_list[1]:
                if dic[match_list[0]] not in ranges_dict:
                    # Init the list of item that matched the key
                    ranges_dict[dic[match_list[0]]] = []
                ranges_dict[dic[match_list[0]]].append(
                    {"start": item.start()//2, "end": item.end()//2})
                # the start and end are relative to the current buffer, we will fix that later
        return ranges_dict
