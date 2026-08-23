samtools view -bS results/aligned.sam > results/aligned.bam
samtools sort results/aligned.bam -o results/sorted.bam
samtools index results/sorted.bam
