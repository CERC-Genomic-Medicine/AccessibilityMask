# Accessibility Mask Pipeline

This repository provides a Nextflow pipeline for generating high-coverage regions from cram files, which can be valuable for downstream analyses.

## Introduction

The Accessibility Mask pipeline utilizes Python scripts and Nextflow to process cram files and identify high-coverage regions. By following a few simple steps, you can generate the accessibility mask for your genomic data.

## Pipeline Setup

To set up and run the pipeline, please follow these instructions:

1. **Python Virtual Environment**: Activate your Python virtual environment to ensure the required Python modules are installed correctly.

2. **Install Dependencies**: Install the following Python modules using the package manager of your choice:

   - pandas
   - pysam
   - statistics
   - numpy

3. **Install Nextflow, Samtools, and Tabix**: Ensure Nextflow, Samtools, and Tabix are installed on your system. You can find installation instructions for each tool in their respective documentation.

4. **Nextflow Configuration**: Place the provided `nextflow.config` file in the folder where you intend to execute the pipeline. Modify the `nextflow.config` file based on your specific requirements and settings.

5. **Load Dependencies**: Load Nextflow, Samtools, and Tabix in your environment to make them accessible during pipeline execution.

6. **Job Submission**: Submit the job to the Compute Canada cluster using the following command:

```bash
sbatch --account="name of the account" --time=168:00:00 --mem=4G -J coverage --wrap="nextflow run /path/to/AccessibilityMask/Coverage.nf" -o coverage.slurm.log
```
7. **Deactivate Virtual Environment**: After job submission, remember to deactivate your Python virtual environment to return to the original setting.

