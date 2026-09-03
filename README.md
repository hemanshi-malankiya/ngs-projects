# Variant Calling Pipeline for E. coli Genome Using NGS Data

## Key Results

- 50,000 read pairs (100,000 total reads) were selected for analysis
- [X] reads ([X]%) passed quality filtering after trimming
- 94.31% of reads were mapped successfully to the *E. coli* reference genome
- 91.54% of read pairs were properly paired after alignment
- Base quality (Q30) improved from [X]% to [X]% (Read 1) and [X]% to [X]% (Read 2) after trimming
- 26,870 raw variant sites were identified: 26,738 SNPs and 132 indels
- 3,579 filtered variant sites remained after quality/depth filtering: 3,551 SNPs and 28 indels
- [X] Transition/Transversion (Ts/Tv) ratio
- 6 stop-gain variants were identified and annotated using SnpEff
- The *ydbD* p.Ser37* variant was prioritized as a major candidate because the predicted premature stop could eliminate approximately 95.3% of the 768-aa protein

---

## Project Overview

This project implements a complete Next-Generation Sequencing (NGS) variant-calling pipeline. It identifies single nucleotide polymorphisms (SNPs) and small insertions/deletions (indels) in an *E. coli* sequencing sample by comparing it against the *E. coli* K-12 MG1655 reference genome.

The project demonstrates practical NGS data analysis using standard bioinformatics tools, including quality control, read trimming, sequence alignment, BAM processing, haploid variant calling, variant filtering, and functional annotation.

---

## Biological Question

How does the genome of the sequenced *E. coli* sample differ from the reference *E. coli* K-12 MG1655 genome, and what potentially important functional variants can be identified from these differences?

---

## Dataset

- **Reference genome:** *E. coli* K-12 MG1655
- **NCBI assembly:** GCF_000005845.2
- **Chromosome:** NC_000913.3
- **Genome size:** ~4.64 Mb
- **Sequencing reads:** SRA accession SRR2584863
- **Sequencing platform:** Illumina paired-end
- **Subset analyzed:** First 50,000 read pairs (100,000 total reads)
- **Data source:** NCBI Sequence Read Archive (SRA) and NCBI Genome database

A subset of the sequencing reads was used to make the analysis practical and reproducible on a personal computer.

---

## Tools Used

| Tool | Version | Purpose |
|------|---------|---------|
| FastQC | 0.12.1 | Raw and trimmed read quality assessment |
| fastp | 1.3.6 | Read trimming and adapter removal |
| BWA | 0.7.19 | Read alignment to reference genome |
| SAMtools | 1.23.1 | BAM conversion, sorting and indexing |
| BCFtools | 1.22 | Haploid variant calling, filtering and statistics |
| SRA Toolkit | 3.4.1 | Downloading sequencing data from NCBI SRA |
| SnpEff | 5.2f | Functional annotation of variants |
| Python | 3.x | Supporting analysis |

---

## Workflow

1. **Quality Control** — FastQC evaluates sequencing read quality and identifies issues such as low-quality bases and adapter contamination.
2. **Trimming** — fastp removes adapter sequences and low-quality bases.
3. **Alignment** — BWA-MEM aligns cleaned reads against the *E. coli* K-12 MG1655 reference genome.
4. **Sorting & Indexing** — SAMtools converts SAM to BAM and creates sorted, indexed alignment files.
5. **Variant Calling** — BCFtools identifies SNPs and indels.
6. **Haploid Calling** — BCFtools is configured with `--ploidy 1` because *E. coli* is haploid.
7. **Variant Filtering** — Variants are filtered using quality and read-depth thresholds.
8. **Functional Annotation** — SnpEff predicts the functional consequences of the filtered variants.

```text
                  E. coli NGS Reads
                         |
                         v
                  Quality Control
                     (FastQC)
                         |
                         v
                Adapter/Quality Trimming
                       (fastp)
                         |
                         v
                  Reference Alignment
                     (BWA-MEM)
                         |
                         v
                  BAM Processing
                    (samtools)
                         |
                         v
                  Variant Calling
                    (bcftools)
                   --ploidy 1
                         |
                         v
                 Variant Filtering
                         |
                         v
                 SnpEff Annotation
                         |
                         v
              Functional Variant Analysis
```

---

## Installation

```bash
git clone https://github.com/hemanshi-malankiya/ngs-projects.git
cd ngs-projects

conda create -n ngs python=3.10 -y
conda activate ngs

conda install -c bioconda -c conda-forge \
  fastqc fastp bwa samtools bcftools sra-tools -y
```

SnpEff was installed separately and configured with the E. coli K-12 MG1655 GenBank annotation.

