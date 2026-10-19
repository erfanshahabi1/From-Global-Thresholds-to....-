Note on Data Privacy and Repository Content

To protect privacy and comply with data-sharing restrictions, the PDF document and certain other materials in this repository have been uploaded in partial or redacted form. Some information has been intentionally omitted from the publicly available files. These omissions do not necessarily reflect the complete materials used in the original research.

Overview
Climate extremes pose an increasing threat to agricultural productivity, water security, and environmental sustainability in climate-vulnerable regions. Khuzestan Province in southwestern Iran is particularly exposed to drought, extreme heat, precipitation deficits, and other climate-related hazards that can disrupt agricultural activities and intensify pressure on already limited water resources.

This project presents an explainable, regionally calibrated, and leakage-aware machine learning framework for classifying multiple climate hazards across Khuzestan's heterogeneous agro-climatic zones. The framework combines long-term ERA5 climate reanalysis data, scientifically informed hazard labeling, XGBoost classification, and SHAP-based feature attribution to investigate both the predictability and the climatic drivers of regional hazards.

Rather than applying a single province-wide model, the proposed methodology develops separate models for four sub-regions and two agriculturally important seasons: spring and autumn. This design allows the framework to account for spatial heterogeneity and differences in seasonal climate dynamics.

A central methodological principle is the explicit exclusion of label-defining variables from the corresponding model's input features. By preventing direct label-feature overlap, the framework aims to reduce information leakage and encourage learning from related but independent climatic signals.

The ultimate goal is to provide a transparent and reproducible foundation for regional climate-risk assessment, agricultural adaptation, and future climate-resilience decision-support systems.
Research Objectives
The project addresses five main objectives:
1. Regional climate modeling: Develop region-specific classifiers for four agro-climatic zones of Khuzestan.
2. Multi-hazard assessment: Investigate seven climate hazard categories across spring and autumn.
3. Leakage-aware learning: Exclude variables directly involved in defining each hazard label from the corresponding model's predictors.
4. Explainable predictions: Apply SHAP to identify the most influential climatic variables and examine how their importance varies geographically.
5. Robust evaluation: Assess classification performance using F1-score, balanced accuracy, ROC-AUC, confusion matrices, precision, recall, and false-positive and false-negative rates.
Study Area and Climate Data
The study focuses on the terrestrial area of Khuzestan Province, southwestern Iran, approximately bounded by 29.5°–33° N and 47°–51° E. To represent the province's climatic heterogeneity, the domain is divided into four sub-regions:
- NW — Northwest
- NE — Northeast
- SW — Southwest
- SE — Southeast
The analysis focuses on spring and autumn, two seasons associated with important agricultural activities, including sowing and harvesting.

The primary climate data source is ERA5 reanalysis from the Copernicus Climate Change Service. The manuscript describes a long-term analysis spanning 1940–2023, using atmospheric, precipitation, radiation, soil-moisture, wind, and vegetation-related variables, together with derived climate indicators.

The feature engineering stage includes variables such as:
- Relative Humidity (RH)
- Vapor Pressure Deficit (VPD)
- Growing Degree Days (GDD)
- Standardized Precipitation Index (SPI)
- Climate anomalies and seasonal aggregates
Terrestrial grid cells are retained while sea-surface grid points are excluded from the study domain.
Climate Hazards
The framework investigates seven binary climate hazard categories:
Hazard	Description
Drought	Conditions associated with precipitation, soil-moisture, and atmospheric dryness anomalies
Heatwave	Hazardous high-temperature conditions
Cold spell	Unusually cold conditions
Hot and dry	Compound hot-and-dry conditions
Rain deficit	Insufficient precipitation
Radiation deficit	Deficient incoming solar radiation
Temperature accumulation deficit	Insufficient thermal accumulation for crop developmentHazard labels are initially constructed using threshold-based criteria informed by established climate indicators. Regional climate patterns and PCA visualizations are used as supporting diagnostics during label refinement.

The labeling procedure is distinct from model training: variables directly used to define a particular hazard are excluded from that hazard's predictor set.
Methodology
The framework follows a structured workflow from climate-data preparation to model interpretation.
1. Climate Data Preparation
ERA5 variables are extracted for the study domain, filtered for terrestrial grid cells, and organized by year, season, and sub-region. Missing observations are handled before the modeling stage.
2. Feature Engineering
Raw meteorological variables are transformed into scientifically meaningful indicators, including humidity-related indices, atmospheric evaporative demand, thermal accumulation, precipitation indices, and climate anomalies.
3. Hazard Label Construction
Threshold-based rules define the presence or absence of each hazard. PCA visualizations support the examination of class separability and the regional consistency of the initial labels. PCA is used as a diagnostic tool rather than an automated threshold-optimization algorithm.
4. Leakage-Aware Feature Selection
For each hazard, the model excludes variables that directly encode the corresponding label definition. Variables may remain available for other hazard models when they are not directly involved in defining those labels.

This design reduces the risk that the classifier simply reproduces the threshold rules used to generate its targets.
5. XGBoost Model Training
Separate models are developed for each hazard, sub-region, and season. Hyperparameters are tuned using grid search and stratified five-fold cross-validation. The reported methodology includes regularization and class weighting to address model complexity and imbalanced hazard classes.
6. Model Evaluation
Performance is assessed using complementary metrics, including F1-score, balanced accuracy, ROC-AUC, precision, recall, and confusion-matrix-derived error rates. A held-out test set is used for final evaluation.
7. SHAP-Based Explainability
SHAP TreeExplainer is applied to trained XGBoost models to quantify global feature importance. Mean absolute SHAP values and summary plots are used to investigate the dominant predictors and their variation across hazards and sub-regions.
Key Findings
The reported experimental results indicate that the framework can distinguish many climate hazards with useful predictive performance, while revealing meaningful spatial differences in climatic feature importance.
- Strong classification performance: Many hazard models achieved test F1-scores in the approximate range of 0.80–0.90, although performance varied by hazard, region, and season.
- More challenging compound events: Hot-and-dry conditions and other less frequent hazards were generally harder to classify than some individual hazards.
- Regional differences matter: The dominant predictors were not uniform across the four sub-regions, supporting the use of regionally calibrated models rather than a single province-wide classifier.
- Humidity-related predictors are important: RH, RH anomalies, VPD, and other climate variables emerged as influential predictors in different regional and hazard-specific models.
- Leakage-aware design improves methodological transparency: Excluding label-defining features helps separate the operational construction of hazard labels from the predictive learning process.
These findings support further investigation of interpretable machine learning for agricultural climate-risk assessment. They should not be interpreted as proof of operational forecasting skill without additional temporal, spatial, and observational validation.