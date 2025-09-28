# Solubility Prediction Model

A machine learning web application for predicting chemical compound solubility (logS) using molecular descriptors.

## Features

- **Interactive Web Interface**: Built with Streamlit
- **Multiple Input Methods**: 
  - CSV file upload for batch predictions
  - Manual entry for single compound prediction
- **Machine Learning Models**: Linear Regression trained on the Delaney solubility dataset
- **Real-time Predictions**: Get instant solubility predictions
- **Export Results**: Download predictions as CSV files

## Dataset

This project uses the Delaney solubility dataset, which contains:
- 1,144 chemical compounds
- Molecular descriptors (features)
- Experimental solubility values (logS target)

**Source**: [Delaney Solubility Dataset on Kaggle](https://www.kaggle.com/datasets/sorkun/delaney-solubility-with-descriptors)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/solubility-prediction.git
cd solubility-prediction
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Download the dataset:
   - Download `delaney_solubility_with_descriptors.csv` from Kaggle
   - Place it in the project root directory

## Usage

### Training the Model

1. Open and run the Jupyter notebook:
```bash
jupyter notebook solubility-prediction-model.ipynb
```

2. Execute all cells to:
   - Load and explore the dataset
   - Train the Linear Regression model
   - Save the trained model in the `artifacts/` folder

### Running the Web Application

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the Web Interface

1. **Upload CSV**: 
   - Download the template CSV
   - Fill in molecular descriptor values
   - Upload and get batch predictions

2. **Manual Entry**:
   - Enter values directly in the editable table
   - Click "Predict" for instant results

## Model Performance

The Linear Regression model achieves:
- Training R²: ~0.77
- Test R²: ~0.74
- Training MSE: ~0.55
- Test MSE: ~0.58

## Project Structure

```
solubility-prediction/
├── solubility-prediction-model.ipynb  # Training notebook
├── streamlit_app.py                   # Web application
├── requirements.txt                   # Python dependencies
├── README.md                          # Project documentation
├── artifacts/                         # Trained models (created after training)
│   ├── linear_regression.joblib
│   ├── linear_regression.skops
│   └── feature_columns.json
└── delaney_solubility_with_descriptors.csv  # Dataset (download separately)
```

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
