# MachineGuard AI App

> **An AI-powered Predictive Maintenance Application built using Streamlit, Machine Learning, IBM Watsonx AI, and IBM Cloud Lite Services.**

---

## Overview

MachineGuard AI is an intelligent predictive maintenance application that predicts industrial machine failures using real-time operational sensor data.

The application integrates a **locally trained Random Forest model** with **IBM Watsonx AI** to provide accurate failure predictions and maintenance recommendations. If the IBM cloud service is unavailable, the application automatically switches to the local model, ensuring uninterrupted predictions.

---

## Features

- Predict machine failure types
- IBM Watsonx AI cloud prediction
- Automatic Local Random Forest fallback
- Prediction confidence score
- Severity classification
- Maintenance recommendations
- Interactive Streamlit interface
- Real-time prediction workflow

---

# Application Workflow

```text
User Input
     │
     ▼
Streamlit Web Interface
     │
     ▼
Prediction API
     │
───────────────
│             │
▼             ▼
IBM Watsonx AI    Local Random Forest
       │
       └──────Fallback──────┐
                             ▼
                  Failure Prediction
                             │
                             ▼
                 Recommendation Engine
                             │
                             ▼
                  Maintenance Report
```

---

# Machine Learning

## Local Model

- Random Forest Classifier
- Trained using Scikit-learn
- Saved using Joblib
- Offline prediction support

## Cloud AI

IBM Watsonx AI

- IBM Cloud Lite integration
- Cloud-based prediction service
- Automatic fallback to the local model

---

# Input Parameters

The application accepts the following machine parameters:

- Product Type
- Air Temperature
- Process Temperature
- Rotational Speed
- Torque
- Tool Wear

---

# Output

The application provides:

- Predicted Failure Type
- Prediction Confidence
- Prediction Source
- Failure Severity
- Maintenance Recommendation
- Recommended Maintenance Actions

---

# Technology Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| Frontend | Streamlit |
| Machine Learning | Scikit-learn |
| Cloud AI | IBM Watsonx AI |
| Model Storage | Joblib |
| API | Requests |
| Environment | Python Dotenv |

---

# 🤖 IBM Technologies Used

- IBM Cloud Lite
- IBM Watsonx AI
- IBM Watson Machine Learning Deployment
- IBM Identity and Access Management (IAM)

---

# IBM BOB

This project was developed with assistance from **IBM BOB (Build Operations Bot)** during the IBM SkillsBuild internship.

IBM BOB assisted in:

- Understanding IBM Cloud services
- IBM Watsonx AI integration
- Deployment workflow guidance
- Debugging and implementation support
- Improving the overall application development process

IBM BOB served as an AI development assistant throughout the project lifecycle.

---

⭐ If you found this project useful, consider giving the repository a star.
