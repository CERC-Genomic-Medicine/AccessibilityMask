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

  publishDir "result/${chromosome}", pattern: "*.depth*"

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
   tuple val(chromosome), file("${chromosome}.full.json.gz"), file("${chromosome}.full.json.gz.tbi") into aggregated

   publishDir "result/full", pattern: "*.full.json.gz*"

   """
   find . -name "${chromosome}.*.depth.gz" > files_list.txt
   aggregate.py -i files_list.txt -o ${chromosome}.full.json.gz
   """
}

process prune {
   input:
   set val(chromosome), file(full_json), file(full_json_tbi) from aggregated
   each limit from Channel.from(params.prune_limits)

   output:
   tuple file("${chromosome}.bin_${limit}.json.gz"), file("${chromosome}.bin_${limit}.json.gz.tbi")

   publishDir "result/bin_${limit}", pattern: "*.bin_*.json.gz*"

   """
   prune.py -i ${full_json} -l ${limit} -o ${chromosome}.bin_${limit}.json.gz
   """
}
