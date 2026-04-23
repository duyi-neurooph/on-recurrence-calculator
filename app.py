import math
import streamlit as st

st.set_page_config(page_title="ON Recurrence Calculator", layout="centered")

# Final no-age Andersen–Gill model
BETA_FEMALE = 0.2396
BETA_ONFEL_YES_MALE = -0.6066
BETA_TRT_LOW = 0.4386
BETA_TRT_PLACEBO = -0.0940
BETA_DISC_EDEMA = -0.2843
BETA_FEMALE_X_ONFEL = 1.3896

# Baseline survival at selected horizons
S0_1 = 0.8750
S0_3 = 0.7731
S0_5 = 0.7248

def recurrence_prob(baseline_survival: float, lp: float) -> float:
    return 1 - (baseline_survival ** math.exp(lp))

st.title("Optic Neuritis Recurrence Risk Calculator")

sex = st.selectbox("Sex", ["Male", "Female"])
onfel = st.selectbox("History of Fellow-Eye Optic Neuritis", ["No", "Yes"])
trt = st.selectbox(
    "Treatment Regimen",
    [
        "High-Dose Intravenous Methylprednisolone",
        "Low-Dose Oral Prednisone",
        "No Active Corticosteroid"
    ]
)
disc = st.selectbox("Optic Disc in Affected Eye", ["Normal", "Edema"])

female = 1 if sex == "Female" else 0
onfel_yes = 1 if onfel == "Yes" else 0
low_dose = 1 if trt == "Low-Dose Oral Prednisone" else 0
placebo = 1 if trt == "No Active Corticosteroid" else 0
edema = 1 if disc == "Edema" else 0

lp = 0.0
lp += BETA_FEMALE * female
lp += BETA_ONFEL_YES_MALE * onfel_yes
lp += BETA_TRT_LOW * low_dose
lp += BETA_TRT_PLACEBO * placebo
lp += BETA_DISC_EDEMA * edema
lp += BETA_FEMALE_X_ONFEL * female * onfel_yes

risk_1 = recurrence_prob(S0_1, lp)
risk_3 = recurrence_prob(S0_3, lp)
risk_5 = recurrence_prob(S0_5, lp)

st.subheader("Predicted Recurrence Risk")
c1, c2, c3 = st.columns(3)
c1.metric("1 Year", f"{risk_1:.1%}")
c2.metric("3 Years", f"{risk_3:.1%}")
c3.metric("5 Years", f"{risk_5:.1%}")

st.divider()
st.write("Linear Predictor:", round(lp, 4))
