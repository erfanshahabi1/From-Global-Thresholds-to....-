# Regional Insights: An Explainable AI Framework for Classifying Climate Hazards in Khuzestan

**Machine Learning | Climate Risk Assessment | XGBoost | SHAP | ERA5 | Explainable AI**

## Overview

Climate extremes pose significant challenges to agricultural productivity, water security, and environmental sustainability, particularly in climate-vulnerable regions such as Khuzestan Province in southwestern Iran.

This research develops a **regionally calibrated, explainable, and leakage-aware machine learning framework** for classifying seven climate hazards across four agro-climatic sub-regions of Khuzestan.

Using long-term ERA5 climate reanalysis data, the framework integrates scientifically informed hazard labeling, feature engineering, XGBoost classification, hyperparameter optimization, and SHAP-based model interpretation.

Unlike approaches that treat the entire province as a single homogeneous region, this study develops separate classification models for four sub-regions and two agriculturally important seasons: **spring and autumn**.

A central methodological consideration is the exclusion of variables directly involved in defining each hazard label from the corresponding model's predictors. This reduces direct label-feature overlap and encourages the models to identify related climatic patterns rather than simply reproduce the original threshold rules.

The project aims to contribute to interpretable climate-risk assessment and provide a foundation for future research on agricultural adaptation and climate-resilience decision support.

## Research Objectives

The main objectives of this research are:

1. **Regional climate hazard classification:** Develop separate machine learning models for four agro-climatic sub-regions of Khuzestan.
2. **Multi-hazard assessment:** Classify seven climate hazards during spring and autumn.
3. **Leakage-aware modeling:** Reduce direct target leakage by excluding hazard-label-defining variables from the corresponding predictor sets.
4. **Explainable AI:** Apply SHAP to identify influential climatic predictors and examine regional differences in model behavior.
5. **Model evaluation:** Assess classification performance using complementary metrics, including F1-score, balanced accuracy, ROC-AUC, precision, recall, and confusion matrices.

## Study Area

The study focuses on the terrestrial area of Khuzestan Province, southwestern Iran, approximately bounded by:

- **Latitude:** 29.5°–33° N
- **Longitude:** 47°–51° E

The study domain is divided into four sub-regions:

| Code | Sub-region |
|---|---|
| NW | Northwest |
| NE | Northeast |
| SW | Southwest |
| SE | Southeast |

The regional division uses approximately 31.25° N and 49° E as spatial boundaries, representing the study's four climatic subdivisions.

Only terrestrial grid cells are included; sea-surface grid points are excluded.

Spring and autumn are selected because of their importance for agricultural activities, including sowing and harvesting.

## Climate Data and Feature Engineering

### Data Source

The primary data source is **ERA5 reanalysis**, provided by the Copernicus Climate Change Service (C3S).

The manuscript describes an analysis covering **1940–2023**, using ERA5 climate data at approximately 0.25° spatial resolution.

### Primary Climate Variables

The study incorporates variables representing atmospheric, hydrological, surface, and vegetation conditions.

| Variable | Description |
|---|---|
| T2M | 2-meter air temperature |
| D2M | 2-meter dew point temperature |
| TP | Total precipitation |
| SSRD | Surface solar radiation downwards |
| Z | Geopotential |
| SWVL1 | Topsoil volumetric moisture |
| U10 | 10-meter eastward wind component |
| V10 | 10-meter northward wind component |
| LAI_LV | Leaf Area Index for low vegetation |
| LAI_HV | Leaf Area Index for high vegetation |

### Derived Climate Indicators

Additional features are engineered to represent agriculturally relevant climate processes:

- **Relative Humidity (RH):** Atmospheric moisture conditions.
- **Vapor Pressure Deficit (VPD):** Atmospheric evaporative demand and potential plant water stress.
- **Growing Degree Days (GDD):** Temperature accumulation relevant to crop development, calculated using a base temperature of 10°C.
- **Standardized Precipitation Index (SPI):** Standardized precipitation anomalies associated with meteorological drought.
- **Climate anomalies:** Deviations from long-term climatological conditions.
- **Seasonal aggregates:** Climate indicators summarized for spring and autumn.

The processed observations are organized by year, season, terrestrial grid cell, and sub-region.

## Climate Hazard Categories

The framework investigates seven binary climate hazard categories.

