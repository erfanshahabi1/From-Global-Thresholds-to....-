# Multi-Hazard Climate Classification in Khuzestan: A Regionally Calibrated Approach Based on Local Thresholds and Spatiotemporal Patterns

**Machine Learning | Climate Risk Assessment | XGBoost | SHAP | ERA5 | Explainable AI**

## Overview

Climate hazards threaten agricultural sustainability, water resources, and livelihoods in Khuzestan Province, southwestern Iran. The region's climatic heterogeneity motivates analysis that distinguishes local conditions rather than relying exclusively on province-wide averages.

This research develops a regionally calibrated, explainable machine learning framework for classifying seven climate hazards across four agro-climatic sub-regions and two agricultural seasons: spring and autumn.

Using long-term ERA5 reanalysis data, the framework combines climate-indicator computation, threshold-based hazard labeling, regional threshold refinement, XGBoost classification, hyperparameter optimization, and SHAP-based interpretation.

Initial hazard thresholds are informed by established definitions and manually refined using PCA visualizations and local climatic patterns. Separate classifiers are developed for each hazard, sub-region, and season.

The manuscript describes a leakage-aware feature-exclusion strategy, including the removal of SPI from the drought classifier and its possible use in other models where it does not define the target. The exact extent of feature exclusion requires clarification because the manuscript's drought-label description and SHAP figure are not fully consistent; this issue is documented under **Research Limitations and Future Work**.

The study aims to support interpretable regional climate-hazard assessment and further research on agricultural adaptation and climate resilience. Its conclusions call for independent observational validation before operational deployment.

## Research Objectives

The main objectives of this research are:

- **Regional climate hazard classification:** Develop separate models for four agro-climatic sub-regions of Khuzestan.
- **Multi-hazard assessment:** Classify seven binary climate hazards during spring and autumn.
- **Leakage-aware modeling:** Apply hazard-specific feature exclusion to reduce direct overlap between label definitions and model predictors.
- **Explainable AI:** Use global SHAP analysis to identify influential predictors and examine geographic differences in model behavior.
- **Model evaluation:** Assess performance using F1-score, balanced accuracy, ROC-AUC, and confusion-matrix measures.

## Study Area

The study describes a terrestrial domain in Khuzestan Province, southwestern Iran, bounded by:

- **Latitude:** 29.5°–33° N
- **Longitude:** 47°–51° E

The domain is divided into four sub-regions:

| Code | Sub-region |
|---|---|
| NW | Northwest |
| NE | Northeast |
| SW | Southwest |
| SE | Southeast |

The regional boundaries are placed at **31.25° N** and **49° E**. The manuscript relates these boundaries to physiographic and hydroclimatic differences, including contrasts between foothill areas and southern plains and variations in moisture conditions.

Each terrestrial grid point is assigned to one sub-region. Sea-surface grid points are excluded using a Natural Earth land mask and spatial processing with Cartopy and Shapely.

Spring and autumn are selected because they coincide with active sowing and harvesting periods and are therefore important windows for agricultural hazard assessment.

## Climate Data and Feature Engineering

### Data Source

The primary source is **ERA5 reanalysis**, accessed through the **Copernicus Climate Data Store (CDS)**.

The abstract and Section 2.2 report an analysis covering **1940–2023**, at a spatial resolution of **0.25°**. Section 2.2 names ERA5 Monthly Averaged Data on Single Levels and also describes the extraction of daily and monthly data for feature computation.

This README follows the study period stated in the abstract and methods. Conflicting dates in the manuscript's figures and ambiguities in the data-product description are identified under **Research Limitations and Future Work**.

### Primary Climate Variables

The manuscript lists the following primary variables:

| Variable | Description |
|---|---|
| T2M | 2-meter air temperature |
| D2M | 2-meter dew point temperature |
| TP | Total precipitation, described as monthly total precipitation in the variable table |
| SSRD | Surface incoming shortwave radiation |
| Z | Geopotential-related variable at 500 hPa |
| SWVL1 | Topsoil volumetric moisture in the 0–7 cm layer |
| U10 | 10-meter eastward wind component |
| V10 | 10-meter northward wind component |
| LAI_LV | Leaf Area Index for low vegetation |
| LAI_HV | Leaf Area Index for high vegetation |

The manuscript labels Z as geopotential height but reports units of m²/s². Its precise representation and any conversion should be checked against the source data and implementation before assigning a definitive height unit.

### Derived Climate Indicators

The derived features include:

