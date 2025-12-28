# VolunteerMLOps: End-to-End MLOps Pipeline for Beach Volunteer Turnout Prediction

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![DVC](https://img.shields.io/badge/DVC-Data_Version_Control-9cf.svg)](https://dvc.org/)

> **An automated machine learning operations (MLOps) pipeline for predicting volunteer turnout at beach cleanup events.**

This project demonstrates production-ready ML infrastructure incorporating Continuous Integration/Continuous Deployment (CI/CD), data versioning, containerization, and cloud deployment.

---

## 📑 Table of Contents
- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start-local)
- [API Usage](#-api-usage)
- [CI/CD Pipeline](#-cicd-github-actions)
- [Configuration](#-configuration)
- [Model Performance](#-model-performance-reference)
- [Future Work](#-limitations-and-future-work)
- [Authors](#-authors-and-acknowledgments)

---

## 📊 Project Overview

Environmental organizations often struggle to predict volunteer attendance at beach cleanup events. This uncertainty leads to resource wastage (overstaffing) or insufficient workforce (understaffing). 

**VolunteerMLOps** addresses this problem using an end-to-end pipeline that:
- **Predicts attendance** with high accuracy ($R^2 \approx 0.93$) based on historical event records.
- **Automates deployment** from code push to production via GitHub Actions.
- **Ensures reproducibility** through DVC (Data Version Control) and model versioning.
- **Scales efficiently** via containerized infrastructure (Docker) on AWS.

The core model is a **Random Forest Regressor** trained on features such as seasonality, time of day, and registration data.

---

## 🎯 Key Features

### Machine Learning
- **Model:** Random Forest Regressor.
- **Input Features:**
  - `Month` (1–12)
  - `Day of week` (0–6)
  - `Time of day` (0–23)
  - `Is holiday` (Binary: 0/1)
  - `Beach ID` (Categorical: 1–5)
  - `Registered volunteers` (Integer count)
- **Output:** Predicted volunteer turnout (Continuous).

### MLOps Infrastructure
- **Data Version Control (DVC):** Tracks datasets, models, and pipeline stages.
- **GitHub Actions:** Automates the CI/CD pipeline (Process $\rightarrow$ Train $\rightarrow$ Evaluate $\rightarrow$ Build $\rightarrow$ Push).
- **Docker:** Containerizes the Flask web service and model for consistent deployment.
- **AWS Integration:** - **S3:** Artifact and data storage.
  - **ECR:** Container registry.
  - **EC2:** Production deployment.
- **Validation Gates:** Automated checks ensure only models meeting metric thresholds are deployed.

---

## 🏗️ Architecture



**The High-Level Data Flow:**

1.  **Ingestion:** Raw data (CSV) is stored in AWS S3.
2.  **Orchestration:** DVC pulls data and manages the pipeline DAG (Directed Acyclic Graph):
    * Preprocessing & Splitting
    * Model Training
    * Evaluation & Metrics Logging
3.  **CI/CD:** GitHub Actions triggers on every push to `main`.
4.  **Deployment:** If metrics pass defined thresholds, a Docker image is built, pushed to AWS ECR, and served via AWS EC2.
5.  **Inference:** The API is exposed via Flask (Gunicorn in production) for real-time predictions.

---

## 📦 Project Structure

```bash
volunteer-turnout-mlops/
├── .github/
│   └── workflows/
│       └── mlops-pipeline.yml      # CI/CD workflow definition
├── app/
│   ├── app.py                      # Flask REST API entry point
│   └── templates/
│       └── index.html              # Frontend UI (optional)
├── data/
│   ├── raw/                        # Raw CSV data (tracked by DVC)
│   └── processed/                  # Transformed data (tracked by DVC)
├── models/
│   ├── model.joblib                # Serialized Random Forest model
│   └── feature_names.joblib        # Feature metadata
├── metrics/
│   └── metrics.json                # Evaluation results
├── src/
│   ├── process.py                  # Data cleaning & splitting
│   ├── train.py                    # Model training script
│   ├── evaluate.py                 # Evaluation & metrics generation
│   └── validate_model.py           # Deployment gate logic
├── dvc.yaml                        # DVC pipeline stages
├── params.yaml                     # Hyperparameters & configuration
├── Dockerfile                      # Container build specification
├── requirements.txt                # Python dependencies
└── README.md