| Hazard | Description |
|---|---|
| Drought | Conditions involving precipitation, soil-moisture, temperature, and atmospheric dryness anomalies |
| Heatwave | Abnormally high-temperature conditions |
| Cold spell | Unusually cold conditions |
| Hot and dry | Compound high-temperature and dry conditions |
| Rain deficit | Insufficient precipitation |
| Radiation deficit | Deficient incoming solar radiation |
| Temperature accumulation deficit | Insufficient thermal accumulation relevant to crop development |

Hazard labels are constructed using threshold-based criteria informed by established climate indicators and regional climatic characteristics.

Principal Component Analysis (PCA) visualizations support the examination of class separability and regional consistency. PCA serves as a diagnostic tool rather than an automated threshold-optimization method.

## Methodology

The research follows a structured workflow consisting of seven major stages.

### 1. Climate Data Preparation

ERA5 climate variables are extracted for the study domain. Sea-surface grid points are excluded, and the remaining observations are organized by year, season, and sub-region.

Missing observations are removed during preprocessing.

### 2. Feature Engineering

Raw meteorological variables are transformed into derived climate indicators, including RH, VPD, GDD, SPI, anomalies, and seasonal aggregates.

These features provide representations of climatic conditions relevant to agricultural hazards.

### 3. Hazard Label Construction

Binary hazard labels are initially generated using scientifically informed threshold-based rules.

PCA visualizations are subsequently used to examine class separability and support regionally informed assessment of the labels.

The labeling procedure remains distinct from the supervised model-training stage.

### 4. Leakage-Aware Feature Selection

For each hazard, variables directly involved in defining its target label are excluded from the corresponding model's predictor set.

For example, SPI is excluded from the drought classifier when it contributes to the drought-label definition, but may remain available for other hazard models where it is not used to construct the target.

This strategy reduces direct label-feature leakage. It does not, by itself, eliminate every possible form of information leakage or dependence between predictors and targets.

### 5. XGBoost Model Training

Separate XGBoost classifiers are developed for each combination of hazard, sub-region, and season.

The reported modeling procedure includes:

- A 70:30 training–testing split.
- StandardScaler normalization fitted on the training subset.
- Stratified five-fold cross-validation.
- GridSearchCV for hyperparameter optimization.
- Balanced accuracy as the grid-search refitting criterion.
- Regularization and class weighting, including `scale_pos_weight`, to address model complexity and class imbalance.

### 6. Model Evaluation

The trained classifiers are evaluated using:

- F1-score
- Balanced accuracy
- ROC-AUC
- Precision and recall
- Confusion matrices
- False-positive and false-negative rates

Held-out test-set results are used to assess classification performance beyond the training data.

### 7. SHAP-Based Model Interpretation

SHAP (Shapley Additive exPlanations) is applied to the trained XGBoost classifiers to investigate feature contributions.

TreeExplainer, mean absolute SHAP values, and summary plots are used to examine influential predictors across hazards and sub-regions.

The analysis provides insight into model behavior and regional differences in climatic associations. SHAP feature attribution should not be interpreted as direct evidence of causality.

## Key Findings

### 1. Classification Performance Varies by Hazard and Region

The framework achieves useful classification performance for multiple climate hazards, although results differ substantially across seasons, regions, and hazard categories.

Selected results reported in the manuscript include:

| Season | Region | Hazard | Test F1-score |
|---|---|---|---|
| Autumn | NE | Temperature accumulation deficit | 0.990 |
| Autumn | NE | Heatwave | 0.913 |
| Autumn | SW | Drought | 0.896 |
| Autumn | NW | Cold spell | 0.678 |
| Spring | NW | Heatwave | 0.891 |
| Spring | SW | Drought | 0.918 |
| Spring | SE | Temperature accumulation deficit | 0.927 |
| Spring | SW | Temperature accumulation deficit | 0.605 |

These examples illustrate both strong-performing models and more challenging classification settings.

### 2. Regional Climatic Differences Matter

Model performance and feature importance vary across Khuzestan's four sub-regions.

This variation supports the investigation of region-specific modeling strategies rather than relying exclusively on province-wide averages.

### 3. Compound and Less Frequent Hazards Can Be More Challenging

Some compound hot-and-dry events, cold spells, and precipitation-related hazards exhibit lower classification performance.

