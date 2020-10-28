import subprocess
from os import system
import argparse
parser = argparse.ArgumentParser(description='Assemble genome from MinION sequencing data')
parser.add_argument("--fast5_path", "-f5", help="path to fast5 files", type=str)
parser.add_argument("--flowcell", "-fc", help="the code of flowcell used (ex. FLO-MIN106)", type=str)
parser.add_argument("--kit", "-k", help="the MinION kit used (ex. SQK-LSK109)", type=str)
parser.add_argument("--threads", "-t", help="threads to be used (ex. 16)", type=int)
parser.add_argument("--num", "-n", help="number of callers to use (ex. 8)", type=int)
parser.add_argument("--barcode", "-bc", help="the code of the barcodes kit used (ex. EXP-PBC001 )", type=str)
parser.add_argument("--medaka_m", "-mm", help="define a model based on the basecaller (ex. r941_min_high_g303) see medaka tool for more details", type=str)
args = parser.parse_args()
subprocess.call(["guppy_basecaller", "--input_path", args.fast5_path, "--save_path", "./guppy_out", "--flowcell", args.flowcell,
                 "--kit", args.kit, "--cpu_threads_per_caller", args.threads, "--num_callers", args.num, "--barcode_kits", args.barcode,
                 "--trim_barcodes"])
subprocess.call(["find", "./guppy_out/", "-name", "*.fastq", "-exec", "cat", "{}", "+", ">", "run_all.fastq"])
system('paste - - - - < run_all.fastq | cut -f 1,2 | sed "s/^@/>/" | tr "\t" "\n" | sed "s/ //g" > run_all.fasta')
system('NanoFilt sequences.fastq --maxlength 8000 | gzip > NF_trimmed-reads.fastq.gz && filtlong --min_length 7000 '
       '--keep_percent 10 NF_trimmed-reads.fastq.gz | gzip > FL_output.fastq.gz')
system('canu -p run -d canu -nanopore-corrected FL_output.fastq.gz -genomesize=8k –assemble')
subprocess.call(['medaka_consensus', '-i', 'FL_output.fastq.gz', '-d', './canu/*.contigs.fasta', '-o', 'medaka-out',
                 '-t', args.threads, '-m', args.medaka_m])
print("you can find the final consensus sequence inside the folder medaka-out. The name of the file is consensus.fasta"
      "Bye!")
