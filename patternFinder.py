import fileAnalyzer
import utils
from time import time
import argparse


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "<filepath>", help="the name of the file to be parsed", default=None)
    ap.add_argument(
        "<dictpath>", help="the path to the pattern/regex dictionary,default is dict.json", default=None)
    ap.add_argument(
        "--minrepeats", help="the minimum amout of bytes repeats to log to the json file, default is 0", default="0")
    ap.add_argument(
        "--readsize", help="the amout of bytes to be read from the file, default is the whole file", default="0")
    ap.add_argument(
        "--chunksize", help="the amount of bytes read at a time, default is 2MB, do not exceed 1GB", default=4*utils.MB)
    ap.add_argument(
        "--time", help="messures and prints the time the tool took", default=False)
    ap.print_help
    return ap.parse_args()


def main():
    args = parse_args()
    if not (args.filepath and args.dictpath):
        raise(ValueError("you need to specify the filepath and dictpath"))
    patt_dict = utils.get_dict_from_json(args.dictpath)
    find_patterns(args.filepath, patt_dict, repeats=args.minrepeats,
                  readsize=args.readsize, chunksize=args.chunksize, time_=args.time)


def find_patterns(filename, patt_dict, repeats=0, readsize=0, chunksize=4*utils.MB, time_=False):
    '''
    finds the patterns from `patt_dict` in  `filename`'s binary, writes them to a json file
    \nArgs:
    \n\t filename (str): The name of the file to be searched
    \n\t `patt_dict` (dict): The patterns dictionary
    \n\t repeats (int): the minimum length of a repeating byte sequance to be search for
    \t (default is 0(don't search for repeats))
    \n\t readsize (int): the amount of bytes to be read from the file
    \t (default is 0(the whole file))
    \n\t chunksize (int): the amount of bytes to be parsed at once
    \t (default is 4MB)
    \n\t time_ (bool): measure and print how long the process took
    \t (default is False)
    '''
    fa = fileAnalyzer.FileAnalyzer(filename, chunksize=chunksize)
    if time_:
        t0 = time()
    fa.find_patterns(patt_dict, readsize, repeating=repeats)
    fa.write_results()
    if time_:
        print(f"the run took {time() - t0} seconds")


if __name__ == "__main__":
    main()
