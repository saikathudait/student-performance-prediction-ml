from functools import lru_cache
import pickle

import pandas as pd
from django.conf import settings

MODEL_FEATURES = [
    "school",
    "sex",
    "age",
    "address",
    "famsize",
    "Pstatus",
    "Medu",
    "Fedu",
    "Mjob",
    "Fjob",
    "reason",
    "guardian",
    "traveltime",
    "studytime",
    "failures",
    "schoolsup",
    "famsup",
    "paid",
    "activities",
    "nursery",
    "higher",
    "internet",
    "romantic",
    "famrel",
    "freetime",
    "goout",
    "Dalc",
    "Walc",
    "health",
    "absences",
    "G1",
    "G2",
]


@lru_cache(maxsize=1)
def load_model():
    with open(settings.MODEL_PATH, "rb") as handle:
        return pickle.load(handle)


def _default_features():
    defaults = settings.PREDICTION_DEFAULTS.copy()
    return defaults


def build_model_input(cleaned_data):
    payload = _default_features()
    payload.update(
        {
            "school": cleaned_data["school"],
            "sex": cleaned_data["gender"],
            "age": cleaned_data["age"],
            "address": cleaned_data["address"],
            "famsize": cleaned_data["family_size"],
            "Pstatus": cleaned_data["parental_status"],
            "Medu": cleaned_data["mother_education"],
            "Fedu": cleaned_data["father_education"],
            "guardian": cleaned_data["guardian"],
            "traveltime": cleaned_data["travel_time"],
            "studytime": cleaned_data["study_time"],
            "failures": cleaned_data["failures"],
            "famsup": cleaned_data["family_support"],
            "activities": cleaned_data["activities"],
            "internet": cleaned_data["internet_access"],
            "health": cleaned_data["health"],
            "absences": cleaned_data["absences"],
            "G1": cleaned_data["g1"],
            "G2": cleaned_data["g2"],
        }
    )

    missing = [name for name in MODEL_FEATURES if name not in payload]
    if missing:
        raise ValueError(f"Missing model features: {missing}")

    return pd.DataFrame([payload], columns=MODEL_FEATURES)


def predict(cleaned_data):
    model = load_model()
    inputs = build_model_input(cleaned_data)
    raw_prediction = int(model.predict(inputs)[0])

    confidence = None
    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(inputs)[0][1])
        confidence = probability if raw_prediction == 1 else 1 - probability

    label = "PASS" if raw_prediction == 1 else "FAIL"
    return label, confidence
