# Antibiotic Resistance Model

Predicts resistance rates for bacteria-antibiotic pairs using biological mechanism features trained against clinical surveillance data.

## Overview

Given a bacterium and an antibiotic, the model estimates the fraction of isolates likely to be resistant. It takes as input two feature tables: one describing which resistance mechanisms each bacterium has (efflux pumps, hydrolysis, porin mutations, etc.), and one scoring how effective each mechanism is at stopping each antibiotic. These are combined into 30 features per pair and fed into a GradientBoosting regressor trained on observed resistance rates from ATLAS (Pfizer's Antimicrobial Testing Leadership and Surveillance program).

The project includes a Streamlit web interface where users can select any bacteria-antibiotic combination and view the model prediction alongside the ATLAS observed value (where available) and the original formula-based score from an earlier version of the model.

## Performance

Validated using leave-one-out cross-validation on 84 ATLAS-grounded pairs.

| Metric | Value |
|--------|-------|
| Mean Absolute Error (MAE) | 0.121 |
| R² | 0.536 |
| Baseline MAE (predict mean) | 0.206 |
| Error reduction vs. baseline | 41.3% |

## Data

**Table A** contains 12 bacterial species mapped against 15 binary features describing resistance-relevant biological properties (e.g., has efflux pump, performs hydrolysis, gram-negative, outer membrane presence).

**Table B** contains 22 antibiotics scored from 0 to 1 against the same 15 features. These values are qualitative estimates based on literature review, not experimentally derived measurements.

**ATLAS observed data** provides real-world resistance rates (fraction of resistant isolates) for 84 of the 264 possible bacteria-antibiotic pairs. The remaining 180 pairs have model predictions only.

Source: [atlas-surveillance.com](https://atlas-surveillance.com)

## Background

The initial version of this project (V1) used a hand-built formula to compute resistance scores: for each pair, multiply each mechanism's binary presence by its effectiveness weight, sum the results, and divide by the total number of mechanisms. Comparing these scores against ATLAS data revealed that the formula consistently overestimated resistance and could not distinguish between bacteria with identical mechanism profiles (6 of 12 bacteria shared the same feature set).

V2 addressed this by adding four distinguishing biological features (gram-negative, outer membrane, intrinsic beta-lactamase, non-fermenter), training a GradientBoosting regressor on ATLAS data, and validating with leave-one-out cross-validation. Both versions are shown in the web interface for comparison.

## Installation

Requires Python 3.10+.

```bash
pip install pandas numpy scikit-learn streamlit
```

## Usage

Run in order:

```bash
# 1. Train the model and generate predictions for all 264 pairs
python scripts/Model.py

# 2. Build the supertable with formula-based scores
python scripts/Build_Dataset.py

# 3. Launch the web interface
streamlit run website/Home.py
```

## Project structure

```
data set/
    Data - Table A.csv          Bacteria x mechanism features (binary)
    Data - Table B.csv          Antibiotic x mechanism effectiveness (0-1)
    training_data.csv           84 ATLAS-grounded pairs, 30 features + target
    supertable.csv              264-pair cross-join with formula scores
    predictions.csv             Model predictions for all 264 pairs

scripts/
    Model.py                    Trains model, runs LOO validation, predicts all pairs
    Build_Dataset.py            Builds supertable and computes formula scores

website/
    Home.py                     Streamlit landing page
    pages/Virtual_Lab.py        Interactive lab with dropdowns and pie chart
    pages/Report.py             Embedded research report
    requirements.txt

metrics.txt                     MAE, R², baseline comparison
```

## Limitations

- Three bacteria pairs share identical feature profiles and always receive the same prediction: E. coli / Salmonella, Pseudomonas / Acinetobacter, Klebsiella / Enterobacter
- ATLAS coverage is 84 of 264 pairs (32%); predictions for uncovered pairs are extrapolations
- Table B values are literature-informed estimates, not lab measurements
- GradientBoosting can predict outside [0, 1]; outputs are clipped
- All predictions are at the species level and do not capture strain-level variation

## References

- ATLAS Surveillance: https://atlas-surveillance.com
- scikit-learn: https://scikit-learn.org
- Streamlit: https://streamlit.io
- Mechanism research: https://pmc.ncbi.nlm.nih.gov/articles/PMC6604941/