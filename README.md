# Solubility Prediction Model

A machine learning web application for predicting chemical compound solubility (logS) using molecular descriptors.

## Features

- **Interactive Web Interface**: Built with Streamlit
- **Multiple Input Methods**: 
  - CSV file upload for batch predictions
  - Manual entry for single compound prediction
- **Machine Learning Model**: Linear Regression trained on the Delaney solubility dataset
- **Real-time Predictions**: Get instant solubility predictions
- **Export Results**: Download predictions as CSV files

## Dataset

This project uses the Delaney solubility dataset, which contains:
- 1,144 chemical compounds
- Molecular descriptors (features)
- Experimental solubility values (logS target)

**Source**: [Delaney Solubility Dataset on Kaggle](https://www.kaggle.com/datasets/sorkun/delaney-solubility-with-descriptors)

## Local Development

1. Clone this repository:
```bash
git clone https://github.com/yourusername/solubility-prediction.git
cd solubility-prediction
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Train the model by running the notebook and executing all cells

4. Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

## Cloud Deployment (Google Cloud Run)

### Prerequisites
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### Enable APIs
```bash
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com
```

### Deploy
```bash
gcloud builds submit --config cloudbuild.yaml
```

Your app will be available at: `https://solubility-predictor-[hash]-as.a.run.app`

### Local Docker Testing
```bash
# Build image
docker build -t solubility-predictor .

# Run on custom host port (maps HOST:CONTAINER = 8087:8080)
docker run -e PORT=8080 -p 8087:8080 solubility-predictor

# Open in browser:
# http://localhost:8087
```

## Project Structure

```
solubility-prediction/
├── solubility-prediction-model.ipynb  # Training notebook
├── streamlit_app.py                   # Web application
├── Dockerfile                         # Container configuration
├── cloudbuild.yaml                    # Cloud Build configuration
├── requirements.txt                   # Python dependencies
├── README.md                          # Documentation
└── artifacts/                         # Trained models (created after training)
    ├── linear_regression.joblib
    └── feature_columns.json
```

## Model Performance

The Linear Regression model achieves:
- Training R²: ~0.77
- Test R²: ~0.74
- Training MSE: ~0.55
- Test MSE: ~0.58

## License

This project is licensed under the MIT License.
## Requirements

- Python 3.7+
- pandas
- numpy
- scikit-learn
- streamlit
- matplotlib
- joblib
- skops

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Delaney et al. for the solubility dataset
- Scikit-learn team for the machine learning library
- Streamlit team for the web app framework

## Deployment

### Google Cloud Run (Recommended)

1. **Prerequisites**:
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

2. **Enable APIs**:
```bash
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com
```

3. **Deploy**:
```bash
gcloud builds submit --config cloudbuild.yaml
```

Your app will be available at: `https://solubility-predictor-[hash]-as.a.run.app`

### Google App Engine (Alternative)

```bash
gcloud app deploy
```

### Local Docker Testing

```bash
docker build -t solubility-predictor .
docker run -p 8080:8080 solubility-predictor
```

## Environment Variables

For cloud deployment, set these if needed:
- `STREAMLIT_SERVER_PORT=8080`
- `STREAMLIT_SERVER_ADDRESS=0.0.0.0`
- `STREAMLIT_SERVER_PORT=8080`
- `STREAMLIT_SERVER_ADDRESS=0.0.0.0`
