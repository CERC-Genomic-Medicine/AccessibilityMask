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
   time "3h"
   //scratch true

   input:
   tuple val(chromosome), path(depth_files), path(depth_indices)

   output:
   path("${chromosome}.full.txt.gz")

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
   path(aggregate_file)

   output:
   tuple path("${aggregate_file.getSimpleName()}.${params.min_dp}_calculate_stats.txt"), path(aggregate_file)
   
   publishDir "result/stats/", pattern: "*.txt", mode: "copy"

   """
   calculate.py -i ${aggregate_file} -dp ${params.min_dp} -o ${aggregate_file.getSimpleName()}.${params.min_dp}_calculate_stats.txt
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
   tuple  path(stats), path(aggregate_file)

   output:
   path("*.bed")

   publishDir "result/accessibility_mask/", pattern: "*.bed", mode: "copy"

   """
   if[${params.load_params} == "true"]
   then
       min_pct_ind=\$(grep "^5%" ${stats} | cut -f3)
       mean_dp=\$(grep "99%" ${stats} | cut -f2)
       high_coverage_regions.py -i ${aggregate_file} -dp ${params.min_dp} -ind "\${min_pct_ind}" -mdp "\${mean_dp}" -o ${aggregate_file.getSimpleName()}.${params.min_dp}_"\${min_pct_ind}"_"\${mean_dp}".bed
   else
       high_coverage_regions.py -i ${aggregate_file} -dp ${params.min_dp} -ind ${params.min_pct_ind} -mdp ${params.mean_dp} -o ${aggregate_file.getSimpleName()}.${params.min_dp}_${params.min_pct_ind}_${params.mean_dp}.bed
   fi
   """
}


workflow {

    if(params.skip == false){
       bam_files = Channel.fromPath(params.bam_files).map{ file -> [file, file + (file.getExtension() == "bam" ? ".bai" : ".crai")] }
       chromosomes = Channel.from(params.chromosomes)

       depth_files = pileup(bam_files, chromosomes)
       aggregated_files = aggregate(depth_files.groupTuple())
       stats = calculate_stats(aggregated_files)
       create_accessibility_mask(stats)
   }else{
       aggregated_files = Channel.from(params.depth_files)
       stats = calculate_stats(aggregated_files)
       create_accessibility_mask(stats)
   }

}
