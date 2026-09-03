#!/bin/bash

bcftools view -i 'QUAL>=20 && INFO/DP>=5' results/variants.vcf -Ov -o results/variants_filtered.vcf

bcftools stats results/variants_filtered.vcf > results/filtered_variant_stats.txt
