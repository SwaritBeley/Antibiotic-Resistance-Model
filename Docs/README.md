# Antibiotic Resistance Model
## Overview

The Antibiotic Resistance Model is an image-based machine learning model designed to analyze disk diffusion images in order to predict the degree of antibiotic resistance across 16 different antibiotics.

By measuring inhibition zones from agar plate images, the model can estimate an amount of resistance in the form of percentages, helping a process that is traditionally manual and often prone to human error.

This project explores how image-based detection and pattern recognition can be applied to the medical field, helping solve public health issues.


## Motivation

Bacteria fighting back makes treating infections tougher today. Labs often rely on disk methods to check drug effectiveness, yet problems remain such as:
- Measuring them means doing it by hand
- Results can vary between observers
- Scaling analysis across large datasets is difficult

This project aims to demonstrate how computer vision + machine learning can assist in:
- Standardizing resistance detection
- Speeding up analysis
- Laying groundwork for automated lab workflows


## Dataset

- Source: The dataset is from the Dryad Digital Repository
 https://datadryad.org/dataset/doi:10.5061/dryad.5dv41nsfj

- Content: The dataset is modified by code that splits up the disk diffusion images into rectangular sections, isolating each antibiotic
