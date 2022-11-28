import pandas as pd
import sys
import argparse

argparser = argparse.ArgumentParser(description = 
 'This script makes bed files from depth files generated by coverage pipeline!')

argparser.add_argument('-i', '--input-file', metavar = 'file', dest = 'in_path', type = str, required = True, help = 'File containing coverage of each variant and percent of individuals havingthat variant with specified coverage.')
argparser.add_argument('-dp', '--min-dp', metavar = 'number', dest = 'in_depth', type = int, required = True, help = 'Minimum depth considering as high coverage threshold, must be one of the elements of following list [5X, 10X, 15X, 20X, 25X, 30X, 50X, 100X].')
argparser.add_argument('-ind', '--pct-ind', metavar = 'number', dest = 'in_pct', type = int, required = True, help = 'Minimum percentile of individuals with the mentioned depth threshold, should be between 0 and 1.')
argparser.add_argument('-o', '--output', metavar = 'file', dest = 'out_file_path', type = str, required = True, help = 'Output bed file containing high coverage files.')

def load_coverage_data(path_read = '/path/to/depth/data', path_write='/path/to/bed/file',  min_depth = "10X", min_percent = 1):
    if ((min_percent > 1) or (min_percent < 0)):
        raise Exception("minimal percentile of individuals over minimum depth should be between 0 and 1.")
        
    column_name = f'PCT_INDV_OVER_{min_depth}'
        
    with open(path_read, 'r') as fr, open(path_write, 'w') as fw:
        fw.write(f'chrom\tchromStart\tchromEnd\n')
        header = fr.readline().rstrip().split()
        if column_name not in header:
            raise Exception(f'{column_name} is not in the header.')
        chrom_colindex = header.index('CHROM') 
        bp_colindex = header.index('BP')
        pct_colindex = header.index(column_name)
        range_start = previous_number = -1
        for line in fr:
            columns = line.rstrip().split()
            chrom = columns[chrom_colindex]
            bp = int(columns[bp_colindex]) - 1
            pct = float(columns[pct_colindex])
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
        
if __name__ == "__main__":
    args = argparser.parse_args()
    depth_file = args.in_path
    min_depth = args.in_depth
    pct_ind = args.in_pct
    out_file_path = args.out_file_path
    load_coverage_data(path_read = depth_file, path_write = out_file_path, min_depth = min_depth, min_percent = min_percent)
    exit()
    