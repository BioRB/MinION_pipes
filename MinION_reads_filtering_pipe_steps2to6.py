# command : python MinION_reads_filtering_pipe_steps2to6.py MinION_raw_reads.fastq
# run this pipe on Slurm based cluster
import os
import subprocess
import sys
from subprocess import Popen
from Bio import SeqIO

fastq = sys.argv[1]  # fastq files all reads
SeqIO.convert(fastq, "fastq", "all_raw_reads.fasta", "fasta")
print("start Porechop")
os.system(
    "srun -A pc -J pc -c 35 --mem=150GB -t infinite --output=out.out --error=errs.txt bash -c 'porechop -i {} -o pc_reads.fastq.gz'".format(
        fastq))
print("finish porechop and start NanoFilt")
command = '''
gunzip -c pc_reads.fastq.gz | NanoFilt -q 10 -l 200 | gzip > NF_trimmed-reads.fastq.gz
'''
process = Popen(command, shell=True, stdout=subprocess.PIPE)
process.communicate()
print("finish NanoFilt and starting Filtlong")
command = '''
filtlong --min_length 200 --keep_percent 90 NF_trimmed-reads.fastq.gz  | gzip > icb2_fin_FL_output.fastq.gz
'''
process = Popen(command, shell=True, stdout=subprocess.PIPE)
process.communicate()
print("finish Filtlong and starting SPAdes")
command = '''
srun -A "R" -J "R" -c 74 --mem=250GB -t infinite --output=out.txt --error=errs.txt bash -c '/usr/bin/python2 /home/brancaccior/SPAdes-3.10.1-Linux/bin/spades.py --only-assembler --careful -s icb2_fin_FL_output.fastq.gz -t 74 -m 200 -k 21,33,55,77 -o ./spaout/ -t 74 -m 240'
'''
process = Popen(command, shell=True, stdout=subprocess.PIPE)
process.communicate()
print("finish SPAdes and starting CAP3")
command = '''
srun -A "R" -J "R" -c 15 --mem=100GB -t infinite --output=out.txt --error=errs.txt bash -c 'cap3 ./spaout/contigs.fasta > cap3out.out'
'''
process = Popen(command, shell=True, stdout=subprocess.PIPE)
process.communicate()
command = '''
mkdir -p second_cap3 | cp ./spaout/contigs.fasta.cap.contigs ./second_cap3
'''
process = Popen(command, shell=True, stdout=subprocess.PIPE)
process.communicate()
command = '''
srun -A "R" -J "R" -c 10 --mem=80GB -t infinite --output=out.txt --error=errs.txt bash -c 'cap3 ./second_cap3/contigs.fasta.cap.contigs > cap3out2.out'
'''
process = Popen(command, shell=True, stdout=subprocess.PIPE)
process.communicate()
command = '''
mkdir -p third_cap3 | cp ./second_cap3/contigs.fasta.cap.contigs.cap.contigs ./third_cap3
'''
process = Popen(command, shell=True, stdout=subprocess.PIPE)
process.communicate()
command = '''
srun -A "R" -J "R" -c 8 --mem=30GB -t infinite --output=out.txt --error=errs.txt bash -c 'cap3 ./third_cap3/contigs.fasta.cap.contigs.cap.contigs > cap3out3.out'
'''
process = Popen(command, shell=True, stdout=subprocess.PIPE)
process.communicate()
command = '''
mkdir -p forth_cap3 | cp ./third_cap3/contigs.fasta.cap.contigs.cap.contigs.cap.contigs ./forth_cap3
'''
process = Popen(command, shell=True, stdout=subprocess.PIPE)
process.communicate()
command = '''
srun -A "R" -J "R" -c 5 --mem=15GB -t infinite --output=out.txt --error=errs.txt bash -c 'cap3 ./forth_cap3/contigs.fasta.cap.contigs.cap.contigs.cap.contigs > cap3out4.out'
'''
process = Popen(command, shell=True, stdout=subprocess.PIPE)
process.communicate()
print("finish!")
sys.exit()