- **Relative Humidity (RH):** Calculated from air temperature and dew point to represent atmospheric moisture conditions.
- **Vapor Pressure Deficit (VPD):** Derived using relative humidity and saturation vapor pressure to represent atmospheric evaporative demand.
- **Growing Degree Days (GDD):** Reported as calculated daily using a base temperature of **10°C**, then summed monthly and seasonally.
- **Standardized Precipitation Index (SPI):** Calculated by fitting a gamma distribution to seasonal precipitation and transforming the cumulative probabilities to the standard normal distribution.
- **Climate anomalies:** Computed relative to long-term climatic means over the study period.
- **Seasonal aggregates:** Means for temperature variables and sums for precipitation and GDD, as described in Section 2.2.

Processed observations are organized by **year, season, grid cell, and climatic sub-region**.

## Climate Hazard Categories

The framework investigates seven binary hazard categories:

| Hazard | Description |
|---|---|
| Drought | A composite label involving SPI, temperature anomalies, soil-moisture anomalies, and VPD anomalies in the methods description |
| Heatwave | High-temperature hazard; temperature anomaly is identified as a label-defining variable |
| Cold spell | Cold-condition hazard |
| Hot and dry | Compound hot-and-dry hazard |
| Rain deficit | Precipitation-deficit hazard |
| Radiation deficit | Incoming-radiation-deficit hazard |
| Temperature accumulation deficit | Thermal-accumulation-deficit hazard relevant to crop development |

Labels represent hazard presence or absence. Initial threshold rules are informed by established hazard definitions and subsequently refined using regional climatic information and visual assessment in a two-dimensional PCA space.

PCA is used as a diagnostic aid; the manuscript explicitly states that **no automated threshold-optimization algorithm** was applied. It also states that adjustments were checked through subsequent classification performance and SHAP consistency.

The manuscript does not provide a complete numerical threshold specification for all seven hazards. The descriptions above should therefore not be treated as executable labeling rules.

## Methodology

The research workflow can be summarized in seven stages.

### 1. Climate Data Preparation

ERA5 variables are extracted for the study domain. Sea-surface grid points are removed, and terrestrial observations are assigned to non-overlapping sub-regions.

Regional datasets are organized for spring and autumn. Observations with missing values are removed during preprocessing.

### 2. Feature Engineering

RH, VPD, GDD, SPI, climate anomalies, and seasonal summaries are calculated to represent climatic conditions relevant to agricultural hazards.

The modeling data are split into training and testing subsets in a **70:30 ratio**. StandardScaler is fitted on the training subset and used to transform both subsets, according to Section 2.3.1.

### 3. Hazard Label Construction

Initial binary labels are assigned using threshold-based criteria.

For drought, the methods describe a composite condition involving **SPI, t2m_anom, swvl1_anom, and VPD_anom**.

Normalized climatic variables, excluding the hazard label itself, are projected into two dimensions using PCA. Visual assessment of class separability and local climatic patterns supports manual threshold refinement.

Label construction is described as a separate step from supervised model fitting. However, the manuscript also reports using subsequent model performance and SHAP consistency to assess the refinements; it does not establish that all such feedback was restricted to training data.

### 4. Leakage-Aware Feature Selection

The manuscript describes hazard-specific exclusion of important variables involved in label construction. Examples include **SPI for drought** and **temperature anomaly for heatwave**.

A variable excluded from one hazard model may remain available for another hazard when it is not part of that target's labeling logic. SPI is specifically discussed as a predictor for other hazards, including radiation deficit and heatwave.

The manuscript also makes broader claims about removing label-defining variables. These claims require reconciliation with Figure 7, which includes VPD_anom among the drought model's predictors even though Section 2.3.1 lists it in the drought-label definition. This README therefore does not assert that every label-defining variable was demonstrably excluded from every model.

### 5. XGBoost Model Training

Separate XGBoost classifiers are developed for each **hazard × sub-region × season** combination.

The reported training procedure includes:

- A **70:30 training–testing split**.
- Training-subset fitting of **StandardScaler**.
- **Stratified five-fold cross-validation**.
- **GridSearchCV** for hyperparameter optimization.
- **Balanced accuracy** as the model-selection and refit criterion.
- Tuning of tree depth, learning rate, regularization, and positive-class weighting.
- **reg_alpha** and **reg_lambda** for L1 and L2 regularization.
- **scale_pos_weight**, described in relation to class ratios and grid-search tuning.

Reported conservative parameter ranges include **max_depth ∈ {3, 5}** and **learning_rate ∈ {0.01, 0.03}**.

The manuscript additionally describes a sensitivity analysis in which balanced accuracy is averaged for each tree-depth and learning-rate value across the other grid-search settings.

### 6. Model Evaluation

The reported evaluation measures include:

