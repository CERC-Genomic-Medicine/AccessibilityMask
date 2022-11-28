#!/usr/bin/env python3
import pandas as pd
import argparse
import gzip
import pysam
import rapidjson


argparser = argparse.ArgumentParser(description = 
 'This script makes bed files from depth files generated by coverage pipeline!')
argparser.add_argument('-i', '--input-file', metavar = 'file', dest = 'in_path', type = str, required = True, help = 'File containing coverage of each variant and percent of individuals havingthat variant with specified coverage.')
argparser.add_argument('-dp', '--min-dp', metavar = 'number', dest = 'in_depth', type = str, required = True, help = 'Minimum depth considering as high coverage threshold, must be one of the elements of following list [5, 10, 15, 20, 25, 30, 50, 100].')
argparser.add_argument('-ind', '--pct-ind', metavar = 'number', dest = 'in_pct', type = int, required = True, help = 'Minimum percentile of individuals with the mentioned depth threshold, should be between 0 and 1.')
argparser.add_argument('-o', '--output', metavar = 'file', dest = 'out_file_path', type = str, required = True, help = 'Output bed file containing high coverage files.')


if __name__ == '__main__':
    args = argparser.parse_args()
    column_name = args.in_depth
    min_percent = args.in_pct
    range_start = -1
    with gzip.open(args.in_path, 'rt') as ifile, open(args.out_file_path, 'w') as fw:
        fw.write(f"CHROM\tstart\tend\n")
        for line in ifile:
            chrom, start, stop, data = line.rstrip().split('\t')
            data = rapidjson.loads(data)
            bp = int(data['start']) - 1
            pct = float(data[column_name])
            if (pct >= min_percent):
                if(range_start == -1):
                    range_start = previous_number = bp
                else:
                    if(bp == (previous_number + 1)):
                        previous_number = bp
                    else:
                        fw.write(f"{chrom}\t{range_start}\t{previous_number}\n")
                        range_start = previous_number = bp
        fw.write(f"{chrom}\t{range_start}\t{previous_number}\n")