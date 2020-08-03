import fileAnalyzer
import utils
import time
import argparse


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "filepath", help="the name of the file to be parsed", default=None)
    ap.add_argument(
        "dictpath", help="the path to the pattern/regex dictionary,default is dict.json", default=None)
    ap.add_argument(
        "min_repeats", help="the minimum amout of bytes repeats to log to the json file, default is 0", default="0")
    ap.add_argument(
        "--readsize", help="the amout of bytes to be read from the file, default is the whole file", default="0")
    ap.add_argument(
        "--chunksize", help="the amount of bytes read at a time, default is 2MB, do not exceed 1GB", default=4*utils.MB)
    ap.add_argument(
        "--time", help="messures and prints the time the tool took", default=False)
    return ap.parse_args()


def main():
    args = parse_args()
    if not (args.filepath and args.dictpath):
        raise(ValueError("you need to specify the filepath and dictpath"))
    fa = fileAnalyzer.FileAnalyzer(args.filepath, chunksize=args.chunksize)
    pat_dict = utils.get_dict_from_json(args.dictpath)
    if args.time:
        t0 = time.time()
    fa.find_patterns(pat_dict, upto_offset=args.readsize,
                     repeating=args.min_repeats)
    fa.write_results()
    if args.time:
        print(f"the run took {time.time() - t0} seconds")


if __name__ == "__main__":
    main()
