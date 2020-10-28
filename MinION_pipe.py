import sys
import subprocess
from os import system

fast5_path = sys.argv[1]
flowcell = sys.argv[2]
kit = sys.argv[3]
threads = sys.argv[4]
num = sys.argv[5]
barcode = sys.argv[6]
medaka_m = sys.argv[7]
subprocess.call(["guppy_basecaller", "--input_path", fast5_path, "--save_path", "./guppy_out", "--flowcell", flowcell,
                 "--kit", kit, "--cpu_threads_per_caller", threads, "--num_callers", num, "--barcode_kits", barcode,
                 "--trim_barcodes"])
subprocess.call(["find", "./guppy_out/", "-name", "*.fastq", "-exec", "cat", "{}", "+", ">", "run_all.fastq"])
system('paste - - - - < run_all.fastq | cut -f 1,2 | sed "s/^@/>/" | tr "\t" "\n" | sed "s/ //g" > run_all.fasta')
system('NanoFilt sequences.fastq --maxlength 8000 | gzip > NF_trimmed-reads.fastq.gz && filtlong --min_length 7000 '
       '--keep_percent 10 NF_trimmed-reads.fastq.gz | gzip > FL_output.fastq.gz')
system('canu -p run -d canu -nanopore-corrected FL_output.fastq.gz -genomesize=8k –assemble')
subprocess.call(['medaka_consensus', '-i', 'FL_output.fastq.gz', '-d', './canu/*.contigs.fasta', '-o', 'medaka-out',
                 '-t', threads, '-m', medaka_m])
print("you can find the final consensus sequence inside the folder medaka-out. The name of the file is consensus.fasta"
      "Bye!")
