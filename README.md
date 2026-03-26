# 🚀 Agile Sprint Failure Prediction System

![Sprint Risk Banner](https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:203a43,100:2c5364&height=300&section=header&text=Sprint%20Risk%20Analytics&fontSize=60&animation=fadeIn&fontAlignY=35&desc=Predictive%20Agile%20Intelligence%20%7C%20MLOps%20%E2%80%A2%20Risk%20Forecasting&descAlignY=60&descSize=20&fontColor=ffffff)
[![Status](https://img.shields.io/badge/Status-Work_In_Progress-FFC107?style=for-the-badge&logo=git&logoColor=black)](#-current-development-status)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Airflow](https://img.shields.io/badge/MLOps-Apache_Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)](https://airflow.apache.org/)
[![XGBoost](https://img.shields.io/badge/ML-XGBoost-17B41C?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.ai/)
[![React](https://img.shields.io/badge/Frontend-React_(WIP)-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)

> **An intelligent predictive analytics platform designed to evaluate software development sprints and forecast the probability of failure based on team composition, code churn, and task complexity.**

---

## 🚧 Current Development Status

**Phase 3: Frontend Interface Integration (Currently In Progress)**

* ✅ **Phase 1: ML Pipeline (Completed):** XGBoost classification model and NLP text processing pipeline built, tuned via `GridSearchCV`, and serialized.
* ✅ **Phase 2: Backend & MLOps (Completed):** FastAPI inference server deployed. Apache Airflow DAGs configured for daily automated data extraction and model retraining.
* ⏳ **Phase 3: Frontend Dashboard (In Progress):** Currently building the user interface to allow project managers to input sprint metrics and visualize risk factors in real-time.

---

## 📌 Project Overview
The **Sprint Failure Prediction System** acts as an AI safety net for engineering managers. By analyzing historical Jira and GitHub data, the system identifies mathematical and linguistic patterns that lead to sprint bottlenecks, missed deadlines, or buggy releases.

Instead of relying on gut feeling, project managers can input proposed sprint metrics and receive an instant, data-driven risk assessment before committing to the workload.

### 🎯 Key Features
* **🧠 Hybrid Machine Learning:** Combines numerical analysis (code churn, team seniority) with Natural Language Processing (TF-IDF on sprint descriptions) to gauge true complexity.
* **⚙️ Automated MLOps Pipeline:** Utilizes Apache Airflow to extract fresh sprint data via SQL, retrain the model, and deploy the updated artifact automatically.
* **⚡ Real-Time API Inference:** A FastAPI backend processes incoming JSON payloads, decodes the feature space, and returns a strict probability score and categorical risk flag.
* **📈 Actionable Risk Factors:** Identifies exactly *why* a sprint is risky (e.g., "Code churn exceeds safe thresholds for the current team seniority").

---

## ⚙️ Technology Stack

| Component | Tech Stack | Description |
| :--- | :--- | :--- |
| **Frontend (WIP)** | React.js, Tailwind CSS | Dashboard for sprint risk visualization and payload submission |
| **Backend** | FastAPI (Python), Uvicorn | High-performance asynchronous REST API |
| **Data Orchestration**| Apache Airflow, Docker | DAG-based scheduling for ETL and automated model retraining |
| **Database** | MySQL | Relational storage for historical agile sprint records |
| **AI / ML** | Scikit-Learn, XGBoost, Pandas | `ColumnTransformer` pipelines combining `TfidfVectorizer` and gradient boosting |

---

## 🔄 System Architecture & Workflow

The system is designed with a strict separation of concerns, ensuring the heavy ML training loop does not block the real-time API serving the frontend.

1.  **Data Extraction:** Airflow cron jobs execute `query.sql` against the data warehouse to pull completed sprint metrics.
2.  **Continuous Training:** The Airflow worker passes the `pandas` DataFrame into the Scikit-Learn pipeline, optimizing `max_depth` and `max_features` on the fly.
3.  **Real-Time Evaluation:** The frontend sends a proposed sprint payload (Seniority Ratio, Churn, Description) to the FastAPI `/predict` endpoint.
4.  **Instant Feedback:** The API returns a risk probability (e.g., 85% chance of failure) and highlights specific warnings for the project manager.

---

## 🧠 Machine Learning & MLOps Implementation
> **Theme:** Automated Feature Engineering & Gradient Boosting

Predicting human performance and software complexity requires a model that can handle non-linear relationships and sparse text data simultaneously. 

### 🛡️ Implemented ML Controls

#### 1️⃣ Unified Transformation Pipeline
* **Mechanism:** Scikit-Learn `ColumnTransformer` handles disparate data types in a single pass.
* **NLP:** `TfidfVectorizer` parses the `sprint_description`, identifying high-risk keywords (e.g., "legacy", "migration", "rewrite").
* **Numeric:** Pass-through routing for `team_seniority_ratio` and `code_churn_lines` directly into the boosting trees.

#### 2️⃣ XGBoost Classification
* **Optimization:** Hyperparameters tuned via `GridSearchCV` to balance tree depth and learning rate, preventing overfitting on small agile teams.
* **Evaluation:** Optimized for `roc_auc` to ensure the model confidently separates successful sprints from catastrophic failures.

#### 3️⃣ Airflow DAG Automation
* **Resilience:** The `@task` decorators manage state between data extraction and model training.
* **Isolation:** Runs inside a Dockerized Linux container to ensure environment parity with production servers.

---

## 🚀 Future Roadmap

### 💻 Frontend Enhancements (Current Focus)
- [ ] **Risk Gauges:** Implement dynamic Chart.js radial gauges to display the `risk_probability` score.
- [ ] **Form Validation:** Build strict client-side constraints (e.g., Seniority Ratio must be 0.0 - 1.0) before calling the API.

### 🧠 System Enhancements
- [ ] **SHAP Integration:** Use Shapley values to dynamically generate the `primary_risk_factors` array rather than relying on hardcoded thresholds.
- [ ] **Webhook Integration:** Connect the FastAPI endpoint directly to Jira/GitHub webhooks for automated PR/Sprint scoring.

---

## 👥 Contributors
* **Ujjwal Upreti**

---

## 💻 Frontend Interface
*(Screenshot will be added upon completion of the React dashboard)*
