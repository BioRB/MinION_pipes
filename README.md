# MinION nanopore sequencing and assembly of a complete human papillomavirus genome: bioinformatics pipeline 

A pipeline developed to analyse MinION sequencing data for the reconstruction of viral genomes

## Description
<p align="center">
<img width="423" height="799" src="https://user-images.githubusercontent.com/43418626/97430029-91be2800-1918-11eb-87ec-c9f931ab4aaa.jpeg">

</p>

This pipeline was developed to analyse MinION sequencig raw data, to generate a consensus sequence for a viral genome.
This script perform a polishing of the raw data and generate a de novo assemblig using Canu tool. After, it takes the canu contigs and performs a step of polishing using Medaka tool. 

## Prerequisites
This pipe was written in python3
Guppy is required for the basecalling.
Nanofilt and filtlong are required for the filtering of the reads.
Canu is required for the assembling step.
Medaka is required for the polishing step.

## Installation
To run these scripts, each of the tools used needs to be installed before to launch the process.
Tools to install: Guppy, Nanofilt, Filtlong, Canu, Medaka.  
   
## Parameters
  * #### Mandatory
| Name  | Example value | Description     |
|------------|---------------|-----------------|

| fast5_path | path/to/file | path to fast5 files | 
| flowcell | flowcell code | the code of flowcell used (ex. FLO-MIN106) |
| kit | kit_used | the MinION kit used (ex. SQK-LSK109) |
| threads | nr. of threads (int)| threads to be used (ex. 8) |
| num | num_callers (int) | number of callers to use (ex. 8) |
| barcode | barcode kit code | the code of the barcodes kit used (ex. EXP-PBC001 ) |
| medaka_m | medaka model | define a model based on the basecaller (ex. r941_min_high_g303) - see medaka tool for more details - |

  * #### Flags

Flags are special parameters without value.

| Name      | Description     |
|-----------|-----------------|
| -h   | Display help |

## Usage 


Part5:
```
python3 MinION_pipe.py fast5_path flowcell kit threads num barcode medaka_m 
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
