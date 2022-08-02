#!/usr/bin/env python3
import sys, os, argparse, logging

logger = logging.getLogger()

def init_logging():
    global logger
    log_formatter = logging.Formatter('[{asctime}] {levelname}: {message}', datefmt='%Y-%m-%d %H:%M:%S', style='{')
    stream_handler = logging.StreamHandler(stream=sys.stderr)
    stream_handler.setFormatter(log_formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Sort k-mers in a (small!) matrix according to their position within a given unitig')
    parser.add_argument('-m','--mat', dest='kmat', metavar='PATH', required=True, help='Input k-mer matrix (it will be loaded in memory)')
    parser.add_argument('-s','--samples', dest='samples', metavar='PATH', required=True, help='List of samples (i.e., matrix-column identifiers)')
    parser.add_argument('-o','--output', dest='out', metavar='PATH', required=True, help='Output file name')
    args = parser.parse_args()

    init_logging()

    is_input_valid=True
    if not os.path.isfile(args.kmat):
        is_input_valid=False
        logger.error(f'-m/--mat file "{args.kmat}" does not exist.')
    elif not os.path.isfile(args.samples):
        is_input_valid=False
        logger.error(f'-s/--samples file "{args.samples}" does not exist.')
    elif os.path.isfile(args.out) and os.stat(args.out).st_size > 0:
        is_input_valid=False
        logger.error(f'-o/--output file "{args.out}" already exists.')
    if not is_input_valid:
        return 1

    sample_ids = []
    with open(args.samples,'r') as sf:
        sample_ids = [line.strip() for line in sf if line.strip() != '']

    sample_dict = {}
    for sid in sample_ids:
        sample_dict[sid] = []

    # load matrix in a dictionary
    with open(f'{args.kmat}','r') as mf:
        for line in mf:
            line = line.strip()
            if line == "":
                continue
            kmer,cols = line.split(' ',maxsplit=1)
            for i,val in enumerate(map(int,cols.split())):
                if val == 0:
                    continue
                sid = sample_ids[i]
                sample_dict[sid].append((kmer,val))
    
    for sid in sample_dict.keys():
        slist = sample_dict[sid]
        print(f'{sid} ' + ' '.join((':'.join(map(str,x)) for x in slist)))

    return 0

if __name__ == "__main__":
    sys.exit(main())