---

## How to Run

### 1. Download the Reference Genome

Download the E. coli K-12 MG1655 reference genome into `ref/`:

```bash
wget -P ref/ https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.fna.gz

gunzip ref/*.fna.gz
```

### 2. Download Sequencing Reads

The SRR2584863 dataset was downloaded from the NCBI SRA:

```bash
prefetch SRR2584863 -O raw_data/

fasterq-dump --split-files -e 4 -X 100000 \
  raw_data/SRR2584863/SRR2584863.sra \
  -O raw_data/
```

This extracts the first 100,000 reads, corresponding to approximately 50,000 paired-end read pairs.

### 3. Run the Pipeline

Run the scripts in order:

```bash
bash scripts/01_qc.sh
bash scripts/02_trim.sh
bash scripts/03_align.sh
bash scripts/04_sort_index.sh
bash scripts/05_call_variants.sh
bash scripts/06_filter_variants.sh
```

### 4. Annotate Variants

SnpEff was used to annotate the filtered variants:

```bash
snpEff -c snpEff.config \
  -dataDir ./data \
  ecoli_mg1655 \
  results/variants_filtered.vcf \
  > results/variants_annotated.vcf
```

---

## Results

### Alignment Statistics

| Metric | Result |
|--------|--------|
| Total reads in BAM | 81,492 |
| Primary reads | 80,806 |
| Mapped reads | 76,854 |
| Mapping rate | 94.31% |
| Properly paired | 91.54% |
| Singletons | 0.58% |
| Average coverage depth | 2.30x |
| Reference positions covered ≥1x | 81.41% |

The relatively low average sequencing depth should be considered when interpreting the detected variants.

> **Note:** the alignment shows 81,492 total BAM reads rather than the full 100,000 originally downloaded. This is expected — some reads are removed during trimming/filtering — but it should be verified against the fastp log before finalizing, so the Key Results section accurately reflects what was actually analyzed versus what was downloaded.

### Variant Statistics

**Raw Variant Calls**

| Metric | Count |
|--------|-------|
| Total variant sites | 26,870 |
| SNPs | 26,738 |
| Indels | 132 |
| Multiallelic sites | 0 |
| Transition/Transversion (Ts/Tv) ratio | [X] |

**Filtered Variant Calls**

| Metric | Count |
|--------|-------|
| Total variant sites | 3,579 |
| SNPs | 3,551 |
| Indels | 28 |
| Multiallelic sites | 0 |
| Transition/Transversion (Ts/Tv) ratio | [X] |

Variants were filtered using:
- `QUAL >= 20`
- `INFO/DP >= 5`

### Functional Annotation

The filtered variants were functionally annotated using SnpEff.

**Major Variant Consequences**

| Effect | Count |
|--------|-------|
| Synonymous variant | 2,660 |
| Missense variant | 476 |
| Upstream gene variant | 423 |
| Stop gained | 6 |
| Splice region & stop retained | 3 |
| Frameshift variant | 3 |
| Downstream gene variant | 3 |
| Disruptive in-frame deletion | 2 |
| Stop lost & splice region | 1 |
| Start lost | 1 |
| Disruptive in-frame insertion | 1 |

### Candidate Stop-Gain Variants

Six stop-gain variants were identified in the filtered variant set.

| Gene | Variant | Protein Length | Approx. Protein Lost |
|------|---------|-----------------|------------------------|
| ydbD | p.Ser37* | 768 aa | 95.3% |
| creD | p.Trp190* | 450 aa | 58.0% |
| yzcX | p.Leu76* | 161 aa | 53.4% |
| yzcX | p.Leu120* | 161 aa | 26.1% |
| tsx | p.Trp258* | 294 aa | 12.6% |
| hyfD | p.Gln479* | 479 aa | ~0.2% |

### Prioritized Candidate: *ydbD* p.Ser37*

The *ydbD* p.Ser37* variant was prioritized for further investigation.

- **Gene:** ydbD
- **Protein:** DUF2773 domain-containing protein YdbD
- **Protein length:** 768 aa
- **Variant:** p.Ser37*
- **Approximate protein sequence lost:** 95.3%

The premature stop occurs very early in the protein and could result in a substantially truncated protein.

This variant is considered a **candidate** functional variant, rather than a confirmed damaging mutation, because the sequencing dataset has relatively low coverage.

### Coverage

The alignment showed:

- Average depth: 2.30x
- Genome positions covered ≥1x: 81.41%
- Genome positions covered ≥5x: 12.14%
- Genome positions covered ≥10x: 0.26%