- F1-score
- Balanced accuracy
- ROC-AUC
- Precision and recall
- Confusion matrices
- False-positive rate (FPR)
- False-negative rate (FNR)

Cross-validation means and standard deviations are used to assess variability. The selected models are retrained on the full training subset and evaluated on held-out test data.

Tables 1 and 2 report training F1, test F1, test AUC, and test-sample counts for autumn and spring, respectively. Tables 3 and 4 report confusion-matrix-derived metrics for drought and heatwave during spring and autumn.

### 7. SHAP-Based Model Interpretation

SHAP is applied after model training using **TreeExplainer**.

The study uses **global explanations**, specifically summary plots and mean absolute SHAP values, to identify influential predictors and compare regions. Section 3.3 explicitly states that instance-level interpretations, such as force plots or explanations of individual predictions, were not performed.

Figure 7 presents the autumn drought models across all four sub-regions. These attributions describe model behavior and climatic associations; they do not independently establish causal effects.

## Key Findings

### 1. Classification Performance Varies by Hazard and Region

Tables 1 and 2 show substantial differences across hazards, regions, and seasons.

Selected test-set results are:

| Season | Region | Hazard | Test F1-score |
|---|---|---|---:|
| Autumn | NE | Temperature accumulation deficit | 0.990 |
| Autumn | NE | Heatwave | 0.913 |
| Autumn | SW | Drought | 0.896 |
| Autumn | NW | Cold spell | 0.678 |
| Spring | NW | Heatwave | 0.891 |
| Spring | SW | Drought | 0.918 |
| Spring | SE | Temperature accumulation deficit | 0.927 |
| Spring | SW | Temperature accumulation deficit | 0.605 |

These values are transcribed from the **F1_Test** columns of the manuscript's autumn and spring tables. They are selected examples rather than averages across the full model set.

### 2. Regional Climatic Differences Matter

The study reports regional differences in model performance, hazard occurrence, and feature importance.

Its spatial results describe drought concentration in the northwest, heatwaves in the northeast, radiation deficits in the southwest, and temperature accumulation deficits in the southeast. Figure 5 additionally presents the two dominant hazards per grid cell and seasonal hazard composition.

These analyses motivate regional assessment. The manuscript does not report a direct performance comparison against a single province-wide baseline model.

### 3. Compound and Less Frequent Hazards Can Be More Challenging

Selected examples include autumn hot-and-dry classification in SE (**F1 = 0.723**), autumn cold-spell classification in NW (**F1 = 0.678**), and spring rain-deficit classification in NE (**F1 = 0.669**).

Difficulty varies by setting: hot-and-dry classification also reaches **0.872** in NW during autumn and **0.890** in SW during spring. Compound hazards therefore do not uniformly have the lowest scores.

The manuscript discusses physical complexity, limited positive samples, and incomplete representation of atmospheric dynamics as possible explanations for lower performance in some settings.

### 4. Humidity-Related Predictors Are Influential

For autumn drought, Section 3.3 and Figure 7 identify:

- **RH** as the leading predictor in **NE and NW**.
- **RH_anom** as the leading predictor in **SE and SW**.
- Region-dependent contributions from VPD-related features, GDD, and vegetation indicators.

The manuscript relates these differences to regional climatic conditions. The VPD_anom labeling-versus-predictor inconsistency noted above remains relevant when interpreting these results.

### 5. Leakage-Aware Modeling Supports Transparency

Explicit reporting of label definitions and hazard-specific predictor exclusions makes the intended relationship between labeling and model training easier to assess.

The manuscript presents this separation as a central methodological contribution. Its exact implementation should be verified using the final feature lists, labeling rules, and model inputs, particularly where the methods and SHAP figure differ.

## Research Limitations and Future Work

Several limitations and reporting ambiguities should be considered.

- **Subjective threshold refinement:** The manuscript acknowledges that visual PCA-based adjustment introduces subjectivity and proposes more objective, data-driven labeling protocols and quantitative diagnostics.
- **Independent observations:** The conclusions call for validation against in-situ or expert-based observations before operational deployment.
- **Feature-exclusion inconsistency:** VPD_anom is listed in the drought-label definition and also appears in the drought SHAP figure. The final label logic, model inputs, and figure provenance need to be reconciled before claiming complete removal of label-defining predictors.
- **Study-period inconsistency:** The abstract and Section 2.2 state **1940–2023**, whereas the download step in Figure 3 and the caption of Figure 4 state **1940–2025**. This README uses the period reported in the abstract and methods without treating the conflicting figure dates as resolved.
- **Data-source and variable ambiguities:** Section 2.2 emphasizes monthly single-level data but also describes daily data and daily GDD computation. The 500 hPa variable and its height/geopotential terminology likewise require precise source and unit documentation.
- **Label-calibration feedback:** Model performance and SHAP consistency were used to assess threshold refinements. The manuscript does not specify whether all such feedback was confined to training data.
- **Incomplete labeling specification:** A complete set of numerical thresholds for all hazards is not provided in the manuscript.
- **Validation scope:** The reported design uses a held-out split and stratified cross-validation; it does not document temporally blocked, spatially independent, or out-of-region evaluation.
- **SHAP's procedural role:** Section 3.3 describes post-training interpretation, while Section 3.4 refers to feature selection informed by SHAP. A separate SHAP-based feature-selection procedure is not sufficiently specified to reconstruct it from the manuscript.

