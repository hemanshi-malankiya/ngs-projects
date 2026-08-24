content = open('README.md').read()

old = """- results/SRR2584863_1_fastqc.html and results/SRR2584863_2_fastqc.html - full raw read quality reports (all graphs: per-base quality, GC content, duplication levels, adapter content, etc.)
- results/fastp.html - full before/after trimming report (quality curves, filtering summary, adapter trimming details)
- results/stats.txt - complete variant calling statistics"""

new = """- [Read 1 FastQC Report](https://htmlpreview.github.io/?https://github.com/hemanshi-malankiya/ngs-projects/blob/main/results/SRR2584863_1_fastqc.html) - full raw read quality report (all graphs: per-base quality, GC content, duplication levels, adapter content, etc.)
- [Read 2 FastQC Report](https://htmlpreview.github.io/?https://github.com/hemanshi-malankiya/ngs-projects/blob/main/results/SRR2584863_2_fastqc.html) - full raw read quality report
- [fastp Trimming Report](https://htmlpreview.github.io/?https://github.com/hemanshi-malankiya/ngs-projects/blob/main/results/fastp.html) - full before/after trimming report (quality curves, filtering summary, adapter trimming details)
- [Full Variant Statistics](results/stats.txt) - complete variant calling statistics"""

if old in content:
    content = content.replace(old, new)
    open('README.md', 'w').write(content)
    print("SUCCESS: README updated")
else:
    print("NO MATCH FOUND - nothing changed")