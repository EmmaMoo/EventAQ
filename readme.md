# Hierarchical Event Attribution Analysis for Air Quality

This repository contains the code and data used in the study:  
**"Hierarchical Event Attribution Analysis for Air Quality"**, with Beijing as a case study.  
We propose a multi-granularity spatiotemporal event analysis method using LLM-based event identification, hierarchical clustering, and interpretable machine learning.

---

## Repository Structure

- `rawdata.csv`  
  News texts collected from Weibo (2015–2023), filtered for Beijing-related content.

- `LLM-identify.py`  
  Uses a Large Language Model (LLM) to identify and extract real-world events from news data.

- `cluster.ipynb`  
  Performs hierarchical clustering of events using LLM embeddings and KMeans to build a macro–meso–micro event classification system.

- `xgboost.ipynb`  
  Trains an XGBoost model to predict air quality levels and uses SHAP to interpret the impact of social and meteorological events.

---

## Datasets Used

- **News Data**  
  Collected from Weibo using keyword-based crawling (2015–2023), saved in `rawdata.csv`.

- **Air Quality Data**  
  Sourced from the [Chinese Research Data Services (CNRDS) Platform](https://www.cnrds.com/).  
  *Note: Data access may require registration or institutional access.*

- **Meteorological Data**  
  Provided by Xiaolei Wang. Publicly available at [https://quotsoft.net/air/](https://quotsoft.net/air/).

---

## Requirements

- Python 3.8+
- OpenAI-compatible LLM API (e.g., GPT)
- Jupyter Notebook
- Required packages: `pandas`, `numpy`, `scikit-learn`, `xgboost`, `shap`, `openai`, `matplotlib`, etc.