Future directions explicitly discussed in the manuscript include:

- More objective and reproducible hazard-label calibration.
- Quantitative assessment of threshold refinement.
- Validation against independent observations.
- Integration of spatiotemporal models and atmospheric circulation variables.
- Improved representation of compound climate events.
- Testing transferability to other climate-vulnerable regions, including North Africa and Central Asia.

## Repository Organization

The manuscript does not provide a repository directory tree, notebook inventory, executable entry points, or a list of released datasets and model artifacts.

Accordingly, this README does not attribute specific folder names or file availability to the manuscript. The repository's actual files should be consulted to determine which components of data preparation, modeling, interpretation, and figure generation are available.

## Tools and Technologies

The manuscript explicitly names or describes the following components:

- **Python**, including the SHAP Python package.
- **XGBoost** for classification.
- **StandardScaler**, **GridSearchCV**, and **StratifiedKFold** from the scikit-learn workflow.
- **SHAP / TreeExplainer** for global feature attribution.
- **PCA** for exploratory projection and threshold diagnostics.
- **Cartopy** and **Shapely** for spatial processing.
- **Natural Earth** land masking.
- **ERA5** data obtained through the Copernicus Climate Data Store.

Package versions, an environment specification, and a complete dependency list are not provided in the manuscript.

## Data Availability, Privacy, and Reproducibility

**Important Notice — Source and Reproducibility Scope**

The manuscript's Data and Software Availability Statement identifies ERA5 reanalysis as publicly accessible through the Copernicus Climate Data Store:

[https://cds.climate.copernicus.eu](https://cds.climate.copernicus.eu)

That statement does not specify a public code archive, processed-data release, trained-model archive, software environment, or restrictions requiring redaction of research materials.

This README therefore makes no manuscript-derived claim that files have been omitted for privacy reasons or that all experiments can be reproduced from the repository alone.

Reproduction requires the actual data selection, preprocessing implementation, final hazard thresholds, predictor exclusions, split configuration, hyperparameter settings, and executable code. The reporting ambiguities identified above should be resolved against those materials.

## Research Context

This README describes the research manuscript:

**Multi-Hazard Climate Classification in Khuzestan: A Regionally Calibrated Approach Based on Local Thresholds and Spatiotemporal Patterns**

**Authors:** Mahboubeh Molavi-Arabshahi, Masoumeh Chalangaryamchi, and Erfan Shahabinezhad.

**Affiliation:** Department of Mathematics & Computer Science, Iran University of Science and Technology, Tehran, Iran.

The study integrates regional climate analysis, threshold-based hazard labeling, XGBoost modeling, and global SHAP interpretation. Its conclusions identify further observational validation as necessary before deployment.

The source for this README is the supplied manuscript **final-check (2).docx**. No journal publication status or publication year is assigned here because the supplied manuscript does not establish one.

## References

The manuscript includes a bibliography covering:

- ERA5 reanalysis and climate-data evaluation.
- Agricultural meteorology and climate hazards.
- Growing Degree Days and the Standardized Precipitation Index.
- PCA and dimensionality reduction.
- Machine learning, XGBoost, and model validation.
- SHAP and feature attribution for tree-based models.
- Regional climate-risk assessment and agricultural decision support.

Full bibliographic details are provided in the manuscript's References section. The dataset citation should be checked against the exact ERA5 products used: the methods name single-level data, whereas reference [21] is titled **ERA5 monthly averaged data on pressure levels from 1940 to present**.

## Disclaimer

Results in this README summarize the supplied manuscript and its reported evaluation settings. They have not been independently reproduced from code or validated against observations as part of preparing this document.

The study's historical classification results and SHAP attributions should be interpreted within the stated labeling, data, and validation constraints. The manuscript calls for further validation before operational use; its reported scores alone do not establish a validated early-warning service.
