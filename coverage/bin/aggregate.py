#!/usr/bin/env python

import argparse
import gzip
from contextlib import ExitStack
import pysam
from statistics import mean, median


argparser = argparse.ArgumentParser(description = 'Aggregate depth information (output as JSON) from individual depth files (generated using SAMtools mpileup).')
argparser.add_argument('-i', '--in', metavar = 'file', dest = 'in_files_list', required = True, help = 'Input file which lists all depth files (one depth file per sample) generated using SAMtools mpileup. One file per line.')
argparser.add_argument('-o', '--out', metavar = 'file', dest = 'out_file_name', required = True, help = 'Output file of depth information compressed with bgzip. In addition to this file, the tabix index will be produced.')
argparser.add_argument('-f', '--flag', metavar = 'string', dest = 'output_type_flag', required = True, help = 'Flag identifies the type of output file whether it is a json file or a tsv file. Flag value should be either \'j\' indicate json format or \'t\' indicate tsv format.')

if __name__ == '__main__':
    args = argparser.parse_args()
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
        if(args.output_type_flag == 't'):
                ofile.write('#CHROM\tBP\tMEAN\tMEDIAN\tPCT_INDV_OVER_1X\tPCT_INDV_OVER_5X\tPCT_INDV_OVER_10X\tPCT_INDV_OVER_15X\tPCT_INDV_OVER_20X\tPCT_INDV_OVER_25X\tPCT_INDV_OVER_30X\tPCT_INDV_OVER_50X\tPCT_INDV_OVER_100X\n'.encode())
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
            if(args.output_type_flag == 't'):
                ofile.write('{}\t{:d}\t{:g}\t{:g}'.format(chromosome.replace('chr', '', 1), min_position, mean(depths), median(depths)).encode())
            else:
                ofile.write('{}\t{:d}\t{:d}\t{{"chrom":"{}","start":{:d},"end":{:d},"mean":{:g},"median":{:g}'.format(chromosome.replace('chr', '', 1), min_position, min_position, chromosome.replace('chr', '', 1), min_position, min_position, mean(depths), median(depths)).encode())
            for br, cnt in zip(breaks, counts):
                if(args.output_type_flag == 't'):
                    ofile.write('\t{:g}'.format(cnt / n_indv).encode())
                else:
                    ofile.write(',"{:d}":{:g}'.format(br, cnt / n_indv).encode())

            if(args.output_type_flag == 't'):
                    ofile.write('\n'.encode())
            else:
                    ofile.write('}\n'.encode())
        pysam.tabix_index(args.out_file_name, seq_col = 0, start_col = 1, end_col = 1, force = True)
