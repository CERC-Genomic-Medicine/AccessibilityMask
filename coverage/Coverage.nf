process pileup {

   errorStrategy "retry"
   maxRetries 3
   cache "lenient"
   cpus 1
   memory "4GB"
   time "1h"
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
   time "5d"
   //scratch true

   input:
   tuple val(chromosome), path(depth_files), path(depth_indices)

   output:
   tuple val(chromosome), path("${chromosome}.full.txt.gz")

   publishDir "result/aggregated/", pattern: "*.full.txt.gz*", mode: "copy"

   """
   find . -name "${chromosome}.*.depth.gz" > files_list.txt
   aggregate.py -f t -i files_list.txt -o ${chromosome}.full.txt.gz
   """
}

process calculate_stats {
   errorStrategy "finish"
   cache "lenient"
   cpus 1
   memory "4GB"
   time "3h"
   //scratch true

   input:
   tuple val(chromosome), path(aggregate_file)

   output:
   tuple val(chromosome), path("${chromosome}.${params.min_dp}_calculate_stats.txt")
   
   publishDir "result/aggregated/", pattern: "*.txt", mode: "copy"

   """
   calculate.py -i ${aggregate_file} -dp ${params.min_dp} -o ${chromosome}.${params.min_dp}_calculate_stats.txt
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
   tuple val(chromosome), path(aggregate_file), path(aggregate_index), path(stats)

   output:
   tuple val(chromosome), path("${chromosome}.${params.min_dp}_${params.min_pct_ind}.bed")

   publishDir "result/accessibility_mask/", pattern: "${chromosome}.${params.min_dp}_${params.min_pct_ind}.bed", mode: "copy"

   """
   if[-z ${params.min_pct_ind}]
   then 
       ${params.min_pct_ind} = \$(awk 'NR == 14 {print \$3}' ${stats})
   fi
   
   if[-z ${params.mean_dp}]
   then 
       ${params.mean_dp} = \$(awk 'NR == 6 {print \$3}' ${stats})
   fi
   
   High_coverage_bed.py -i ${aggregate_file} -dp ${params.min_dp} -ind ${params.min_pct_ind} -mdp ${params.mean_dp} -o ${chromosome}.${params.min_dp}_${params.min_pct_ind}_${params.mean_dp}.bed
   """
}


workflow {
   if[ -z ${params.bam_files}]
   then 
       aggregated_files = aggregate(params.depth_files)
       stats = calculate_stats(aggregated_files)
       combined_channel = aggregated_files.join(stats)
       create_accessibility_mask(combined_channel)
   else 
   then
       bam_files = Channel.fromPath(params.bam_files).map{ file -> [file, file + (file.getExtension() == "bam" ? ".bai" : ".crai")] }
       chromosomes = Channel.from(params.chromosomes)

       depth_files = pileup(bam_files, chromosomes)
       aggregated_files = aggregate(depth_files.groupTuple())
       stats = calculate_stats(aggregated_files)
       combined_channel = aggregated_files.join(stats)
       create_accessibility_mask(combined_channel)
   fi
}
