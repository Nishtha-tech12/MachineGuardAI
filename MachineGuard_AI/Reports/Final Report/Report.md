# MachineGuard AI
## Predictive Maintenance System Using Machine Learning and IBM Watsonx AI

---

# 1. Introduction

Industrial machines are critical components in manufacturing industries. Unexpected machine failures can result in production downtime, increased maintenance costs, and reduced operational efficiency.

**MachineGuard AI** is an AI-powered predictive maintenance system that uses machine sensor data to predict possible failures before they occur.

The system analyzes operational parameters such as temperature, rotational speed, torque, and tool wear to identify machine health conditions and provide maintenance recommendations.

The project integrates:

- Machine Learning for failure prediction
- IBM Watsonx AI for cloud-based prediction capability
- Streamlit for an interactive web interface
- IBM BOB assistance during development and IBM Cloud integration

---

# 2. Problem Statement

Traditional maintenance approaches mainly depend on two methods.

## Reactive Maintenance

- Maintenance is performed after machine failure.
- Causes unexpected downtime and production loss.

## Scheduled Maintenance

- Maintenance is performed at fixed intervals.
- May result in unnecessary maintenance or missed failures.

## Objective

MachineGuard AI aims to develop an intelligent system that can:

- Predict machine failure type.
- Identify machine health status.
- Provide preventive maintenance suggestions.
- Reduce unexpected downtime.

---

# 3. Dataset Description

The project uses the **Predictive Maintenance Dataset** from Kaggle containing machine operational information.

## Input Features

- Product ID
- Machine Type
- Air Temperature
- Process Temperature
- Rotational Speed
- Torque
- Tool Wear

## Target Variable

**Failure Type**

The target contains six classes:

- No Failure
- Heat Dissipation Failure
- Power Failure
- Overstrain Failure
- Tool Wear Failure
- Random Failure

---

# 4. Dataset Statistics

| Property | Value |
|-----------|-------|
| Dataset Source | Kaggle Predictive Maintenance Dataset |
| Total Records | 10,000 |
| Selected Input Features | 6 |
| Target Classes | 6 |
| Problem Type | Multi-Class Classification |

---

# 5. Data Preprocessing and Cleaning

## Data Cleaning

The following preprocessing steps were performed:

- Checked missing values
- Checked duplicate records
- Removed unnecessary columns
- Selected meaningful operational parameters
- Prepared the dataset for machine learning

## Feature Selection

The original dataset contained columns that were not useful for prediction.

Identifier-based columns were removed because they do not represent machine behavior.

### Final Features

- Machine Type
- Air Temperature (K)
- Process Temperature (K)
- Rotational Speed (RPM)
- Torque (Nm)
- Tool Wear (min)

---

# 6. Handling Data Leakage

Possible data leakage issues were identified during preprocessing.

Data leakage occurs when the model receives information during training that would not be available during real-world prediction.

To prevent this:

- Failure-related information was removed from the input features.
- Only real-time machine sensor parameters were used.
- The model was trained using information available before machine failure.

This improves prediction reliability in real-world industrial environments.

---

# 7. Machine Learning Models

MachineGuard AI uses two prediction approaches.

## Model 1 – Random Forest Classifier

The first model is a locally trained **Random Forest Classifier** using Scikit-learn.

### Purpose

- Local prediction model
- Offline fallback prediction
- Reliable multi-class classification

### Advantages

- Handles nonlinear relationships
- High prediction accuracy
- Robust against noisy sensor data
- Fast inference

---

## Model 2 – IBM Watsonx AI Cloud Prediction Service

The application integrates **IBM Watsonx AI** using IBM Cloud Lite Services.

### Purpose

- Cloud-based prediction
- IBM Cloud integration
- Scalable deployment

If IBM Watsonx AI is unavailable, the application automatically switches to the local Random Forest model.

### Prediction Flow

```text
User Input
     |
     v
IBM Watsonx AI
     |
Prediction

If Cloud Unavailable
     |
     v
Random Forest Model
```

---

# 8. IBM BOB Assistance

IBM BOB assisted during the project development process by:

- Supporting application development
- Assisting IBM Watsonx AI integration
- Helping with debugging and workflow understanding
- Improving project implementation

IBM BOB acted as an AI development assistant throughout the project lifecycle.

---

# 9. System Architecture

```text
                User
                  |
                  v
        Streamlit Application
                  |
                  v
          Prediction API Layer
                  |
        -------------------------
        |                       |
        v                       v
 IBM Watsonx AI         Random Forest Model
        |                       |
        -----------Fallback------
                  |
                  v
      Failure Classification
                  |
                  v
Severity Detection & Recommendation Engine
                  |
                  v
     Maintenance Action Report
```

---

# 10. Application Development

## Technology Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python |
| Frontend | Streamlit |
| Machine Learning | Scikit-learn |
| Model Storage | Joblib |
| Cloud AI | IBM Watsonx AI |
| Development Assistant | IBM BOB |

## Application Features

MachineGuard AI provides:

- User-friendly sensor input interface
- Machine failure prediction
- Prediction confidence score
- Failure severity classification
- Maintenance recommendations
- IBM Watsonx AI cloud prediction
- Local Random Forest fallback prediction

## Project Structure

```text
MachineGuardAI-App/
│
├── app.py
├── api/
│   └── ibm_predict.py
├── pages/
│   └── Predict.py
├── models/
│   ├── predictive_model.joblib
│   └── label_encoder.joblib
├── recommendations.py
├── train_local_model.py
├── requirements.txt
├── assets/
├── utils/
└── data/
```

---

# 11. Results and Testing

## Example 1 – Normal Machine Condition

**Prediction:** No Failure

**Confidence:** 100%

The system correctly identifies normal operating conditions.

---

## Example 2 – Failure Detection

**Prediction:** Overstrain Failure

**Confidence:** 42.2%

**Severity:** Critical

### Recommended Actions

- Stop machine operation
- Reduce mechanical load
- Inspect machine components
- Replace damaged tools

---

# 12. Conclusion

MachineGuard AI successfully demonstrates an AI-based predictive maintenance solution using Machine Learning and IBM Watsonx AI.

The application can:

- Analyze machine sensor data
- Predict possible failures
- Provide maintenance recommendations
- Support preventive maintenance
- Continue prediction through a local fallback model when cloud prediction is unavailable

The combination of Machine Learning, IBM Cloud services, and Streamlit creates an efficient industrial predictive maintenance solution.

---

# 13. Future Scope

Future improvements include:

- Real-time IoT sensor integration
- Live machine monitoring
- Deep Learning-based predictive models
- Automated maintenance scheduling
- Industrial dashboard integration
- ERP and MES integration
- Mobile application support
