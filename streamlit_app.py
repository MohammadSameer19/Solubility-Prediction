import os
import io
import json
import zipfile
import urllib.request
import pandas as pd
import streamlit as st
import sklearn

# Streamlit config first
st.set_page_config(page_title="Solubility Predictor", layout="wide")

# Model location and optional remote ZIP (now using the app root)
BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.getenv("MODEL_DIR", BASE_DIR)  # default to app root
MODEL_ZIP_URL = os.getenv("MODEL_ZIP_URL")  # renamed from ARTIFACTS_ZIP_URL

def ensure_model_files():
    os.makedirs(MODEL_DIR, exist_ok=True)
    feature_path = os.path.join(MODEL_DIR, "feature_columns.json")
    model_joblib = os.path.join(MODEL_DIR, "linear_regression.joblib")

    if os.path.exists(feature_path) and os.path.exists(model_joblib):
        return

    if MODEL_ZIP_URL:
        try:
            st.caption("Downloading model files from MODEL_ZIP_URL...")
            with urllib.request.urlopen(MODEL_ZIP_URL) as resp:
                buf = resp.read()
            with zipfile.ZipFile(io.BytesIO(buf)) as zf:
                zf.extractall(MODEL_DIR)
        except Exception as e:
            st.error(f"Failed to download model files: {e}")

    if not (os.path.exists(feature_path) and os.path.exists(model_joblib)):
        req1 = os.path.join(MODEL_DIR, "linear_regression.joblib")
        req2 = os.path.join(MODEL_DIR, "feature_columns.json")
        st.error(
            f"Model files not found. Ensure the image (or MODEL_ZIP_URL) provides:\n"
            f"- {req1}\n"
            f"- {req2}"
        )
        st.stop()

ensure_model_files()

# Debug: list files in the model directory at runtime
try:
    st.caption(f"Model dir: {MODEL_DIR} | files: {', '.join(sorted(os.listdir(MODEL_DIR))[:20])}")
except Exception:
    pass

st.title("Solubility Predictor (logS)")

# Load features and model (from app root)
FEATURES_PATH = os.path.join(MODEL_DIR, "feature_columns.json")
MODEL_PATH = os.path.join(MODEL_DIR, "linear_regression.joblib")
with open(FEATURES_PATH) as f:
    feature_cols = json.load(f)["columns"]

import warnings, joblib
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    MODEL = joblib.load(MODEL_PATH)

st.subheader("Prediction mode")
mode = st.radio("Choose input method", ["Upload CSV", "Manual entry"], horizontal=True)

with st.expander("Template / Feature Schema"):
    st.write(f"Required features: {len(feature_cols)}")
    template_csv = pd.DataFrame(columns=feature_cols).to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV template", data=template_csv, file_name="template.csv", mime="text/csv")

if mode == "Upload CSV":
    st.markdown("Upload a CSV file with the required feature columns.")
    uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if "logS" in df.columns:
            df = df.drop(columns=["logS"])
        missing = [c for c in feature_cols if c not in df.columns]
        if missing:
            st.error(f"Missing columns: {missing[:5]}{'...' if len(missing) > 5 else ''}")
        else:
            X = df.reindex(columns=feature_cols)
            preds = MODEL.predict(X)
            out = df.copy()
            out["predicted_logS"] = preds
            st.success(f"Predicted {len(out)} rows.")
            st.dataframe(out.head(20), use_container_width=True)
            st.download_button("Download predictions", data=out.to_csv(index=False).encode("utf-8"),
                               file_name="predictions.csv", mime="text/csv")
    else:
        st.info("Please upload a CSV file to get predictions.")
else:
    st.markdown("Enter feature values manually for a single compound.")
    init = st.selectbox("Initialize with:", ["Zeros", "Empty"], index=0)
    initial = {c: (0.0 if init == "Zeros" else None) for c in feature_cols}
    edited_df = st.data_editor(pd.DataFrame([initial]), num_rows="fixed", use_container_width=True, key="manual")
    st.caption("Edit values above, then click Predict.")
    if st.button("Predict", type="primary"):
        X = edited_df.reindex(columns=feature_cols).apply(pd.to_numeric, errors="coerce").fillna(0.0)
        pred = MODEL.predict(X)[0]
        out = edited_df.copy()
        out["predicted_logS"] = pred
        st.success(f"Predicted solubility (logS): {pred:.4f}")
        st.dataframe(out, use_container_width=True)