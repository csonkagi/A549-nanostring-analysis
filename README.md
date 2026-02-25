# NanoString Data Analysis for A549 Lung Adenocarcinoma
This repository contains the NanoString codeset and associated Python scripts used for the analysis presented in the paper:

Csonka, G.I., Somlyai, I., Somlyai, G.

Deuterium Concentration as a Dual Regulator: Depletion and Enrichment Elicit Divergent Transcriptional Responses in A549 Lung Adenocarcinoma Cells

International Journal of Molecular Sciences (IJMS), Manuscript ID: ijms-4072276.

Included are:

The full NanoString codeset (gene list, cluster assignments, functional annotations, quantitative metrics)

Python scripts for data processing, statistical analysis, and visualization

This repository enables reproducible transcriptomic analysis and supports further research in cancer transcriptomics.

Contents
/data/
240lung cancer genes data.xlsx

NanoString gene list (236 genes, 4 of them were measured twice leading to 240 records), technical duplicates of transcription count data at 40, 80, 150 and 300 ppm after 72 h of incubation.

consensus_cancer_gene.csv.xlsx

Consensus genes used to retain only consensus genes in the analysis

/scripts/
240mcanceran.py:

This script processes NanoString gene expression data, calculates error propagation, classifies reliability, and generates 3D visualizations.
How to Run

Place your data file (240lung cancer genes data.xlsx) in the same directory as the script.
Install required Python packages:pandas, numpy matplotlib.pyplot, matplotlib.lines import Line2D, mpl_toolkits.mplot3d import Axes3D

Run the script:
python 240mcanceran.py

What the Script Does

Reads NanoString gene expression data from Excel.
Calculates mean, standard deviation, and relative expression at 40, 80, 300 ppm vs 150 ppm reference medium for each gene
Propagates errors and assigns a reliability category to each gene based on the sum of propagated relative errors.

Exports:
240 genes error propagation.xlsx: Full annotated dataset.
110 genes error filtered.xlsx: High-quality, filtered gene subset (total_error < 0.55).


Outputs:
Generates 3D scatter plots of gene expression ratios, colored by categories of total_error (e.g. 0.35, 0.45, 0.55, 0.65).

Customization
You can adjust filtering thresholds or color categories in the script to suit your analysis needs.

If you use this script or data, please cite:
Csonka, G.I., Somlyai, I., Somlyai, G. IJMS, Manuscript ID: ijms-4072276.


Generated 3D scatter plots of gene expression ratios, colored by reliability


<img width="1400" height="900" alt="Figure_240errors" src="https://github.com/user-attachments/assets/6b04c3b8-6ae1-40bb-8a2b-21bbc2f77adc" />

Relative gene expression reliability classification (all genes).
Three dimensional scatter plot of summed relative propagated errors for the full set of 236 cancer related genes measured across 40, 80, and 300 ppm deuterium concentrations. Each point is color coded by reliability class: ≤ 0.30 (green), ≤ 0.45 (light green), ≤ 0.55 (yellow), ≤ 0.65 (light red), and > 0.65 (red). Axes represent expression ratios at the three concentrations, illustrating the distribution of measurement precision across the dataset.


<img width="1400" height="900" alt="Figure_110errors" src="https://github.com/user-attachments/assets/6ae0da3f-bf78-47f4-96e1-d48a8543790b" />


Relative gene expression reliability classification (filtered genes).
Three dimensional scatter plot of the 110 genes retained after error propagation filtering (total propagated relative error < 0.55). The same color scheme is applied as in Fig. S1. This figure highlights the subset of genes with reproducible, low error measurements that form the basis for downstream clustering and pathway analysis.


