# 🚀 MachineGuard AI
### Predictive Maintenance System for Industrial Machinery using Machine Learning and IBM Watsonx AI

---

## 📌 Project Overview

MachineGuard AI is an intelligent predictive maintenance application that predicts industrial machine failures using machine learning and IBM Watsonx AI.

The application analyzes real-time machine sensor data to identify possible failure types before breakdowns occur and provides maintenance recommendations to reduce downtime and operational costs.

If IBM Watsonx AI is unavailable, the system automatically switches to a locally trained Random Forest model, ensuring uninterrupted predictions.

---

## 🎯 Problem Statement

**IBM SkillBuild Internship**

**Problem Statement No. 39**

Develop a predictive maintenance model for industrial machinery capable of predicting machine failures before they occur using operational sensor data.

The system should identify the failure type and assist industries in reducing maintenance costs and unexpected downtime.

---

# 🏭 Project Domain

**Manufacturing Industry**

**Industrial Automation**

**Predictive Maintenance**

---

# ✨ Features

-Predict machine failures
-IBM Watsonx AI integration
-Local Random Forest fallback model
-Prediction confidence score
-Failure severity detection
-Intelligent maintenance recommendations
-Interactive Streamlit dashboard

---

# Machine Learning Models

## Model 1

**Random Forest Classifier**

- Trained using Scikit-learn
- Local prediction engine
- Offline fallback support

---

## Model 2

**IBM Watsonx AI**

- Cloud prediction service
- IBM Cloud Lite integration
- Automatic fallback to local model

---

#  Dataset

**Source**

Kaggle Predictive Maintenance Dataset

Dataset contains:

- Machine Type
- Air Temperature
- Process Temperature
- Rotational Speed
- Torque
- Tool Wear

Target Variable:

- Failure Type

---

# Data Preprocessing

The dataset was cleaned before model training.

Steps performed:

- Missing value analysis
- Duplicate removal
- Removal of unnecessary columns
- Feature selection
- Data leakage prevention

Final selected features:

- Machine Type
- Air Temperature
- Process Temperature
- Rotational Speed
- Torque
- Tool Wear

---

# System Architecture

```text
User
   │
   ▼
Streamlit Web App
   │
   ▼
Prediction API
   │
───────────────
│             │
▼             ▼
IBM Watsonx AI      Random Forest
       │
       └── Fallback
             │
             ▼
Failure Prediction
             │
             ▼
Severity Detection
             │
             ▼
Maintenance Recommendation
```

---

# 🛠 Technology Stack

| Category | Technology |
|-----------|------------|
| Programming Language | Python |
| Frontend | Streamlit |
| Machine Learning | Scikit-learn |
| Cloud AI | IBM Watsonx AI |
| Model Storage | Joblib |
| Environment | Python Dotenv |
| API | Requests |

---


# 📊 Example Prediction

### Input

- Product Type: M
- Air Temperature: 298.5 K
- Process Temperature: 308.7 K
- Rotational Speed: 1500 rpm
- Torque: 42 Nm
- Tool Wear: 50 min

### Output

Prediction:

**No Failure**

or

**Overstrain Failure**

The application displays:

- Prediction
- Confidence Score
- Severity Level
- Maintenance Recommendation

---

# 🔮 Future Scope

- IoT sensor integration
- Live machine monitoring
- Deep Learning models
- Automated maintenance scheduling
- Mobile application
- ERP integration

---


# 🔗 Links

**Live Streamlit Application**

(Add your Streamlit Cloud link after deployment)

---

## ⭐ If you found this project helpful, consider giving it a Star!
