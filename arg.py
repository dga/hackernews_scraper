import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--echo", help="echo stuff", action="store_true")
args = parser.parse_args()

if args.echo:
    print(args.echo)
