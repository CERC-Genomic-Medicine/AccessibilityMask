process pileup {

   errorStrategy "retry"
   maxRetries 3
   cache "lenient"
   cpus 1
   memory "4GB"
   time "4h"
   scratch true

   input:
   tuple path(bam), path(bam_index)
   each chromosome

   output:
   tuple val(chromosome),
      path("${chromosome}.${bam.getSimpleName()}.depth.gz"), 
      path("${chromosome}.${bam.getSimpleName()}.depth.gz.tbi")

    publishDir "result/depth/${chromosome}", pattern: "*.depth*", mode: "copy"

    """
    samtools depth -a -s -q20 -Q20 -r ${chromosome} ${bam} | bgzip > ${chromosome}.${bam.getSimpleName()}.depth.gz
    tabix -s1 -b2 -e2 ${chromosome}.${bam.getSimpleName()}.depth.gz
    """
}


process aggregate {
   
   errorStrategy "finish"
   cache "lenient"
   cpus 1
   memory "8GB"
   time "2d"
   //scratch true

   input:
   tuple val(chromosome), path(depth_files), path(depth_indices)

   output:
   tuple val(chromosome), path("${chromosome}.full.json.gz"), path("${chromosome}.full.json.gz.tbi")

   publishDir "result/aggregated/", pattern: "*.full.json.gz*", mode: "copy"

   """
   find . -name "${chromosome}.*.depth.gz" > files_list.txt
   aggregate.py -i files_list.txt -o ${chromosome}.full.json.gz
   """
}


process create_accessibility_mask {

   errorStrategy "finish"
   cache "lenient"
   cpus 1
   memory "4GB"
   time "1h"
   //scratch true

   input:
   tuple val(chromosome), path(aggregate_file), path(aggregate_index)

   output:
   tuple val(chromosome), path("${chromosome}.${params.min_dp}_${params.min_pct_ind}.bed")

   publishDir "result/accessibility_mask/", pattern: "${chromosome}.${params.min_dp}_${params.min_pct_ind}.bed", mode: "copy"

   """
   high_coverage_regions_json.py -i ${aggregate_file} -dp ${params.min_dp} -ind ${params.min_pct_ind} -o ${chromosome}.${params.min_dp}_${params.min_pct_ind}.bed
   """
}


workflow {
   bam_files = Channel.fromPath(params.bam_files).map{ file -> [file, file + (file.getExtension() == "bam" ? ".bai" : ".crai")] }
   chromosomes = Channel.from(params.chromosomes)

   depth_files = pileup(bam_files, chromosomes)
   aggregated_files = aggregate(depth_files.groupTuple())

   create_accessibility_mask(aggregated_files)
}
