from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Antibiotic Resistance Report",
    page_icon="🧬"
)

st.markdown("""
# PREDICTING ANTIBIOTIC RESISTANCE ACROSS BACTERIAL MECHANISMS USING MACHINE LEARNING

**Swarit Beley**  

---

## Abstract

For decades, antibiotic resistance has posed a threat to patients around the world. Antibiotics have been used to treat various bacterial illnesses, yet fail due to the wrong type of antibiotic being paired with the wrong type of bacteria. This project aims to analyze whether a bacterium's antibiotic resistance can be estimated computationally using known bacterial mechanisms and known antibiotic vulnerabilities. The first model (V1) used two tables of data, Table A and Table B. Table A contains whether a bacterium had a certain mechanism or not, and Table B determines which antibiotics were vulnerable to which mechanisms on a 0–1 scale. When compared to real data from the ATLAS surveillance database, Model V1's results did not track with the results shown on ATLAS. Additionally, scores shown from Model V1 repeatedly assigned identical scores to bacteria with overlapping mechanism profiles. The second model (V2) took this into account, which led us to use the same mechanism features as V1, trained against real resistance values from the ATLAS surveillance database. Model V2 integrated machine learning, using a gradient-boosted regression model to make predictions based on those mechanism features. Validated with leave-one-out cross-validation across 84 bacterium-antibiotic pairs with observed data, model V2 achieved a 41.3% improvement over baseline in mean absolute error. The result suggests that mechanism-level features do carry a real predictive signal, but only when the relationship between mechanisms and resistance is learned from data rather than assumed by secondary research. The results from both model V1 and V2 are integrated into an interactive Streamlit website, with a drop-down selection for a bacterium and an antibiotic, along with a displayed pie chart.

**Keywords:** Antibiotic resistance, computational modeling, machine learning, resistance mechanisms, bacteria, bioinformatics  

---

# 1. Introduction

Antibiotic resistance has proved to be a great threat for years to come. Bacteria continue to evolve, making certain antibiotics continuously ineffective over time. This issue leads to higher medical costs, greater illness, and an increased mortality rate. Predicting antibiotic resistance is difficult because it arises from a range of distinct bacterial mechanisms — drug efflux, hydrolysis, target alteration, and others — and bacterial species differ in which of these mechanisms they carry. Most computational approaches to this problem rely on scanning a sequenced bacterial genome for known resistance genes, which requires an isolate to already be cultured and sequenced before a prediction can be made. This project asks whether mechanism-level knowledge alone, without a sequenced genome, can be used to estimate resistance instead.

This project investigates common bacterial mechanisms across a wide range of bacteria and organizes them into a structured dataset. Within the dataset, Table A contains the bacteria and a yes or no for whether each performs a particular mechanism, and Table B contains individual antibiotics and their vulnerability rating from 0 to 1 to each mechanism. These tables were first combined into a mathematical formula to generate resistance percentages, and tested against real-world surveillance data to see whether that formula held up. The results of that test then shaped a second, machine-learning-based model trained on the same features.

---

# 2. Research Question and Objectives

## Research Question

Can antibiotic resistance be predicted from a bacterium's known resistance mechanisms alone, without relying on a sequenced genome?

## Objectives

- Identify common resistance patterns among bacterial species.
- Identify the effectiveness of various antibiotics.
- Create a dataset comprising pairings of antibiotics with bacterial species.
- Develop a computational mathematical model that will generate these percentages of resistance.
- Compare the mathematical model results against real-world data.
- Train a machine learning model on the real-world data and resistance mechanisms as input.
- Build an interactive website that showcases these comparisons.

---

# 3. Background and Literature Context

## 3.1 Common Resistance Mechanisms

- **Multidrug efflux pump** – Actively transports structurally diverse antimicrobial agents out of bacterial cells  
- **Hydrolysis** – Produces enzymes made of water, breaking chemical bonds within the antibiotic molecule which renders it inactive  
- **Porin loss** – Eliminates water-filled channels in the outer membrane that hydrophilic antibiotics use as entryways  
- **Porin mutation** – Reduces the number of outer membrane channels  
- **PBP modification** – Alters the structure of bacterial enzymes so beta lactam antibiotics cannot bind to them  
- **Ribosomal methylation** – Bacteria that add methyl chemical groups to specific sites on their ribosomal RNA which prevents ribosomal-targeting antibiotics from binding  
- **Biofilm protection** – Creates a slimy, protective barrier that allows bacteria to survive antibiotic treatments  
- **Target alteration** – Changes the cellular structure that antibiotics target their attack towards  
- **Target replacement** – Bacteria produce an alternative version of the target that isn't recognized or bound by the antibiotic  
- **Target overexpression** – Increases the amount of target molecule produced so the antibiotic can't block all of it  
- **Drug inactivation** – Bacteria chemically modify the antibiotic so it can no longer bind to its target  
- **Gram negative** – Bacteria with an added outer membrane that limits which antibiotics can enter the cell  
- **Outer membrane** – An extra lipid layer in Gram negative bacteria that acts as a barrier to antibiotics entering  
- **Intrinsic beta lactamase** – Bacteria that naturally produce beta lactamase enzymes without needing to acquire the gene  
- **Non fermenter** – A group of Gram negative bacteria that don't ferment glucose and tend to have higher natural resistance  

## 3.2 Rationale for Using Individual Antibiotics

Initial source for answering why the main classes were chosen instead of individual drugs:  
https://pharmainfonepal.com/classification-of-antibiotics-based-on-mechanism-of-action

Initially, the main antibiotic classes were chosen for the model input since it appeared that major antibiotic classes share similar mechanisms of action. However, after reviewing data from [https://atlas-surveillance.com/r/antibacterials/database/mic-distribution], a difference in resistance across different antibiotics within the same classes became apparent. This finding led to revising the model from using broad antibiotic class inputs to incorporating individual antibiotic-specific inputs, allowing it to capture variation in resistance patterns within the same class and improve overall accuracy.

## 3.3 Existing Computational Approaches

Currently, identifying antibiotic resistance among various bacteria is typically done through genomic sequencing. Two of the most well-known tools that use genomic sequencing to map antibiotic resistance include AMRFinderPlus (Feldgarden et al., 2021) and the Comprehensive Antibiotic Resistance Database Gene Identifier, CARD/RGI (Alcock et al., 2023). Both of these tools take a sequenced bacterial genome and run it through their database, attempting to find similar known resistance genes using sequence alignment methods. The result typically includes the resistance genes that are present after the searches have been conducted. This use of genomic sequencing makes the results showcased on AMRFinderPlus and CARD/RGI highly accurate, as it is backed by a verifiable method and draws on an extensive reference database, making its results highly reliable.

A key limitation of tools such as AMRFinderPlus and CARD/RGI is their dependence on an already-sequenced bacterial genome, a process that can take anywhere from two to eight weeks. This project addresses that limitation by requiring only existing knowledge of bacterial mechanisms rather than a sequenced genome as input. As a result, the model is able to estimate resistance percentages without the delay associated with genome sequencing.

---

# 4. Model V1 Data Collection and Dataset Design

## 4.1 Table A – Bacterial Resistance Mechanisms

Common resistance characteristics were identified across different bacterial species. If a resistance mechanism was common within the species, it was marked as **Yes**; otherwise, **No**. Isolates of the same species can differ in the specific mechanisms that they possess, due to mutation. Thus, the specific mechanisms were scored at the species level for the presence of each of those mechanisms.

## 4.2 Table B – Antibiotic Vulnerability to Mechanisms

Antibiotic classes vary in vulnerability to different resistance mechanisms. A predicted vulnerability value between **0 and 1** was assigned based on multiple published literature providing information on how strongly each mechanism impacts the antibiotic class.

---

# 5. Model V1 Model Design and Data Integration

## 5.1 Combining Tables

The **Pandas** library in Python was used to combine the two tables into a supertable that is used as the model input.
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

# --- Figure 1: Supertable Diagram ---
supertable_diagram = BASE_DIR / "data" / "Images" / "supertable_diagram.png"
st.image(supertable_diagram, caption="Figure 1: Process for combining Table A (bacterial mechanism presence) and Table B (antibiotic vulnerability weights) into the supertable used as model input.", use_container_width=True)

st.markdown("""
---

## 5.2 Resistance Scoring Method

To measure the interaction between a bacterium and an antibiotic, the binary mechanism value (0 or 1) is multiplied by the antibiotic vulnerability weight (0–1) for each mechanism. This identifies which mechanisms meaningfully contribute to resistance.

All resulting values are then summed to produce the bacterium's total mechanism impact for that antibiotic. Finally, this sum is divided by the maximum possible mechanism score, producing a resistance percentage.

This percentage represents how resistant the bacterium is to the antibiotic based on its known mechanisms.

---

# 6. Validation of Model V1

The website https://atlas-surveillance.com was used to compare the generated resistance value to real established data. The data showed that certain types of penicillin exhibited higher resistance percentages than others. After comparing the data and output from Atlas Surveillance, it became clear that most species of bacteria for certain mechanisms had identical scores, making most of the resistance rates the exact same percentage or extremely similar. To address this issue, additional mechanisms were added to balance the data, such as drug inactivation, Gram-negative, outer membrane, and intrinsic beta-lactamase; however, it made little difference when comparing the scores that ATLAS had provided.

---

# 7. Model V2: Machine Learning Approach

Looking at the results that Model V1 provided, machine learning was integrated as a separate model: Model V2. Specifically, a gradient-boosted regression model was used, trained on the mechanisms picked out for Model V1 and using the data from ATLAS as learning material to make a prediction. Because only 84 bacterium-antibiotic pairs had observed ATLAS data to train and validate on, leave-one-out cross-validation was implemented, which preserves as much training data as possible for each fold rather than setting aside a larger fixed test set. Leave-one-out cross-validation works by training the model on all but one bacterium-antibiotic pair, testing it on the pair left out, and repeating this process for each of the 84 observed pairs so that every pair is used once as a test case. For the model itself, 200 estimators, a learning rate of 0.05, and a maximum depth of 3 were used, which produced the reported MAE score.

---

# 8. Validation of Model V2

`model_mae = mean_absolute_error(actuals, predictions)` was used to output the MAE (mean absolute error) value, which was then compared to a baseline MAE to calculate the improvement over baseline. The higher the improvement over baseline, the higher the accuracy of the model. By changing the number of estimators, learning rate, and maximum depth, Model V2 was able to reach a **41.3% improvement over baseline**. Later, the model's predictions were compared with results from ATLAS once more, and Model V2's predictions appeared closer to the ATLAS values than the scores produced by Model V1.

---

# 9. Implementation

## 9.1 Programming Tools

- Python  
- Pandas  
- Streamlit  
- Apache ECharts  

## 9.2 Virtual Lab Interface

An interactive website was created using Python and the Streamlit documentation, acting as a virtual lab that used the combined super table as data. Dropdowns were created for choosing the bacteria/antibiotic and having it print out the resistance value, creating a way of comparing any target bacteria against an antibiotic and getting a resistance value. An interactive pie chart was embedded into the website, showcasing a graphical representation of which mechanisms are effective against the antibiotic.
""")

# --- Figure 2: Virtual Lab Interface ---
interface = BASE_DIR / "data" / "Images" / "virtual_lab_upscaled.png"
st.image(interface, caption="Figure 2: Virtual Lab interface showing the formula-based (Model V1), predictive (Model V2), and observed ATLAS resistance values for a selected bacterium-antibiotic pair, along with a breakdown of resistance contribution by mechanism.", use_container_width=True)

st.markdown("""
---

# 10. Results

Model V2 achieved an MAE of 0.1207 and an R² of 0.536 from cross-validation on the 84 bacterium-antibiotic pairs with observed ATLAS data. This represents a reduction in error of 41.3% compared to a model that always predicted the mean observed resistance value for each bacterium-antibiotic pair, which had an MAE of 0.2058. The R² value of 0.536 indicates that the model explains roughly half the variance in the observed resistance of each bacterium to each antibiotic, with the remainder of the variance unaccounted for in the model.

In general, accuracy of predictions varied between bacterium-antibiotic pairs. For instance, Model V2 predicted that *Klebsiella pneumoniae* will exhibit resistance to Ampicillin of 0.8811, whereas the observed value was 0.9219. In another example, the model predicted that *Enterobacter cloacae* will exhibit resistance to Amoxicillin-clavulanate of 0.5635, whereas the observed value was 0.9308. It should be noted that this model was applied to bacterium-antibiotic pairs beyond those present in the ATLAS database to determine their predicted levels of resistance to those antibiotics; these predictions were applied outside of the 84 evaluated bacterium-antibiotic pairs in the database and, therefore, have not been validated against observed resistance. In all cases, however, the model ensured that its predicted levels of resistance were bounded between 0 and 1.
""")

# --- Figure 3: Predicted vs. Observed ---
predicted_vs_observed = BASE_DIR / "data" / "Images" / "predicted_vs_observed_scatter.png"
st.image(predicted_vs_observed, caption="Figure 3: Predicted vs. observed resistance values for the 84 bacterium-antibiotic pairs with ATLAS data, generated using the final model trained on the complete dataset. Because this model was trained on all 84 pairs shown, these predictions reflect in-sample fit rather than the leave-one-out cross-validation results reported in the text (MAE = 0.1207, R² = 0.536).", use_container_width=True)

st.markdown("""
---

# 11. Discussion

Model V2's 41.3% improvement over baseline shows that the model is picking up on real patterns in the data, giving it meaningful value when compared against results from real experiments, such as those recorded in ATLAS. V1, by contrast, held far less significance due to its reliance on a fixed formula. V2 addressed this issue using the same mechanism data but a different approach, learning its weights directly from real experimental data rather than assigning them by hand. This reveals that grounding the model in real, professionally collected data mattered far more than simply having the right features or general knowledge.

An R² of 0.536 means the model only explains about half of what's actually driving resistance, so predictions from it shouldn't be treated as fully reliable on their own. This is likely because mechanism data alone doesn't capture the full picture, and other factors are contributing to resistance that the model simply isn't accounting for. This becomes clear when looking at individual pairs. *Klebsiella pneumoniae* and Ampicillin predicted close to the real value, but *Enterobacter cloacae* and Amoxicillin-clavulanate came out way off, showing that the model doesn't perform consistently across every bacterium and antibiotic. This is likely because some pairs carry more complex or unique resistance patterns that the model has a harder time learning from limited data.

Even with these limitations, a model that gives an answer instantly holds real value in situations where waiting 2 to 8 weeks for genome sequencing simply isn't practical, even if that answer isn't as precise. This could make Model V2 useful as an early estimate to help guide treatment decisions while more accurate, sequencing-based results are still being processed. Still, the biggest thing to keep in mind is that the model was trained on only 84 pairs, which isn't a large amount of data for a machine learning model to learn from. Because of this, its results should be treated as a starting point rather than a fully reliable answer.
""")

# --- Figure 4: MAE Comparison ---
mae_comparison = BASE_DIR / "data" / "Images" / "mae_comparison_bar_chart.png"
st.image(mae_comparison, caption="Figure 4: Mean absolute error across the baseline model, Model V1, and Model V2, evaluated on the same 84 validated bacterium-antibiotic pairs. Model V2's error reflects leave-one-out cross-validation; Model V1's error reflects its fixed formula applied directly, since it requires no training.", use_container_width=True)

# --- Figure 5: Feature Importance ---
feature_importance = BASE_DIR / "data" / "Images" / "feature_importance_chart.png"
st.image(feature_importance, caption="Figure 5: Top 15 most influential features in Model V2, ranked by feature importance, as reported by the trained gradient-boosted regression model.", use_container_width=True)

st.markdown("""
---

# 12. Limitations

A key constraint throughout this project was the fairly small amount of data Model V2 was trained on. Usually, machine learning models are trained on extremely large amounts of data, making them better prepared for different cases. However, Model V2 had only 264 total bacterium-antibiotic pairs and 84 complete pairs, limiting the percent improvement over baseline.

Another limitation was that the model assumes the effects of different mechanisms are additive, whereas in reality many mechanisms operate at a more complex level. These aspects of the model keep it elementary at the expense of more accuracy.

---

# 13. Possible Future Improvements

- Include a more complete, larger dataset for Model V2 to be trained on  
- Continue adding more resistance mechanisms for Table A  
- Testing whether incorporating genomic data alongside mechanism features could improve accuracy  
- Incorporating different model architectures beyond gradient boosting to see if performance improves  

---

# 14. Conclusion

The creation of Model V1 and Model V2 sought out to determine whether antibiotic resistance could be determined computationally without the use of genomic sequencing. Model V2 supports that this is possible through using mechanism features combined with pre-created data to generate percentages of resistance successfully, even to the extent of a 41.3% improvement over baseline. The comparison between V1 and V2 demonstrates that having the right mechanism data was never the main issue — the real difference came from how that data was used, since learning the weights directly from real experimental results outperformed a fixed, hand-assigned formula built on the same information.

Although antibiotic resistance was successfully estimated computationally without the use of genomic sequencing, the limitations were that the model was trained on a relatively small set of 84 observed pairs and only explained about half the variance in real resistance values, meaning its predictions are best treated as an early estimate rather than a fully reliable result. Even so, this makes Model V2 a potentially useful tool for guiding treatment decisions in the window before slower, more precise methods like AMRFinderPlus or CARD/RGI can produce results.

---

# 15. Tools and Resources

- NCBI  
- Atlas Surveillance  
- Streamlit Documentation  
- Apache ECharts  

---

# 16. References

Feldgarden, M., Brover, V., Gonzalez-Escalona, N., Frye, J. G., Haendiges, J., Haft, D. H., Hoffmann, M., Pettengill, J. B., Prasad, A. B., Tillman, G. E., Tyson, G. H., & Klimke, W. (2021). AMRFinderPlus and the Reference Gene Catalog facilitate examination of the genomic links among antimicrobial resistance, stress response, and virulence. *Scientific Reports, 11*, 12728. https://doi.org/10.1038/s41598-021-91456-0

Alcock, B. P., Huynh, W., Chalil, R., Smith, K. W., Raphenya, A. R., Wlodarski, M. A., Edalatmand, A., Petkau, A., Syed, S. A., Tsang, K. K., Baker, S. J. C., Dave, M., McCarthy, M. C., Mukiri, K. M., Nasir, J. A., Golbon, B., Imtiaz, H., Jiang, X., Kaur, K., Kwong, M., Liang, Z. C., Niu, K. C., Shan, P., Yang, J. Y. J., Gray, K. L., Hoad, G. R., Jia, B., Bhando, T., Carfrae, L. A., Farha, M. A., French, S., Gordzevich, R., Rachwalski, K., Tu, M. M., Bordeleau, E., Dooley, D., Griffiths, E., Zubyk, H. L., Brown, E. D., Maguire, F., Beiko, R. G., Hsiao, W. W. L., Brinkman, F. S. L., Van Domselaar, G., & McArthur, A. G. (2023). CARD 2023: Expanded curation, support for machine learning, and resistome prediction at the Comprehensive Antibiotic Resistance Database. *Nucleic Acids Research, 51*(D1), D690–D699. https://doi.org/10.1093/nar/gkac920

Reygaert, W. C. (2018). An overview of the antimicrobial resistance mechanisms of bacteria. *AIMS Microbiology, 4*(3), 482–501. https://doi.org/10.3934/microbiol.2018.3.482

PharmaInfoNepal. Classification of antibiotics based on mechanism of action. Retrieved from https://pharmainfonepal.com/classification-of-antibiotics-based-on-mechanism-of-action

ATLAS Surveillance Database. Antibacterial database, MIC distribution. Retrieved from https://atlas-surveillance.com/r/antibacterials/database/mic-distribution
""")