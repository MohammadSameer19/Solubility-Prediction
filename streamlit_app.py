import os
import json
import pandas as pd
import streamlit as st
import sklearn

# Must be first Streamlit command
st.set_page_config(page_title="Solubility Predictor", layout="wide")

# Import skops with fallback
try:
    from skops.io import load as skops_load, get_untrusted_types as skops_get_untrusted_types
    SKOPS_AVAILABLE = True
except ImportError:
    SKOPS_AVAILABLE = False

ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
FEATURES_PATH = os.path.join(ARTIFACT_DIR, "feature_columns.json")

st.title("Solubility Predictor (logS)")
st.caption(f"scikit-learn runtime: {sklearn.__version__}")

# Check for required files
if not os.path.isdir(ARTIFACT_DIR) or not os.path.exists(FEATURES_PATH):
    st.error("Artifacts not found. Run training and save models in the notebook first.")
    st.stop()

# Load feature columns
with open(FEATURES_PATH) as f:
    feature_cols = json.load(f)["columns"]

# Find available models (.skops preferred, .joblib fallback) - Linear Regression only
available_models = {}
model_name = "linear_regression"
skops_path = os.path.join(ARTIFACT_DIR, f"{model_name}.skops")
joblib_path = os.path.join(ARTIFACT_DIR, f"{model_name}.joblib")

display_name = "Linear Regression"

if os.path.exists(skops_path) and SKOPS_AVAILABLE:
    available_models[display_name] = skops_path
elif os.path.exists(joblib_path):
    available_models[display_name] = joblib_path

if not available_models:
    st.error("Linear Regression model not found. Run the notebook cells to train and save the model.")
    st.stop()

# Use Linear Regression directly (no selection needed)
model_name = "Linear Regression"
st.info("Using Linear Regression model")

@st.cache_resource
def load_model(path: str):
    """Load model with proper format detection."""
    import warnings
    try:
        if path.endswith(".skops") and SKOPS_AVAILABLE:
            with open(path, 'rb') as f:
                trusted_types = list(skops_get_untrusted_types(file=f))
            return skops_load(path, trusted=trusted_types)
        else:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                import joblib
                return joblib.load(path)
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {e}")

# Load selected model
try:
    model_path = available_models[model_name]
    model = load_model(model_path)
    
    # Show model info
    model_type = "skops" if model_path.endswith(".skops") else "joblib"
    st.caption(f"Model format: {model_type}")
    
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Prediction interface
st.subheader("Prediction mode")
mode = st.radio("Choose input method", ["Upload CSV", "Manual entry"], horizontal=True)

# Template download
with st.expander("Template / Feature Schema"):
    st.write(f"Required features: {len(feature_cols)}")
    template_csv = pd.DataFrame(columns=feature_cols).to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV template", data=template_csv, file_name="template.csv", mime="text/csv")

if mode == "Upload CSV":
    st.markdown("Upload a CSV file with the required feature columns.")
    uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Remove target column if present
        if "logS" in df.columns:
            df = df.drop(columns=["logS"])
        
        # Check for missing columns
        missing_cols = [col for col in feature_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Missing columns: {missing_cols[:5]}{'...' if len(missing_cols) > 5 else ''}")
        else:
            # Align columns and predict
            X = df.reindex(columns=feature_cols)
            predictions = model.predict(X)
            
            # Create output DataFrame
            result_df = df.copy()
            result_df["predicted_logS"] = predictions
            
            st.success(f"Predictions completed for {len(result_df)} rows")
            st.dataframe(result_df.head(20), use_container_width=True)
            
            # Download predictions
            result_csv = result_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download predictions", 
                data=result_csv, 
                file_name="predictions.csv", 
                mime="text/csv"
            )
    else:
        st.info("Please upload a CSV file to get predictions.")

else:  # Manual entry mode
    st.markdown("Enter feature values manually for a single compound.")
    
    # Initialize values
    init_option = st.selectbox("Initialize with:", ["Zeros", "Empty"], index=0)
    initial_values = {col: (0.0 if init_option == "Zeros" else None) for col in feature_cols}
    input_df = pd.DataFrame([initial_values])
    
    # Editable table
    edited_df = st.data_editor(
        input_df,
        num_rows="fixed",
        use_container_width=True,
        key="manual_entry"
    )
    
    st.caption("Edit the values above, then click Predict.")
    
    if st.button("Predict", type="primary"):
        # Prepare data
        X = edited_df.reindex(columns=feature_cols)
        X = X.apply(pd.to_numeric, errors="coerce")
        
        # Handle missing values
        missing_count = X.isna().sum().sum()
        if missing_count > 0:
            st.warning(f"Filled {missing_count} missing/invalid values with 0.")
            X = X.fillna(0.0)
        
        # Predict
        prediction = model.predict(X)[0]
        
        # Display result
        result_df = edited_df.copy()
        result_df["predicted_logS"] = prediction
        
        st.success(f"Predicted solubility (logS): **{prediction:.4f}**")
        st.dataframe(result_df, use_container_width=True)
        X = edited_df.reindex(columns=feature_cols)
        X = X.apply(pd.to_numeric, errors="coerce")
        
        # Handle missing values
        missing_count = X.isna().sum().sum()
        if missing_count > 0:
            st.warning(f"Filled {missing_count} missing/invalid values with 0.")
            X = X.fillna(0.0)
        
        # Predict
        prediction = model.predict(X)[0]
        
        # Display result
        result_df = edited_df.copy()
        result_df["predicted_logS"] = prediction
        
        st.success(f"Predicted solubility (logS): **{prediction:.4f}**")
        st.dataframe(result_df, use_container_width=True)
        st.dataframe(result_df, use_container_width=True)
