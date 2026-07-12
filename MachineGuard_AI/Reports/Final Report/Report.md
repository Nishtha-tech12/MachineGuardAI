# **MachineGuard AI**

### Predictive Maintenance System Using Machine Learning and IBM Watsonx AI



**1. Introduction**



Industrial machines are critical components in manufacturing industries. Unexpected machine failures can result in production downtime, increased maintenance costs, and reduced operational efficiency.



MachineGuard AI is an AI-powered predictive maintenance system that uses machine sensor data to predict possible failures before they occur.



The system analyzes operational parameters such as temperature, rotational speed, torque, and tool wear to identify machine health conditions and provide maintenance recommendations.



The project integrates:



Machine Learning for failure prediction

IBM Watsonx AI for AI-based prediction capability

Streamlit for interactive user interface

IBM BOB (Build Operations Bot) for intelligent operational assistance and project demonstration



**2. Problem Statement**



Traditional maintenance approaches mainly depend on:



1\. Reactive Maintenance



Maintenance is performed after machine failure.

Causes unexpected downtime and production loss.



2\. Scheduled Maintenance



Maintenance is performed at fixed intervals.

May result in unnecessary maintenance or missed failures.



**The objective of MachineGuard AI is to develop an intelligent system that:**



Predicts machine failure type.

Identifies machine health status.

Provides preventive maintenance suggestions.

Reduces unexpected downtime.



**3. Dataset Description**



The project uses the Predictive Maintenance Dataset containing machine operational information.



The dataset includes:



Input Features:



Product ID

Machine Type

Air Temperature

Process Temperature

Rotational Speed

Torque

Tool Wear



Target Variable:



Failure Type



The target represents different machine conditions such as:



No Failure

Heat Dissipation Failure

Power Failure

Overstrain Failure

Tool Wear Failure

Random Failure



**4. Data Preprocessing and Cleaning**



Before training the models, the dataset was analyzed and cleaned.



4.1 Data Cleaning



The following preprocessing steps were performed:



Checked for missing values.

Checked duplicate records.

Removed unnecessary columns.

Selected meaningful operational parameters.

Prepared the dataset for machine learning.



4.2 Feature Selection



The original dataset contained some columns that were not useful for prediction.



Identifier-based columns were removed because they do not represent machine behavior.



Final selected features:



Machine Type

Air Temperature \[K]

Process Temperature \[K]

Rotational Speed \[rpm]

Torque \[Nm]

Tool Wear \[min]



**5. Handling Data Leakage**



During preprocessing, possible data leakage issues were identified.



Data leakage occurs when the model receives information during training that would not be available during real-world prediction.



To prevent this:



Failure-related information was removed from input features.

Only real-time machine sensor parameters were used.

The model was trained using information available before failure occurrence.



This improves the reliability of predictions in real-world scenarios.



**6. Machine Learning Models**



MachineGuard AI uses two prediction approaches.



Model 1: Random Forest Classifier



The first model is a local machine learning model trained using Scikit-learn.



Purpose:



Provides local prediction capability.

Acts as a fallback model.

Works even when cloud AI services are unavailable.



Advantages:



Handles complex relationships between sensor parameters.

Works well with classification problems.

Provides reliable predictions for machine conditions.

Model 2: IBM Watsonx AI Model



The second prediction approach uses IBM Watsonx AI services.



Purpose:



Provides cloud-based AI prediction.

Demonstrates IBM Cloud integration.

Enables scalable AI deployment.



The prediction flow:



User Input

&#x20;     ↓

IBM Watsonx AI Model

&#x20;     ↓

Failure Prediction



If unavailable:



&#x20;     ↓



Random Forest Local Model



**7. IBM BOB Integration**

IBM BOB (Build Operations Bot)



IBM BOB is included as part of the project demonstration to showcase AI-assisted operational workflows.



The role of IBM BOB in MachineGuard AI:



Demonstrates AI-based interaction with the predictive maintenance system.

Helps explain project workflow and operational use case.

Represents how AI assistants can support decision-making in industrial environments.



Through IBM BOB, the project highlights the future possibility of combining predictive analytics with intelligent AI assistants for maintenance operations.



**8. System Architecture**



The complete architecture of MachineGuard AI:



&#x20;               User

&#x20;                 |

&#x20;                 ↓

&#x20;       Streamlit Application

&#x20;                 |

&#x20;                 ↓

&#x20;         Prediction API Layer

&#x20;                 |

&#x20;       ---------------------

&#x20;       |                   |

&#x20;       ↓                   ↓

&#x20;IBM Watsonx AI       Random Forest Model

&#x20;       |                   |

&#x20;       --------Fallback-----

&#x20;                 |

&#x20;                 ↓

&#x20;      Failure Classification

&#x20;                 |

&#x20;                 ↓

&#x20;Severity Detection + Recommendation Engine

&#x20;                 |

&#x20;                 ↓

&#x20;     Maintenance Action Report



**9. Application Development**



Technology Stack

Component	       Technology

Programming Language	Python

Frontend	       Streamlit

Machine Learning      Scikit-learn

Model Storage	         Joblib

Cloud AI	     IBM Watsonx AI

AI Assistant	        IBM BOB



Application Features



MachineGuard AI provides:



User-friendly sensor input interface.

Machine failure prediction.

Prediction confidence score.

Failure severity classification.

Maintenance recommendations.

Cloud AI and local fallback support.



**10. Results and Testing**



Normal Machine Condition



Example:



Prediction:



No Failure



Confidence:



100%



The system identifies normal operating conditions successfully.



Failure Detection



Example:



Prediction:



Overstrain Failure



Confidence:



42.2%



Severity:



Critical



Recommendation:



Stop machine operation.

Reduce mechanical load.

Inspect machine components.

Replace damaged tools.



**11. Conclusion**



MachineGuard AI successfully demonstrates an AI-based predictive maintenance solution using machine learning and IBM Watsonx AI.



The system can:



Analyze machine sensor data.

Predict possible failures.

Provide maintenance recommendations.

Support preventive maintenance decisions.



The combination of ML models, IBM AI services, and an interactive dashboard makes the system suitable for industrial maintenance applications.



**12. Future Scope**



Future improvements include:



Real-time IoT sensor integration.

Live machine monitoring.

Advanced deep learning models.

Automated maintenance scheduling.

Integration with industrial control systems.



