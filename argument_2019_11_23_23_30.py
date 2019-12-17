import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--add", help="increase output verbosity")
args = parser.parse_args()
if args.add:
    print ("add turned on")
    print(args.add)


asd