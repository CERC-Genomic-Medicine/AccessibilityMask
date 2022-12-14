# Compute_Coverage

This pipeline generates high coverage regions from cram files.
in order to run the pipeline you will need to:

1- install the following python modules:
  - pandas
  - pysam
  - statistics
  - numpy
  
2- install nextflow, samtools, and tabix.

3- put the nextflow.config file in the folder that you want to execute the pipeline in. 

4- modify the nextflow.config file based on your need.

5- load nextflow, samtools, and tabix

6- run the following command:

    nextflow run path/to/Compute_Coverage/coverage/Coverage.nf
