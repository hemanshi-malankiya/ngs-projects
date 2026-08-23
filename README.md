# Variant Calling Pipeline for E. coli Genome Using NGS Data

## Overview
This project identifies genetic variants in an E. coli sequencing sample by comparing it to a reference genome, using a standard NGS pipeline.

## Data
Reference genome: E. coli K-12 MG1655 (NCBI GCF_000005845.2)
Sequencing reads: SRA accession SRR2584863, subset to 50,000 read pairs

## Pipeline Steps
1. Quality control (FastQC)
2. Trimming (fastp)
3. Alignment (BWA-MEM)
4. Sorting and indexing (samtools)
5. Variant calling (bcftools)

## Results
27,124 total variants found: 26,989 SNPs and 135 indels.
Ts/Tv ratio: 2.61, consistent with expected bacterial genome values.

## Author
Hemanshi
