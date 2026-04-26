import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Antibiotic Resistance Report",
    page_icon="🧬"
)

st.markdown("""
# ANTIBIOTIC RESISTANCE ACROSS BACTERIAL MECHANISMS

**Swarit Beley**  

---

## Abstract

For decades, antibiotic resistance has posed a threat to patients around the world. Antibiotics have been used to treat various bacterial illnesses, yet often fail due to the wrong type of antibiotic being paired with the wrong type of bacteria. This review analyzes common resistance mechanisms among specific bacteria and creates structured table inputs for training a computational model. The model generates a resistance rating in the form of a percentage for any given combination of a bacterial organism and an antibiotic class. The model is integrated into an interactive website, showcasing resistance ratings along with graphical representations.

**Keywords:** Antibiotic resistance, computational modeling, resistance mechanisms, bacteria, bioinformatics  

---

# 1. Introduction

Antibiotic resistance has proven to be a growing global threat. Bacteria continue to evolve, making certain antibiotics ineffective over time. This issue leads to higher medical costs, prolonged illness, and increased mortality rates. Detecting antibiotic resistance remains complex due to diverse mechanisms such as drug efflux, hydrolysis, target alteration, and others.

The diversity among these mechanisms makes predicting resistance patterns based purely on theoretical knowledge extremely difficult.

This project investigates common bacterial resistance mechanisms and organizes them into a structured dataset:

- **Table A** contains bacteria and a Yes/No classification indicating whether a specific resistance mechanism is present.
- **Table B** contains antibiotic classes and their vulnerability ratings (0–1) against each mechanism.

Together, these tables generate a resistance percentage by evaluating the overlap between bacterial mechanisms and antibiotic vulnerabilities.

---

# 2. Research Question and Objectives

## Research Question

How can bacterial resistance mechanisms be used within a computational framework to determine whether a specific antibiotic class will be resistant?

## Objectives

- Identify common resistance mechanisms across bacterial species.
- Categorize antibiotic classes based on mechanism of action.
- Construct structured datasets (Table A and Table B).
- Develop a computational model that calculates resistance percentages.
- Build an interactive virtual lab interface for visualization and comparison.

---

# 3. Background and Literature Context

This section explains known resistance mechanisms and summarizes foundational research that informed the design of this model.

## 3.1 Common Resistance Mechanisms

- Cell wall alteration  
- Multidrug efflux pump  
- Hydrolysis  
- Porin loss  
- Porin mutation  
- PBP modification  
- Ribosomal methylation  
- Biofilm protection  
- Target alteration  
- Target replacement  
- Target overexpression  
- Drug inactivation  

## 3.2 Rationale for Using Antibiotic Classes

Major antibiotic classes were selected instead of individual drugs because drugs within the same class share similar mechanisms of action.

Reference:  
https://pharmainfonepal.com/classification-of-antibiotics-based-on-mechanism-of-action/

The source demonstrates that major antibiotic classes operate through shared biological mechanisms, justifying the class-based modeling approach.

---

# 4. Data Collection and Dataset Design

## 4.1 Table A – Bacterial Resistance Mechanisms

Common resistance characteristics were identified across different bacterial species. If a mechanism was common within the species, it was marked as **Yes**; otherwise, **No**.

## 4.2 Table B – Antibiotic Vulnerability to Mechanisms

Antibiotic classes vary in vulnerability to different resistance mechanisms. A predicted vulnerability value between **0 and 1** was assigned based on research into how strongly each mechanism impacts the antibiotic class.

---

# 5. Model Design and Data Integration

## 5.1 Combining Tables

The **Pandas** library in Python was used to combine the two tables into a "super table," which serves as the model's input dataset.

Conceptual example:
""")

# --- Super Table Section ---
st.markdown("---")
st.subheader("📊 Super Table Construction")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Table A**")
    table_a = pd.DataFrame({
        "A": ["AA", "BA"],
        "B": ["AB", "BB"],
        "C": ["AC", "BC"]
    }, index=["A", "B"])
    st.table(table_a)

with col2:
    st.markdown("**Table B**")
    table_b = pd.DataFrame({
        "A": ["1A", "2A"],
        "B": ["1B", "2B"],
        "C": ["1C", "2C"]
    }, index=["1", "2"])
    st.table(table_b)

st.markdown("**Super Table (Cross Join)**")
a_reset = table_a.reset_index(drop=True)
b_reset = table_b.reset_index(drop=True)
super_table = a_reset.merge(b_reset, how="cross")
st.dataframe(super_table, use_container_width=True)

st.markdown("""
---

## 5.2 Resistance Scoring Method

Resistance scores are calculated by evaluating the overlap between bacterial resistance mechanisms (Yes/No values) and antibiotic vulnerability weights (0–1 values). The combined interaction is converted into a percentage representing predicted resistance strength.

---

# 6. Implementation

## 6.1 Programming Tools

- Python  
- Pandas  
- Streamlit  
- Apache ECharts  

## 6.2 Virtual Lab Interface

An interactive website was developed using Streamlit, functioning as a virtual lab powered by the combined super table.

Key features include:

- Dropdown menus for selecting bacteria and antibiotic classes  
- Automatic resistance percentage output  
- Interactive pie chart visualization  
- Graphical breakdown of mechanism contributions  

---

# 7. Results

General resistance patterns emerged based on mechanism overlap. Certain mechanisms, such as hydrolysis and efflux pumps, significantly increased resistance percentages across multiple antibiotic classes.
""")

# --- Image placed OUTSIDE the markdown string ---
interface = './website/data/Images/interface.png'

st.image(interface, caption="Figure 1: Virtual Lab Interface", use_container_width=True)

st.markdown("""
---

# 8. Validation with Real-World Data

The website https://atlas-surveillance.com was used to compare the generated resistance value to real established data. The data showed that certain types of penicillin exhibited higher resistance percentages than others. After comparing the data and output from Atlas Surveillance, we realized that the bacteria had the same characteristics, making most of the resistance rates the exact same percentage. To address this issue, additional mechanisms were added to balance the data.

---

# 9. Discussion

The results demonstrate that modeling resistance through mechanism overlap produces biologically meaningful trends. Mechanisms such as efflux pumps, hydrolysis, and target alteration heavily influenced resistance scores, consistent with clinical observations.

---

# 10. Limitations

- Binary Yes/No mechanism classification  
- Predicted (not experimentally measured) vulnerability values  
- No strain-level genomic specificity  
- Simplified resistance scoring formula  

---

# 11. Future Improvements

- Integrate genomic datasets for further precision  
- Expand antibiotic class coverage  
- Apply machine learning for weight optimization  

---

# 12. Conclusion

This project provides a structured and simple way to determine percentages of resistance among common bacterial mechanisms and antibiotics. The model highlights which antibiotics are likely to remain effective by combining bacterial mechanisms with antibiotic vulnerability rates. Overall, this project demonstrates how computational models can be implemented in the medical field to better understand resistance patterns and make categorization of bacteria and antibiotics more efficient.

---

# 13. Tools and Resources

- NCBI  
- Atlas Surveillance  
- Streamlit Documentation  
- Apache ECharts  

---

# 14. References

*(APA or MLA formatted citations)*
""")