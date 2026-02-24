# NanoString Data Analysis for A549 Lung Adenocarcinoma
This repository contains the NanoString codeset and associated Python scripts used for the analysis presented in the paper:
Csonka, G.I., Somlyai, I., Somlyai, G.
Deuterium Concentration as a Dual Regulator: Depletion and Enrichment Elicit Divergent Transcriptional Responses in A549 Lung Adenocarcinoma Cells
International Journal of Molecular Sciences (IJMS), Manuscript ID: ijms-4072276.

Included are:

The full NanoString codeset (gene list, cluster assignments, functional annotations, quantitative metrics)
Python scripts for data processing, statistical analysis, and visualization

This repository enables reproducible transcriptomic analysis and supports further research in cancer genomics.

Contents
/data/
240lung cancer genes data.xlsx
NanoString codeset: gene list, transcription count data at 40, 80, 150 ans 300 ppm after 72 h of incubation.


/scripts/
240mcanceran.py:
This script processes NanoString gene expression data, calculates error propagation, classifies reliability, and generates 3D visualizations.
How to Run

Place your data file (240lung cancer genes data.xlsx) in the same directory as the script.
Install required Python packages:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D

Run the script:
python 240mcanceran.py

What the Script Does

Reads NanoString gene expression data from Excel.
Calculates mean, standard deviation, and relative expression at 40, 80, 300 ppm vs 150 ppm reference medium for each gene
Propagates errors and assigns a reliability category to each gene based on the sum of propagated relative errors.

Exports:
240 genes error propagation.xlsx: Full annotated dataset.
110 genes error filtered.xlsx: High-quality, filtered gene subset.
Generates 3D scatter plots of gene expression ratios, colored by reliability.

Outputs
Excel files with processed and filtered data.
3D plots visualizing gene expression reliability.

Customization
You can adjust filtering thresholds or color categories in the script to suit your analysis needs.

If you use this script or data, please cite:
Csonka, G.I., Somlyai, I., Somlyai, G. IJMS, Manuscript ID: ijms-4072276.

<img width="1400" height="900" alt="Figure_110errors" src="https://github.com/user-attachments/assets/6ae0da3f-bf78-47f4-96e1-d48a8543790b" />

<img width="1400" height="900" alt="Figure_240errors" src="https://github.com/user-attachments/assets/6b04c3b8-6ae1-40bb-8a2b-21bbc2f77adc" />

