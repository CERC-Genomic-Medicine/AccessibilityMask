#!/usr/bin/env python

import argparse
import gzip


argparser = argparse.ArgumentParser(description = 'This script generates continuous regions where depth of coverage was similar across all individuals.')
argparser.add_argument('-i', '--input-file', metavar = 'file', dest = 'in_file_path', type = str, required = True, help = 'Tab-delimited file containing coverage metrics of each base pair position. Required column names: #CHROM, BP, MEAN, MEDIAN, PCT_INDV_OVER_1X, PCT_INDV_OVER_5X, PCT_INDV_OVER_10X, PCT_INDV_OVER_15X, PCT_INDV_OVER_20X, PCT_INDV_OVER_25X, PCT_INDV_OVER_30X, PCT_INDV_OVER_50X, PCT_INDV_OVER_100X.')
argparser.add_argument('-c', '--column-name', metavar = 'name', dest = 'in_column_name', type = str, default = 'PCT_INDV_OVER_10X', choices = ['PCT_INDV_OVER_1X', 'PCT_INDV_OVER_5X', 'PCT_INDV_OVER_10X', 'PCT_INDV_OVER_15X', 'PCT_INDV_OVER_20X', 'PCT_INDV_OVER_25X', 'PCT_INDV_OVER_30X', 'PCT_INDV_OVER_50X', 'PCT_INDV_OVER_100X'], required = False, help = 'Column name for the `-m/--min-pct-ind` filter. Default: `PCT_INDV_OVER_10X`')
argparser.add_argument('-m', '--min-pct-ind', metavar = 'number', dest = 'in_min_pct_ind', type = float, required = True, help = 'Minimal percent of individuals in the PCT_INDV_OVER_[1-100]X column (percent of individuals with depth of coverage over 1,5,..,100X). Must be between 0 and 1.')
argparser.add_argument('-M', '--max-mean-dp', metavar = 'number', dest = 'in_max_mean_depth', type = float, required = True, help = 'Maximal depth of coverage in the MEAN column (average depth across all individuals).')
argparser.add_argument('-o', '--output', metavar = 'file', dest = 'out_file_path', type = str, required = True, help = 'Output BED file with regions satisfying the specified depth of coverage thresholds.')


def make_bed(column_name, path_read, path_write,  min_percent = 1, max_depth = 100):
    with gzip.open(path_read, 'rt') as fr, open(path_write, 'w') as fw:
        header = fr.readline().rstrip().split()
        if column_name not in header:
            raise Exception(f'{column_name} is not in the header.')
        chrom_colindex = header.index('CHROM') 
        bp_colindex = header.index('BP')
        mean_dp_colindex = header.index('MEAN')
        pct_colindex = header.index(column_name)
        range_start = previous_number = -1
        for line in fr:
            columns = line.rstrip().split()
            chrom = columns[chrom_colindex]
            bp = int(columns[bp_colindex]) - 1
            pct = float(columns[pct_colindex])
            mean_dp = float(columns[mean_dp_colindex])
            if (pct >= min_percent) and (mean_dp <= max_depth): 
                if (range_start == -1):
                    range_start = previous_number = bp
                else:
                    if (bp == previous_number + 1):
                        previous_number = bp
                    else:
                        fw.write(f"{chrom}\t{range_start}\t{previous_number + 1}\n")
                        range_start = previous_number = bp
        if(range_start != -1):
            fw.write(f"{chrom}\t{range_start}\t{previous_number + 1}\n")
        

if __name__ == "__main__":
    args = argparser.parse_args()
    if ((args.in_min_pct_ind > 1) or (args.in_min_pct_ind < 0)):
        raise Exception("-m/--min-pct-ind must be between 0 and 1.")
    make_bed(args.in_column_name, args.in_file_path, args.out_file_path, min_percent = args.in_min_pct_ind, max_depth = args.in_max_mean_depth)
    
