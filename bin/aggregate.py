#!/usr/bin/env python

import argparse
import gzip
from contextlib import ExitStack
import pysam
from statistics import mean, median


argparser = argparse.ArgumentParser(description = 'Aggregate depth information (output as JSON) from individual depth files (generated using SAMtools depth).')
argparser.add_argument('-i', '--in', metavar = 'file', dest = 'in_files_list', required = True, help = 'Input file which lists all depth files (one depth file per sample) generated using SAMtools depth. One file per line.')
argparser.add_argument('-o', '--out', metavar = 'file', dest = 'out_file_name', required = True, help = 'Output file of depth information compressed with bgzip. In addition to this file, the tabix index will be produced.')
argparser.add_argument('-f', '--format', metavar = 'string', dest = 'output_format', required = True, default = 't', help = 'The type of output file: \'j\' - JSON, \'t\' - TSV (default).')


if __name__ == '__main__':
    args = argparser.parse_args()
    if args.output_format not in {'t', 'j'}:
        raise Error(f'Output format should be either \'j\' or \'t\'.')
    file_names = []
    with open(args.in_files_list, 'r') as ifile:
        for line in ifile:
            line = line.strip()
            if line:
                file_names.append(line)
    
    chromosomes = set()
    positions = dict()
    n_indv = len(file_names)
    breaks = [1, 5, 10, 15, 20, 25, 30, 50, 100]
    with ExitStack() as stack, pysam.BGZFile(args.out_file_name, 'w') as ofile:
        ifiles = [ stack.enter_context(gzip.open(file_name, 'rt')) for file_name in file_names ]
        if (args.output_format == 't'):
            ofile.write('CHROM\tBP\tMEAN\tMEDIAN\t{}\n'.format('\t'.join([f'PCT_INDV_OVER_{br}X' for br in breaks])).encode())
        while True:
            for i, ifile in enumerate(ifiles):
                line = ifile.readline()
                if line:
                    chromosome, position, dp = line.rstrip().split()
                    chromosomes.add(chromosome)
                    if len(chromosomes) > 1:
                        raise Exception(f'Multiple chromosomes detected in input files, but only one is allowed.')
                    positions.setdefault(int(position), []).append(int(dp))
            if not positions:
                    break
            min_position = sorted(positions)[0]
            depths = positions.pop(min_position)
            counts = [0] * len(breaks)
            for dp in depths:
                for i in range(0, len(breaks)):
                    if dp >= breaks[i]:
                        counts[i] += 1
            if (args.output_format == 't'):
                ofile.write('{}\t{:d}\t{:g}\t{:g}'.format(chromosome.replace('chr', '', 1), min_position, mean(depths), median(depths)).encode())
            else:
                ofile.write('{}\t{:d}\t{:d}\t{{"chrom":"{}","start":{:d},"end":{:d},"mean":{:g},"median":{:g}'.format(chromosome.replace('chr', '', 1), min_position, min_position, chromosome.replace('chr', '', 1), min_position, min_position, mean(depths), median(depths)).encode())
            for br, cnt in zip(breaks, counts):
                if (args.output_format == 't'):
                    ofile.write('\t{:g}'.format(cnt / n_indv).encode())
                else:
                    ofile.write(',"{:d}":{:g}'.format(br, cnt / n_indv).encode())

            if (args.output_format == 't'):
                    ofile.write('\n'.encode())
            else:
                    ofile.write('}\n'.encode())
    pysam.tabix_index(args.out_file_name, seq_col = 0, start_col = 1, end_col = 1, line_skip = 1, force = True)
