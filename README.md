# MinION nanopore sequencing and assembly of a complete human papillomavirus genome: bioinformatics pipeline 

A pipeline developed to analyse MinION sequencing data for the reconstruction of viral genomes

## Description
![alt text](https://github.com/BioRB/MinION_pipes/blob/master/Figure1.tif)

This pipeline was developed to analyse MinION sequencig raw data. It is composed of 4 parts:
Part 1: Basecalling and demultiplexing [Guppy]
Part 2: Filtering and assembling [Porechop, Nanofilt, Filtlong, SPAdes, CAP3]
Here a python script that includes all these tools: MinION_reads_filtering_pipe_steps2to6.py 
This script perform a polishing of the raw data and generate a first de novo assemblig using SPAdes tool. After, it takes the SPAdes contigs and performs a second step of de novo assembling using CAP3. Four consecutive assembling steps
are performed using CAP3.
Part 3: The contigs generate from CAP3 (all the four files generated in the four consecutive CAP3 assembling steps) are used to manually reconstruct the viral genome, using BLAST and MUSCLE allignment tools, to identify the contigs and allowing a proper reconstruction of the whole genome of the virus. 
Part 4: Once the whole genome of the virus have been reconstructed this draft sequence is polished using DraftPolisher that correct eventual errors occurred during the assembling of the contigs. At this purpose, the SPAdes consensus sequences are used as reference database to perform this consensus level polishing of the draft sequence.
Part 5: The polished draft genome is passed trough a second step of polishing, this time at signal-level, by using a Nanopolish-based python script: nanopolish_pipe_step9.py  
## Prerequisites
We used a Slurm based cluster to perform our analyses thus all of our scripts are designed to run on this kind of architecture.

## Installation
To run these scripts, each of the tools used needs to be installed before to launch the process.
Tools to install: Guppy V3.1.5+, Porechop V0.2.4, Nanofilt V2.2.0, Filtlong V0.2.0, SPAdes V3.10.1, CAP3 02/10/15, BLAST V2.9.0+, MUSCLE V3.8.1551, Nanopolish V0.11.0, Minimap2 V2.15, Samtools version 1.9.   
Details on DraftPolisher installation and use are present here :[https://github.com/BioRB/DraftPolisher]   

## Usage 

Part 1:
```
srun -A "minion" -J "minion" -c 40 --mem=250GB -t infinite --output=out.txt --error=errs.txt bash -c 'guppy_basecaller –i fast5_folder -s guppy_out --flowcell FLO-MIN106 --kit SQK-LSK109 --cpu_threads_per_caller 70 --num_callers 8 --barcode_kits EXP-PBC001 --trim_barcodes'
```

Part 2:
```
python MinION_reads_filtering_pipe_steps2to6.py MinION_raw_reads.fastq
```
Part 3:
```
'blastn -db nt -query cap3out.fasta -out blast.out -task blastn -outfmt "6 qseqid qlen evalue bitscore score pident mismatch gaps ppos staxid ssciname scomname sblastname stitle sskingdom qstart qend sstart send" -max_target_seqs 1  -num_threads 78
```
```
'muscle -clw -in cap3out.fasta -out muscle.out
```
Part4:
```
python DraftPolisher_cov.py -q query.fa -s subject.fa -f reads.fa -k 8
```
Part5:
```
python nanopolish_pipe_step9.py raw_reads.fasta /path_to_fast5 draft_genome.fasta
```

## Contributions

| Name      | Email | Description     |
|-----------|---------------|-----------------|
  | Rosario Nicola Brancaccio | rosariobrancaccio@yahoo.it | Developer to contact for support |
  | Massimo Tommasino | tommasinom@iarc.fr
  | Tarik Gheit | gheitt@iartc.fr
  

## Authors

**Rosario Nicola Brancaccio** - (https://github.com/BioRB/)

## License
[GNU General Public License, version 3](https://www.gnu.org/licenses/gpl-3.0.html)



## References
