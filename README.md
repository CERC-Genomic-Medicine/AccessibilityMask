# Compute_Coverage

This pipeline generates high coverage regions from cram files.
in order to run the pipeline you will need to:


1- activate your python virtual environment.

2- install the following python modules:
  - pandas
  - pysam
  - statistics
  - numpy
  
3- install nextflow, samtools, and tabix.

4- put the nextflow.config file in the folder that you want to execute the pipeline in. 

5- modify the nextflow.config file based on your need.

6- load nextflow, samtools, and tabix

7- run the following command to submit the job to the compute canada:

  sbatch --account="name of the account" --time=168:00:00 --mem=4G -J coverage --wrap="nextflow run /path/to/AccessibilitMask/Coverage.nf" -o coverage.slurm.log
  
8- deactivate your python virtual environment.