The low coverage is an important limitation of this analysis and means that some genomic regions may have insufficient evidence for confident variant detection.

### Read Quality Improvement (fastp Trimming)

| Metric | Before Trimming | After Trimming |
|--------|-------------------|-------------------|
| Read 1 Q30 bases | [X]% | [X]% |
| Read 2 Q30 bases | [X]% | [X]% |
| Reads passing filter | - | [X] / 100,000 |

The exact Q30 and filtering values should be taken directly from the fastp JSON or HTML report rather than estimated.

### Variant Support

The prioritized stop-gain variants had the following read-depth support:

| Gene | Variant | DP |
|------|---------|----|
| ydbD | p.Ser37* | 7x |
| hyfD | p.Gln479* | 6x |
| yzcX | p.Leu76* | 5x |
| yzcX | p.Leu120* | 8x |
| tsx | p.Trp258* | 5x |
| creD | p.Trp190* | 6x |

Because these variants were observed at relatively low read depths, they should be treated as candidate variants requiring further validation.

### UbiI Candidate Variant

An additional variant identified for further investigation was found in the *ubiI* gene.

- **Gene:** ubiI
- **Protein:** 2-octaprenylphenol 6-hydroxylase
- **Protein length:** 400 aa
- **Variant:** p.Gln37Pro
- **Variant position:** 3,052,208
- **Reference change:** G>A

The *ubiI* p.Gln37Pro variant was selected for additional structural and conservation analysis.

An experimental structure of UbiI is available in PDB entry 4K22. However, residues around position 37 are not experimentally resolved in the crystallographic coordinates. Therefore, the structure cannot be used to directly assess the local atomic environment of the Q37 residue.

Further conservation and domain analysis is required before making a functional interpretation of this variant.

### Quality-Control Reports

The `results/` directory contains generated quality-control and variant-analysis files, including:

- FastQC reports
- fastp trimming statistics
- Variant statistics
- Filtered variant statistics
- SnpEff annotated VCF
- Variant annotation table
- Variant-support table

Large raw sequencing files, reference files, and intermediate alignment files are excluded from the GitHub repository using `.gitignore`.

---

## Repository Structure

```
ngs-projects/
│
├── scripts/
│   ├── 01_qc.sh
│   ├── 02_trim.sh
│   ├── 03_align.sh
│   ├── 04_sort_index.sh
│   ├── 05_call_variants.sh
│   └── 06_filter_variants.sh
│
├── results/
│   ├── stats.txt
│   ├── filtered_variant_stats.txt
│   ├── variant_stats.txt
│   ├── variant_annotation.tsv
│   ├── variant_support.tsv
│   ├── variants.vcf
│   ├── variants_filtered.vcf
│   ├── variants_annotated.vcf
│   └── ubiI.fasta
│
├── raw_data/
│   └── # Sequencing reads (excluded from GitHub)
│
├── ref/
│   └── # Reference genome (excluded from GitHub)
│
├── data/
│   └── # SnpEff database (excluded from GitHub)
│
├── .gitignore
└── README.md
```

---

## Limitations

- Analysis used a 50,000-read-pair subset rather than the complete SRR2584863 sequencing dataset
- Average sequencing depth was approximately 2.30x
- Only 81.41% of the reference genome had at least 1x coverage
- Only 12.14% of positions had at least 5x coverage
- Low-depth variants may have reduced confidence
- Stop-gain predictions are computational annotations and require further biological validation
- The analysis does not establish whether clustered variants occur on the same chromosome/haplotype or in the same cellular lineage
- The identified candidate variants should not be considered experimentally confirmed mutations

---

## Future Work

- Analyze the complete SRR2584863 sequencing dataset
- Increase sequencing depth for higher-confidence variant detection
- Perform conservation analysis of prioritized variants
- Analyze protein domains affected by candidate variants
- Perform structural analysis where experimentally resolved structures are available
- Validate prioritized variants experimentally
- Compare variants across multiple E. coli strains
- Automate the complete workflow using Snakemake or Nextflow

---

## References

- NCBI Sequence Read Archive (SRA)
- NCBI Genome: E. coli K-12 MG1655
- Li H. (2013). Aligning sequence reads with BWA-MEM. arXiv:1303.3997.
- Danecek P. et al. (2021). Twelve years of SAMtools and BCFtools. GigaScience.
- Chen S. et al. (2018). fastp: an ultra-fast all-in-one FASTQ preprocessor. Bioinformatics.
- Cingolani P. et al. (2012). A program for annotating and predicting the effects of single nucleotide polymorphisms, SnpEff.

---

## Author

**Hemanshi Malankiya**
M.Sc. Bioinformatics
