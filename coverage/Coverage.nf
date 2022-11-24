process pileup {

  input:
  // get ID, ID.cram, and ID.cram.crai from glob of crams
  tuple val(name), file(cram), file(crai) from Channel 
                                                 .fromPath(params.cram_files)
                                                 .map{ ["${it.getSimpleName()}",
                                                        file("${it}"),
                                                        file("${it}.crai")] }
  each chromosome from Channel.from(params.chromosomes)


  output:
  tuple val(chromosome),
        file("${chromosome}.${name}.depth.gz"), 
        file("${chromosome}.${name}.depth.gz.tbi") into pileups

  publishDir "result/depth/${chromosome}", pattern: "*.depth*", mode: "copy"

  """
  samtools depth -a -s -q20 -Q20 -r ${chromosome} ${cram}  |\
     bgzip > ${chromosome}.${name}.depth.gz
  tabix -s1 -b2 -e2 ${chromosome}.${name}.depth.gz
  """
}
process aggregate {
   input:
   tuple val(chromosome), file(depth_files), file(depth_tbis) from pileups.groupTuple()

   output:
   tuple val(chromosome), file("${chromosome}.full.json.gz"), file("${chromosome}.full.json.gz.tbi") into aggregated mode flatten

   publishDir "result/full/${chromosome}", pattern: "*.full.json.gz*", mode: "copy"

   """
   find . -name "${chromosome}.*.depth.gz" > files_list.txt
   aggregate.py -i files_list.txt -o ${chromosome}.full.json.gz
   """
}

process extract_high_coverage{
    input:
    tuple val(chromosome), file(aggregate_file), file(aggregate_tbi) from aggregated 

    output:
    tuple val(chromosome), file("*.txt") into high_cov

    publishDir "result/full/${chromosome}/high_cov_regions", pattern: "*.txt", mode: "copy"

    """
    high_coverage_regions_json.py -i $aggregate_file -dp "10" -ind 1 -o ${chromosome}.high_coverage_over_10X_all_inds.txt
    """
}