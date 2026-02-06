# Student Performance Prediction System

## Project Overview
The **Student Performance Prediction System** is a machine learning–based project designed to predict whether a student will **Pass or Fail** based on academic performance, demographic attributes, and behavioural factors.  
The project demonstrates a complete **end-to-end ML workflow**, achieving **90%+ accuracy** using multiple classification models and selecting the best-performing model through comparison.

---

## Web Application (Django + MySQL)

### Quick Start
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and update database credentials.
4. Create the MySQL database `student_prediction_db`.
5. Run migrations:
   ```bash
   python manage.py makemigrations predictions
   python manage.py migrate
   ```
6. Start the server:
   ```bash
   python manage.py runserver
   ```
7. Open the app at:
   ```
   http://127.0.0.1:8000
   ```

### Notes
- The model file is loaded from `best_student_model.pkl` at project root.
- Default values for non-form features can be tuned in `student_performance/settings.py`.

---

## Dataset Information
 
- **Dataset Name:** Student Performance Dataset  
- **Source:** Kaggle (UCI Machine Learning Repository)  
- **Dataset Link:**  
  https://www.kaggle.com/datasets/larsen0966/student-performance-data-set  

### Dataset Summary
| Attribute | Value |
|---------|------|
| Total Records | 649 |
| Total Features | 33 |
| Categorical Features | 17 |
| Numerical Features | 15 |
| Target Variable | `pass_fail` |
| Missing Values | None |
| Duplicate Rows | 0 |

---

## Feature Description

### Categorical Features
school, sex, address, famsize, Pstatus,
Mjob, Fjob, reason, guardian,
schoolsup, famsup, paid, activities,
nursery, higher, internet, romantic


### Numerical Features
age, Medu, Fedu, traveltime, studytime, failures,
famrel, freetime, goout, Dalc, Walc,
health, absences, G1, G2


### Target Variable
- **G3** – Final Grade (0–20)
- **pass_fail**
  - `1` → Pass (G3 ≥ 10)
  - `0` → Fail (G3 < 10)

---

## Class Distribution

| Class | Proportion |
|------|-----------|
| Pass (1) | 84.59% |
| Fail (0) | 15.41% |

> The dataset shows moderate class imbalance, handled during model evaluation.

---

## Tools & Libraries

- Python  
- Google Colab  
- pandas, numpy  
- matplotlib  
- scikit-learn  
- xgboost  
- pickle  

---

## Project Workflow

1. Data loading and inspection  
2. Exploratory Data Analysis (EDA)  
3. Feature engineering and target creation  
4. Data preprocessing using pipelines  
5. Train-test split (80/20, stratified)  
6. Model training (4 classifiers)  
7. Model evaluation and comparison  
8. Best model selection  
9. Model saving for deployment  

---

##  Machine Learning Models Used

1. **Logistic Regression**  
2. **Random Forest Classifier**  
3. **Gradient Boosting Classifier**  
4. **XGBoost Classifier**

---

## Model Performance Comparison

| Model | Accuracy | ROC-AUC |
|------|---------|---------|
| **Gradient Boosting** | **0.9154** | **0.9605** |
| Logistic Regression | 0.9077 | 0.9273 |
| XGBoost | 0.9077 | 0.9514 |
| Random Forest | 0.8846 | 0.9259 |

---

##  Best Model

### Gradient Boosting Classifier
- **Accuracy:** 91.54%  
- **ROC-AUC:** 96.05%  
- Best overall balance between precision, recall, and generalization  

---

## Evaluation Metrics Used

- Accuracy  
- Precision  
- Recall  
- F1-Score  
- Confusion Matrix  
- ROC-AUC Curve  

---

##  Sample Prediction

The trained model predicts **Pass/Fail** using:
- Study time
- Attendance (absences)
- Past exam scores (G1, G2)
- Demographic and behavioural attributes

---

##  Model Export

The best-performing model is saved as:

```bash
best_student_model.pkl
```

This file can be directly used for:

Flask API

Django backend

Streamlit app

REST-based deployment

# Why This Project Stands Out

End-to-end ML pipeline

Real-world education dataset

Multiple model comparison

High accuracy (90%+)

Interview-ready use case

Clean preprocessing with pipelines

Deployment-ready model

# Future Enhancements

Web-based user interface

Grade prediction (regression)

Hyperparameter tuning

Feature importance analysis

Early-warning academic risk system

---

# Additional Web App Updates (New)

## New Pages
- About, How It Works, Insights, Contact
- Student Dashboard, Profile, History
- Staff Dashboard (`/superadmin/`)
- User Management (`/superadmin/users/`)

## Authentication & Roles
- Students can register/login and view only their own history
- Staff users are redirected to the staff dashboard after login
- Login/Register hidden after authentication

## Staff Features
- Staff control panel with metrics and recent predictions
- User management: toggle staff/admin/active status

## Admin URLs
- Staff panel: `http://127.0.0.1:8000/superadmin/`
- Django admin (if needed): `http://127.0.0.1:8000/django-admin/`

## UI Enhancements
- Professional multi-page design
- Advanced form validation and help text
- Custom staff panel layout (not default Django admin)
