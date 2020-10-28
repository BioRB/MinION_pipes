# command : python nanopolish_pipe_step9.py reads_file.fasta /fast5_foder_path draft_genome.fasta
# run this pipe on Slurm based clusters
import glob
import os
import subprocess
import sys
from subprocess import Popen
fasta = sys.argv[1] # fasta file all reads
fast5 = sys.argv[2] # fast5 folder
draft_g = sys.argv[3] # draft genome
os.system("fasta-splitter --n-parts 200 --out-dir ./nanopolished/splitted {}".format(fasta))
#transfer each file inside a directory with the same name of the file (200 different directories)
command = '''
for f in ./nanopolished/splitted/*; do mkdir "${f%.*}"; mv "$f" "${f%.*}"; done
'''
process = Popen(command, shell=True, stdout=subprocess.PIPE)
process.communicate()
diro = './nanopolished/splitted'
#do the following process in loop for all the 200 files created
for dirf in glob.glob(diro + '/*'):
    for filename in os.listdir(dirf):
        if filename.endswith(".fasta"):
            full_filename = dirf + '/' + filename
            os.system(
                "srun -A np -J np -c 20 --mem=80GB -t infinite --output=out.out --error=errs.txt bash -c 'nanopolish index -d {0} {1} '".format(
                    fast5, full_filename))
            os.system(
                "srun -A m -J M -c 20 --mem=80GB -t infinite --output=out.out --error=errs.txt bash -c 'minimap2 -ax map-ont -t 8 {0} {1} > {2}/{3}out.sam'".format(
                    draft_g, full_filename, dirf, filename))
            os.system(
                "srun -A m -J M -c 20 --mem=80GB -t infinite --output=out.out --error=errs.txt bash -c 'samtools sort -O bam -T {1}/sample.sort -o {0}.sort.bam {1}/*out.sam'".format(
                    full_filename, dirf))
            os.system("samtools index {0}/*sort.bam".format(dirf))
            os.system(
                "srun -A m -J M -c 40 --mem=150GB -t infinite --output=out.out --error=errs.txt bash -c 'nanopolish variants --consensus -o {0}/polished.vcf -r {1} -b {0}/*sort.bam -g {2}'".format(
                    dirf, full_filename, draft_g))
            os.system(
                "srun -A m -J M -c 40 --mem=150GB -t infinite --output=out.out --error=errs.txt bash -c 'nanopolish vcf2fasta --skip-checks -g {0} {1}/polished.vcf > {1}/polished_genome.fa'".format(
                    draft_g, dirf))
os.system(
    "find . -name 'polished_genome.fa' -exec cat {} + > all_seqs.fasta"
)
os.system(
    "srun -A m -J M -c 10 --mem=80GB -t infinite --output=out.out --error=errs.txt bash -c 'cap3 all_seqs.fasta > final_consensus.out'"
)

print("the final consensus in fasta format is in the file all_seqs.fasta.cap.contigs")
print("finish!!!!")

sys.exit()
