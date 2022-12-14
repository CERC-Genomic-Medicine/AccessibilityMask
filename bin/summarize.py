#!/usr/bin/env python

import argparse
import pandas as pd
import numpy as np


argparser = argparse.ArgumentParser(description = 'This script computes summary statistics from aggregated depth files.')
argparser.add_argument('-i', '--input-file', metavar = 'file', dest = 'in_file_path', type = str, required = True, help = 'Tab-delimited file containing coverage metrics of each base pair position. Required column names: #CHROM, BP, MEAN, MEDIAN, PCT_INDV_OVER_1X, PCT_INDV_OVER_5X, PCT_INDV_OVER_10X, PCT_INDV_OVER_15X, PCT_INDV_OVER_20X, PCT_INDV_OVER_25X, PCT_INDV_OVER_30X, PCT_INDV_OVER_50X, PCT_INDV_OVER_100X.')
argparser.add_argument('-c', '--column-name', metavar = 'name', dest = 'in_column_name', type = str, default = 'PCT_INDV_OVER_10X', choices = ['PCT_INDV_OVER_1X', 'PCT_INDV_OVER_5X', 'PCT_INDV_OVER_10X', 'PCT_INDV_OVER_15X', 'PCT_INDV_OVER_20X', 'PCT_INDV_OVER_25X', 'PCT_INDV_OVER_30X', 'PCT_INDV_OVER_50X', 'PCT_INDV_OVER_100X'], required = False, help = 'Column name for which to compute summary statistics. `MEAN` is always included. Default: `PCT_INDV_OVER_10X`')
argparser.add_argument('-o', '--output-file', metavar = 'file', dest = 'out_file_path', type = str, required = True, help = 'Output file containing summary statistics.')

    
if __name__ == "__main__":
    args = argparser.parse_args()
    df = pd.read_csv(args.in_file_path, sep = '\t', usecols = ['MEAN', args.in_column_name], dtype = {'MEAN': np.float32, args.in_column_name: np.float32})
    summary = df.describe(percentiles = [0.001, 0.005, 0.01, .05, .1, .5, 0.25, 0.75, 0.95, 0.99, 0.995, 0.999, 1])
    summary.to_csv(args.out_file_path, sep = '\t')