Their relative difficulty varies by region and season, highlighting the complexity of regional climate-hazard classification.

### 4. Humidity-Related Predictors Are Influential

SHAP analysis identifies relative humidity, humidity anomalies, vapor pressure deficit, and other meteorological indicators as influential predictors in several models.

Their relative importance varies across hazards and geographic regions.

### 5. Leakage-Aware Modeling Supports Transparency

Explicit separation between hazard-label construction and predictor selection provides a clearer methodological distinction between the target definitions and the features used for classification.

This improves the transparency of the modeling framework and motivates further investigation of its generalizability.

## Research Limitations and Future Work

Several limitations should be considered when interpreting the results.

**Threshold-based labels:** Hazard labels are constructed using scientifically informed thresholds and regionally informed visual assessment. PCA-supported refinement introduces a degree of subjectivity.

**Validation strategy:** The reported evaluation uses held-out testing and stratified cross-validation. Additional temporally blocked, spatially independent, and out-of-region validation would be valuable for assessing generalization under changing climate conditions.

**Operational forecasting:** Classification performance on historical reanalysis observations does not establish operational forecasting capability or future-event prediction skill.

**Data dependence:** The framework relies primarily on ERA5 reanalysis. Independent observational validation would strengthen the assessment of real-world applicability.

Future research directions include:

- More objective and reproducible hazard-threshold calibration.
- Temporal and spatial out-of-sample validation.
- Integration of atmospheric circulation and spatiotemporal predictors.
- Further investigation of compound climate extremes.
- Evaluation against independent observations.
- Extension to other climate-vulnerable agricultural regions.

## Repository Organization

The repository contains publicly shareable research materials, including selected datasets, Jupyter notebooks, documentation, and supporting figures.

The principal repository directories include:

- `Data/` — Available data resources and supporting files.
- `Notebooks/` — Jupyter notebooks associated with data processing, modeling, and analysis.
- `README/` — Additional documentation, where applicable.

Other project materials and references are provided in the repository where publicly available.

The public repository may not contain every dataset, intermediate output, or research artifact used during the original study.

## Tools and Technologies

The project uses a Python-based data science and machine learning workflow, including:

- Python
- Jupyter Notebook / Google Colab
- XGBoost
- Scikit-learn
- SHAP
- NumPy and Pandas
- Matplotlib
- ERA5 climate reanalysis data
- PCA for exploratory diagnostics

Additional scientific and geospatial libraries are used for climate-data preparation and spatial analysis.

## Data Availability, Privacy, and Reproducibility

**Important Notice — Public Repository Limitations**

To respect privacy, applicable data-sharing restrictions, and research-material distribution constraints, the manuscript PDF and selected supporting materials are provided in partial or redacted form.

Some information has been intentionally omitted from publicly accessible files. These omissions do not necessarily reflect the complete materials used during the original research.

The repository is intended to document the research approach, demonstrate selected implementation components, and communicate the principal methodological contributions.

Because some materials are incomplete or unavailable publicly, full reproduction of every reported experiment and result may not be possible using the repository alone.

Users should review the available documentation and notebooks to determine which components can be independently executed or reproduced.

## Research Context

This repository accompanies the research manuscript:

**Regional Insights: An Explainable AI Framework for Classifying Climate Hazards in Khuzestan**

The research investigates the integration of regional climate analysis, interpretable machine learning, and leakage-aware feature selection for multi-hazard classification.

The framework is intended as a research contribution and foundation for further development, rather than a validated operational early-warning system.

## References

The research draws on established literature in climate reanalysis, agricultural meteorology, machine learning, and explainable artificial intelligence.

Relevant topics include:

- ERA5 climate reanalysis and the Copernicus Climate Change Service.
- XGBoost and gradient-boosted decision trees.
- SHAP-based model interpretation.
- Standardized Precipitation Index (SPI).
- Growing Degree Days (GDD).
- Regional climate-hazard assessment.

Additional bibliographic information is provided in the research manuscript and accompanying reference materials.

## Disclaimer

The findings are based on the data, labeling procedures, and evaluation settings described in the associated research manuscript.

Model classifications and SHAP explanations should be interpreted within these methodological boundaries and should not be used as standalone operational forecasts or agricultural risk-management decisions without further validation.
