bcftools mpileup -f ref/GCF_000005845.2_ASM584v2_genomic.fna results/sorted.bam | bcftools call -mv -Ob -o results/variants.bcf
bcftools view results/variants.bcf > results/variants.vcf
bcftools stats results/variants.vcf > results/stats.txt
